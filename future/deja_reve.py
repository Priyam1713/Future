"""Human declarations and documentary timing; no narrative classification."""
import copy
import html
import json
from pathlib import Path

from .remote_viewing import canonical, digest, bytes_hash, obj, text, identifier, timestamp, hexhash
from .scrying import load_input, freeze, thaw

ROOT = Path(__file__).resolve().parents[1]
PROFILE_HASH = 'fdfe3074e23b10deb96928d85b3440d2a3122acdcffc5270af3596a854c3698a'


def assets():
    p = load_input(ROOT/'knowledge/deja_reve_profile_v1.json')
    if digest(p) != PROFILE_HASH:
        raise ValueError('Pinned profile mismatch')
    for path, key in [('sources', 'source_manifest_sha256'), ('source_freeze_v1', 'source_freeze_sha256')]:
        if digest(load_input(ROOT/f'knowledge/deja_reve_{path}.json')) != p[key]:
            raise ValueError('Pinned source mismatch')
    return p


DATA = freeze(assets())
ATTRS = ('dream_association', 'specific_recollection', 'temporal_context', 'familiarity',
         'present_dreamy_state', 'subjective_confidence', 'reviewer', 'proposal', 'uncertain')
ORIGINAL = ('profile', 'profile_version', 'kind', 'id', 'pseudonym', 'source_ref', 'occurrence',
            'first_record_at', 'lock_at', 'narrative', 'narrative_sha256', 'context', 'attributes', 'consent')


def nonempty(v):
    if not text(v).strip():
        raise ValueError('Nonempty declaration required')
    return v


def boolean(v):
    if type(v) is not bool:
        raise ValueError('Explicit boolean required')


def sequence(v):
    if not isinstance(v, list) or len(v) > 1000:
        raise ValueError('Bounded list required')


def interval(v):
    if v is None:
        return None
    obj(v, ('start', 'end'))
    a, b = timestamp(v['start']), timestamp(v['end'])
    if a > b:
        raise ValueError('Reversed interval')
    return a, b


def point(v):
    return None if v is None else dict(start=v, end=v)


def chronology(lock, target, conflicting=False):
    t = interval(target)
    k = None if lock is None else timestamp(lock)
    if conflicting:
        return 'conflicting_evidence'
    if k is None or t is None:
        return 'unknown'
    if k < t[0]:
        return 'strictly_earlier'
    if k > t[1]:
        return 'later'
    if t[0] == t[1] == k:
        return 'equal_boundary'
    return 'overlapping_or_ambiguous'


def compatibility(a):
    obj(a, ATTRS)
    for key in ('dream_association', 'specific_recollection', 'familiarity', 'present_dreamy_state'):
        if a[key] is not None:
            boolean(a[key])
    boolean(a['uncertain'])
    if a['temporal_context'] not in ('specific', 'vague', 'none', 'unknown'):
        raise ValueError('Invalid temporal context')
    if a['proposal'] not in (None, 'episodic-like', 'familiarity-like', 'dreamy-state', 'unclassifiable'):
        raise ValueError('Unsupported source proposal')
    identifier(a['reviewer']); text(a['subjective_confidence'])
    d, s, f, y, t = (a[k] for k in ('dream_association', 'specific_recollection', 'familiarity', 'present_dreamy_state', 'temporal_context'))
    conflicts = []
    if s is True and d is False:
        conflicts.append('specific_recollection_without_dream_association')
    if s is False and t == 'specific':
        conflicts.append('specific_temporal_context_without_specific_recollection')
    if y is True and (s is True or f is True):
        conflicts.append('mixed_present_state_and_recollection_or_familiarity')
    if a['uncertain'] or conflicts:
        status, reason = 'review_required', 'explicit_uncertainty_or_conflicting_declarations'
    elif any(v is None for v in (d, s, f, y)):
        status, reason = 'unclassifiable', 'missing_structured_declarations'
    elif s and d and t == 'specific' and not y:
        status, reason = 'episodic_like_compatible', 'declared_specific_dream_with_temporal_context'
    elif d and f and not s and not y and t != 'specific':
        status, reason = 'familiarity_like_compatible', 'declared_dream_familiarity_without_specific_episode'
    elif y and not s and not f:
        status, reason = 'dreamy_state_compatible', 'declared_present_dream_like_state'
    elif not d and not s and not y:
        status, reason = 'unsupported', 'no_declared_dream_association_or_present_dream_state'
    else:
        status, reason = 'unclassifiable', 'insufficient_category_specificity'
    mapped = {'episodic_like_compatible': 'episodic-like', 'familiarity_like_compatible': 'familiarity-like',
              'dreamy_state_compatible': 'dreamy-state', 'unclassifiable': 'unclassifiable'}.get(status)
    return dict(status=status, reason=reason, conflicting_attributes=conflicts,
                declared_proposal=a['proposal'], proposal_disagrees=a['proposal'] is not None and a['proposal'] != mapped,
                qualification='Compatibility of human declarations only;not expert clinical consensus or verified memory.')


def validate_record(r):
    obj(r, ('original', 'original_sha256', 'amendments'))
    o = r['original']; obj(o, ORIGINAL)
    if o['profile'] != DATA['id'] or type(o['profile_version']) is not int or o['profile_version'] != 1:
        raise ValueError('Unsupported exact profile/version')
    if o['kind'] not in ('dream', 'observation') or o['context'] not in ('ordinary_nonclinical', 'declared_clinical_context'):
        raise ValueError('Unsupported record kind/context')
    for key in ('id', 'pseudonym'):
        identifier(o[key])
    nonempty(o['source_ref']); interval(o['occurrence'])
    for key in ('first_record_at', 'lock_at'):
        if o[key] is not None:
            timestamp(o[key])
    text(o['narrative']); hexhash(o['narrative_sha256']); hexhash(r['original_sha256'])
    if bytes_hash(o['narrative'].encode('utf-8')) != o['narrative_sha256'] or digest(o) != r['original_sha256']:
        raise ValueError('Original bytes/version hash mismatch')
    c = o['consent']; obj(c, ('local_processing', 'rights', 'export'))
    boolean(c['local_processing']); boolean(c['export'])
    if not c['local_processing'] or c['export'] or c['rights'] not in ('self_authored', 'permission_granted'):
        raise ValueError('Local processing permission/rights required;export unsupported')
    if o['kind'] == 'observation':
        compatibility(o['attributes'])
    elif o['attributes'] is not None:
        raise ValueError('Dream record has no contemporary observation attributes')
    sequence(r['amendments'])
    parent = r['original_sha256']
    times = [timestamp(o[k]) for k in ('first_record_at', 'lock_at') if o[k] is not None]
    previous = max(times) if times else None
    for i, a in enumerate(r['amendments'], 2):
        obj(a, ('version', 'parent_sha256', 'at', 'reason', 'narrative', 'narrative_sha256', 'knowledge'))
        if type(a['version']) is not int or a['version'] != i or a['parent_sha256'] != parent:
            raise ValueError('Broken amendment lineage')
        at = timestamp(a['at'])
        if previous is not None and at < previous:
            raise ValueError('Backdated amendment')
        nonempty(a['reason']); text(a['narrative']); hexhash(a['narrative_sha256'])
        if bytes_hash(a['narrative'].encode('utf-8')) != a['narrative_sha256']:
            raise ValueError('Amendment bytes mismatch')
        obj(a['knowledge'], ('event_known', 'experience_known'))
        for v in a['knowledge'].values():
            if v is not None:
                boolean(v)
        previous, parent = at, digest(a)
    return r


def timing_conflicts(o):
    reasons = []
    first, lock, occurrence = o['first_record_at'], o['lock_at'], interval(o['occurrence'])
    if first is not None and lock is not None and timestamp(lock) < timestamp(first):
        reasons.append('lock_precedes_first_written_record')
    if first is not None and occurrence is not None and occurrence[0] > timestamp(first):
        reasons.append('reported_occurrence_after_first_written_record')
    return reasons


def compare_record(r, observation, event):
    o = r['original']; x = observation['original']
    issues = timing_conflicts(o)
    # Missing original first-record time cannot acquire provenance from a lock alone.
    lock = o['lock_at'] if o['first_record_at'] is not None else None
    targets = dict(experience=x['occurrence'], first_experience_report=point(x['first_record_at']),
                   event=None if event is None else event['occurrence'])
    result = {k: chronology(lock, t, bool(issues) or bool(timing_conflicts(x)) and k == 'experience') for k, t in targets.items()}
    versions = [dict(version=1, sha256=r['original_sha256'], narrative=o['narrative'], at=o['first_record_at'],
                     chronology=result, knowledge=None)]
    for a in r['amendments']:
        versions.append(dict(version=a['version'], sha256=digest(a), narrative=a['narrative'], at=a['at'], knowledge=a['knowledge'],
                             chronology={k: chronology(a['at'], t) for k, t in targets.items()}))
    return dict(original_sha256=r['original_sha256'], original_narrative_sha256=o['narrative_sha256'],
                reported_dream_occurrence=o['occurrence'], original_first_record_at=o['first_record_at'], original_lock_at=o['lock_at'],
                chronology=result, conflicting_evidence=issues, versions=versions,
                qualification='Timing under declared clocks;hashes do not prove when a dream occurred or was written.')


def validate_manifest(m, observation_id):
    obj(m, ('payload', 'sha256')); p = m['payload']
    obj(p, ('observation_id', 'frozen_at', 'candidates')); timestamp(p['frozen_at'])
    if p['observation_id'] != observation_id or digest(p) != m['sha256']:
        raise ValueError('Frozen candidate manifest mismatch')
    sequence(p['candidates']); seen = set()
    for c in p['candidates']:
        obj(c, ('dream_id', 'original_sha256', 'disposition', 'reason'))
        identifier(c['dream_id']); hexhash(c['original_sha256']); nonempty(c['reason'])
        if c['dream_id'] in seen or c['disposition'] not in ('included', 'excluded'):
            raise ValueError('Duplicate/invalid candidate')
        seen.add(c['dream_id'])
    return p


def ledger(group, observation, event, post_hoc=False):
    obj(group, ('manifest', 'dreams', 'comparisons'))
    p = validate_manifest(group['manifest'], observation['original']['id'])
    sequence(group['dreams']); sequence(group['comparisons'])
    dreams = {}; candidates = {c['dream_id']: c for c in p['candidates']}
    for r in group['dreams']:
        validate_record(r); o = r['original']
        if o['kind'] != 'dream' or o['id'] in dreams or o['id'] not in candidates or r['original_sha256'] != candidates[o['id']]['original_sha256']:
            raise ValueError('Exact candidate ID/original hash mismatch')
        dreams[o['id']] = r
    comparisons = {}; counts = {k: 0 for k in (*DATA['manual_statuses'], 'unreviewed', 'excluded', 'missing_original')}
    for c in group['comparisons']:
        obj(c, ('dream_id', 'version_sha256', 'at', 'reviewer', 'criteria', 'reasoning', 'status'))
        identifier(c['reviewer']); nonempty(c['criteria']); nonempty(c['reasoning']); at = timestamp(c['at'])
        if c['dream_id'] not in candidates or candidates[c['dream_id']]['disposition'] != 'included' or c['dream_id'] not in dreams:
            raise ValueError('Comparison outside finite available candidate set')
        if at < timestamp(p['frozen_at']) or c['status'] not in DATA['manual_statuses']:
            raise ValueError('Comparison predates candidate freeze or invalid status')
        r = dreams[c['dream_id']]
        versions = {r['original_sha256']: r['original']['first_record_at']}
        versions.update({digest(a): a['at'] for a in r['amendments']})
        if c['version_sha256'] not in versions:
            raise ValueError('Comparison version missing')
        vt = versions[c['version_sha256']]
        if vt is not None and at < timestamp(vt):
            raise ValueError('Comparison predates narrative version')
        attempts = comparisons.setdefault(c['dream_id'], [])
        if attempts and at < timestamp(attempts[-1]['at']):
            raise ValueError('Backdated comparison amendment')
        attempts.append(copy.deepcopy(c))
    rows = []
    for c in p['candidates']:
        id_ = c['dream_id']; attempts = comparisons.get(id_, [])
        if c['disposition'] == 'excluded':
            status = 'excluded'
        elif id_ not in dreams:
            status = 'missing_original'
        elif not attempts:
            status = 'unreviewed'
        else:
            status = attempts[-1]['status']
        counts[status] += 1
        rows.append(dict(candidate=copy.deepcopy(c), status=status, comparisons=attempts,
                         provenance=None if id_ not in dreams else compare_record(dreams[id_], observation, event)))
    return dict(manifest=copy.deepcopy(group['manifest']), post_hoc=post_hoc, candidates=rows,
                denominators=dict(candidates=len(rows), comparison_attempts=len(group['comparisons']),
                                  reviewed_candidates=len(comparisons), outcomes=counts),
                selection='Every frozen candidate retained;comparison attempts in supplied append order,final declaration per candidate;no ranking.')


def evaluate(a):
    obj(a, ('observation', 'dreams', 'manifest', 'comparisons', 'event', 'post_hoc'))
    validate_record(a['observation']); o = a['observation']['original']
    if o['kind'] != 'observation':
        raise ValueError('Observation required')
    event = a['event']
    if event is not None:
        obj(event, ('id', 'occurrence', 'publication_at', 'discovery_at', 'evidence_ref', 'evidence_sha256'))
        identifier(event['id']); interval(event['occurrence']); nonempty(event['evidence_ref']); hexhash(event['evidence_sha256'])
        for k in ('publication_at', 'discovery_at'):
            if event[k] is not None:
                timestamp(event[k])
    main = ledger({k: a[k] for k in ('dreams', 'manifest', 'comparisons')}, a['observation'], event)
    sequence(a['post_hoc'])
    later = []
    for g in a['post_hoc']:
        if timestamp(g['manifest']['payload']['frozen_at']) < timestamp(a['manifest']['payload']['frozen_at']):
            raise ValueError('Post-hoc search predates initial search')
        later.append(ledger(g, a['observation'], event, True))
    prior = [r for r in main['candidates'] if r['provenance'] is not None and r['candidate']['disposition'] == 'included' and r['provenance']['chronology']['experience'] == 'strictly_earlier']
    return dict(observation=copy.deepcopy(a['observation']), compatibility=compatibility(o['attributes']),
                observation_timing_conflicts=timing_conflicts(o), candidate_ledger=main, post_hoc_searches=later,
                prior_documentary_status='earlier_original_under_declared_timing' if prior else 'subjective_recollection_without_prior_documentary_record',
                event=copy.deepcopy(event), experience_to_event='conflicting_evidence' if timing_conflicts(o)
                else interval_relation(o['occurrence'], None if event is None else event['occurrence']),
                event_evidence_policy='Evidence reference/hash and publication/discovery times are retained declarations;external event bytes and clocks are not independently authenticated.')


def interval_relation(left, right):
    a, b = interval(left), interval(right)
    if a is None or b is None:
        return 'unknown'
    if a[1] < b[0]:
        return 'strictly_earlier'
    if a[0] > b[1]:
        return 'later'
    if a[0] == a[1] == b[0] == b[1]:
        return 'equal_boundary'
    return 'overlapping_or_ambiguous'


def reference(case_id=None):
    source = load_input(ROOT/'knowledge/deja_reve_source_freeze_v1.json')
    if case_id is None:
        return dict(catalog=thaw(DATA['catalog']), cases=thaw(DATA['cases']), counts=source['counts'], edition=source['edition'],
                    rights=source['rights'], dunne_boundary=source['dunne'], clinical_research_limits=source['limits'])
    for c in DATA['cases']:
        if c['id'] == case_id:
            return dict(case=thaw(c), edition=source['edition'], clinical_research_limits=source['limits'], rights=source['rights'])
    raise ValueError('Unknown documentary case ID')


def read(q, registry=None):
    # Recheck pins at request time as well as module load time.
    assets()
    if not isinstance(q, dict) or type(q.get('schema_version')) is not int or q.get('schema_version') != 1:
        raise ValueError('Schema version1 required')
    task = q.get('task'); fields = {'reference': (), 'annotate': ('record',), 'record': ('record',),
        'amend': ('record', 'amendment'), 'freeze-candidates': ('manifest',), 'link-dream': ('analysis', 'comparison'),
        'compare': ('analysis',), 'report': ('analysis',)}
    if task not in fields:
        raise ValueError('Unsupported task')
    obj(q, ('schema_version', 'task', *fields[task]), ('case_id',) if task == 'reference' else ())
    if registry is not None:
        for s in load_input(ROOT/'knowledge/deja_reve_sources.json'):
            registry.add_source(s)
    if task == 'reference':
        value = reference(q.get('case_id'))
    elif task in ('record', 'annotate', 'amend'):
        r = copy.deepcopy(q['record']); validate_record(r)
        if task == 'amend':
            r['amendments'].append(copy.deepcopy(q['amendment'])); validate_record(r)
        if task == 'annotate':
            if r['original']['kind'] != 'observation':
                raise ValueError('Observation required')
            value = dict(record=r, compatibility=compatibility(r['original']['attributes']))
        else:
            value = dict(record=r, record_sha256=digest(r))
    elif task == 'freeze-candidates':
        value = copy.deepcopy(q['manifest']); validate_manifest(value, value['payload']['observation_id'])
    else:
        a = copy.deepcopy(q['analysis'])
        if task == 'link-dream':
            evaluate(a)
            a['comparisons'].append(copy.deepcopy(q['comparison']))
        value = dict(analysis=a, evaluation=evaluate(a))
    result = dict(status='accepted', task=task, visibility='private_local' if task != 'reference' else 'public_reference',
        profile=dict(id=DATA['id'], version=1, sha256=PROFILE_HASH, source_sha256=DATA['source_manifest_sha256'],
                     source_freeze_sha256=DATA['source_freeze_sha256']), request_sha256=digest(q), result=value,
        limits=thaw(DATA['limits']), privacy=DATA['privacy'])
    result['report_sha256'] = digest(result)
    return result


def markdown(r):
    raw = json.dumps(r, ensure_ascii=False, indent=2, allow_nan=False)
    # Raw text is preserved inside JSON; a fence longer than any submitted run prevents markup escape.
    import re
    fence = '`' * max(3, max((len(x) + 1 for x in re.findall(r'`+', raw)), default=0))
    lines = ['# Déjà Rêvé', '', 'Human declarations and documentary provenance;no diagnosis,memory authenticity or prediction certification.', '']
    e = r.get('result', {}).get('evaluation') if isinstance(r.get('result'), dict) else None
    if e:
        lines.extend([html.escape(e['compatibility']['status']), '', html.escape(e['prior_documentary_status']), '',
                      'Candidate ledger: ' + str(e['candidate_ledger']['denominators']['candidates']) + '; all outcomes and versions below.', ''])
    return '\n'.join(lines + [fence+'json', raw, fence, ''])
