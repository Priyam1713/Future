"""Source-specific heuristics and exact descriptive forecast evaluation."""
import copy
from decimal import Decimal, localcontext, ROUND_HALF_EVEN
from fractions import Fraction
import html
import json
from pathlib import Path
import re

from .remote_viewing import canonical, digest, obj, text, identifier, timestamp, hexhash, file_bytes, bytes_hash
from .scrying import load_input, freeze, thaw

ROOT = Path(__file__).resolve().parents[1]
PROFILE_HASH = '9e744dcb6fcd6f8e4ce854c76cafadeae0d9d4e2fa24e77786646c6cf04bc113'


def assets():
    p = load_input(ROOT/'knowledge/intuitive_prediction_profile_v1.json')
    if digest(p) != PROFILE_HASH:
        raise ValueError('Pinned intuition profile mismatch')
    for name, key in [('sources', 'source_manifest_sha256'), ('source_freeze_v1', 'source_freeze_sha256')]:
        if digest(load_input(ROOT/f'knowledge/intuitive_prediction_{name}.json')) != p[key]:
            raise ValueError('Pinned intuition provenance mismatch')
    return p


DATA = freeze(assets())
PROFILES = DATA['profiles']


def fields(v, name):
    obj(v, DATA['fields'][name])


def nonempty(v):
    if not text(v, 4000).strip():
        raise ValueError('Nonempty declared text required')
    return v


def boolean(v):
    if type(v) is not bool:
        raise ValueError('Explicit boolean declaration required')


def probability(v):
    if not isinstance(v, str) or len(v) > 102 or not re.fullmatch(r'(?:0|1)(?:\.[0-9]{1,100})?', v):
        raise ValueError('Plain decimal probability string required')
    q = Fraction(v)
    if not 0 <= q <= 1:
        raise ValueError('Probability outside [0,1]')
    return q


def number(q):
    if q is None:
        return None
    q = Fraction(q)
    with localcontext() as ctx:
        ctx.prec = 260
        value = (Decimal(q.numerator)/Decimal(q.denominator)).quantize(Decimal('0.000000000001'), rounding=ROUND_HALF_EVEN)
    return dict(exact=str(q), decimal=format(value, 'f'))


def sequence(v, maximum=1000):
    if not isinstance(v, list) or len(v) > maximum:
        raise ValueError('Bounded list required')


def context_review(v):
    fields(v, 'context')
    warnings = []
    for k in ('regularity', 'cue_validity', 'feedback_quality', 'feedback_latency'):
        if v[k] not in ('adequate', 'inadequate', 'unknown'):
            raise ValueError('Context state must be adequate/inadequate/unknown')
        if v[k] != 'adequate':
            warnings.append(k+':'+v[k])
    text(v['practice_history'], 4000)
    boolean(v['environment_changed'])
    if v['environment_changed']:
        warnings.append('environment_changed:prior_validity_may_not_transfer')
    return dict(declarations=copy.deepcopy(v), warnings=warnings, expert_certified=False,
                qualification='Human learning-context declarations, not an expertise classifier or measured skill.')


def decision(d):
    fields(d, 'decision')
    identifier(d['decision_id']); timestamp(d['observed_at'])
    sequence(d['alternatives'], 2); sequence(d['recognition'], 2); sequence(d['cues'], 100)
    if len(d['alternatives']) != 2 or len(set(d['alternatives'])) != 2 or len(d['recognition']) != 2:
        raise ValueError('Two distinct alternatives and recognition declarations required')
    for x in d['alternatives']: identifier(x)
    for k in ('criterion', 'domain', 'direction_provenance', 'training_period'): nonempty(d[k])
    for k in ('confidence', 'notes'): text(d[k], 20000)
    if any(x not in ('recognized', 'unrecognized', 'unknown') for x in d['recognition']):
        raise ValueError('Invalid recognition state')
    if d['criterion_direction'] not in ('higher', 'lower') or d['ecological_direction'] not in ('positive', 'negative', 'unknown'):
        raise ValueError('Invalid declared direction')
    if d['profile'] not in PROFILES.values() or d['tie_policy'] not in ('abstain', 'frozen_order'):
        raise ValueError('Unsupported algorithm or tie policy')
    context = context_review(d['context'])
    cue_ids = []; validities = []; previous_rank = 0
    for c in d['cues']:
        fields(c, 'cue'); identifier(c['cue_id']); sequence(c['values'], 2)
        if len(c['values']) != 2 or any(x not in ('positive', 'negative', 'unknown') for x in c['values']):
            raise ValueError('Two exact cue states required')
        q = probability(c['validity'])
        if q < Fraction(1, 2) or c['orientation'] != 'positive':
            raise ValueError('Unsupported cue orientation; independently documented recoding required')
        if type(c['rank']) is not int or c['rank'] <= previous_rank:
            raise ValueError('Frozen cue ranks must strictly increase')
        previous_rank = c['rank']
        if validities and q > validities[-1]:
            raise ValueError('Cue validities must follow supplied descending order')
        for k in ('provenance', 'training_period'): nonempty(c[k])
        cue_ids.append(c['cue_id']); validities.append(q)
    if len(set(cue_ids)) != len(cue_ids): raise ValueError('Duplicate cue ID')
    is_ttb = d['profile'] == PROFILES['take-the-best']
    if not is_ttb and d['cues']: raise ValueError('Recognition-only profile does not consume cues')
    if is_ttb and (d['ecological_direction'] != 'positive' or d['criterion_direction'] != 'higher'):
        raise ValueError('1996TTB requires its own positive recognition/higher-criterion convention')
    selected = None; decisive = None; trace = []; reason = 'unknown_recognition'
    states = d['recognition']
    branch = 'unknown' if 'unknown' in states else 'both' if states == ['recognized']*2 else 'neither' if states == ['unrecognized']*2 else 'one'
    if branch == 'one':
        if d['ecological_direction'] == 'unknown': reason = 'unknown_ecological_direction'
        else:
            side = states.index('recognized')
            if not is_ttb and ((d['ecological_direction'] == 'negative') != (d['criterion_direction'] == 'lower')):
                side = 1-side
            selected = d['alternatives'][side]; reason = 'recognition_rule'
    elif is_ttb and branch == 'both':
        if len(set(validities)) != len(validities) and d['tie_policy'] != 'frozen_order':
            reason = 'ambiguous_validity_tie'
        else:
            reason = 'exhausted_cues_editorial_abstention'
            for c in d['cues']:
                x, y = c['values']; side = None
                if x == 'positive' and y != 'positive': side = 0
                elif y == 'positive' and x != 'positive': side = 1
                trace.append(dict(cue=copy.deepcopy(c), discriminates=side is not None,
                                  disposition='decisive' if side is not None else 'nondiscriminating_skip'))
                if side is not None:
                    selected = d['alternatives'][side]; decisive = c['cue_id']; reason = 'first_discriminating_cue'; break
    elif branch != 'unknown': reason = branch+'_recognized_abstention'
    return dict(input=copy.deepcopy(d), algorithm=d['profile'], recognition_branch=branch,
                inspected=trace, not_inspected=cue_ids[len(trace):], decisive_cue=decisive,
                selected=selected, reason=reason, domain_review=context,
                convention='1996source random branches replaced by deterministic editorial abstention' if is_ttb else '2002isolated recognition rule;lower-criterion inversion explicit',
                probability_generated=False, evidence_layer='Source algorithm plus declared user inputs and named editorial conventions')


def evidence(v, root):
    fields(v, 'evidence'); hexhash(v['sha256'])
    for k in ('holder', 'permission', 'provenance'): nonempty(v[k])
    if bytes_hash(file_bytes(root, v['path'])) != v['sha256']:
        raise ValueError('Evidence bytes mismatch')


def check_plan(p, root):
    fields(p, 'plan'); identifier(p['study_id']); created = timestamp(p['created_at'])
    for k in ('domain', 'horizon', 'event_definition'): nonempty(p[k])
    boolean(p['privacy_consent'])
    if not p['privacy_consent']: raise ValueError('Explicit local private-record consent required')
    sequence(p['events'], 500); sequence(p['slots'], 1000)
    if not p['events'] or not p['slots']: raise ValueError('Nonempty finite event and slot manifests required')
    events = {}; slots = {}; keys = set()
    for e in p['events']:
        fields(e, 'event'); identifier(e['event_id']); identifier(e['dependency_group']); nonempty(e['question'])
        start, end, cutoff = (timestamp(e[k]) for k in ('window_start', 'window_end', 'cutoff'))
        if e['event_id'] in events or start > end or cutoff < created:
            raise ValueError('Duplicate event or invalid frozen window/cutoff')
        events[e['event_id']] = e
    for s in p['slots']:
        fields(s, 'slot')
        for k in ('forecast_id', 'forecaster', 'event_id'): identifier(s[k])
        key = (s['forecaster'], s['event_id'])
        if s['forecast_id'] in slots or key in keys or s['event_id'] not in events:
            raise ValueError('Duplicate/unknown slot or forecaster/event pair')
        slots[s['forecast_id']] = s; keys.add(key)
    b = p['baseline']
    if b is not None:
        fields(b, 'baseline'); q = probability(b['probability'])
        for k in ('domain', 'horizon', 'event_definition'):
            if b[k] != p[k]: raise ValueError('Incompatible baseline scope')
        if not timestamp(b['training_start']) <= timestamp(b['training_end']) < timestamp(b['frozen_at']) <= created:
            raise ValueError('Training must finish before baseline freeze and plan')
        sequence(b['training_outcomes'], 10000)
        if not b['training_outcomes']: raise ValueError('Training outcomes required')
        ids = []; total = 0
        for t in b['training_outcomes']:
            fields(t, 'training_outcome'); identifier(t['event_id'])
            if type(t['outcome']) is not int or t['outcome'] not in (0, 1): raise ValueError('Binary training outcome required')
            ids.append(t['event_id']); total += t['outcome']
        if len(ids) != len(set(ids)) or set(ids) & set(events): raise ValueError('Baseline training/evaluation leakage or duplicate training ID')
        if q != Fraction(total, len(ids)): raise ValueError('Baseline probability must equal frozen training prevalence')
        evidence(b['evidence'], root)
    return events, slots


def create(plan, root=ROOT):
    check_plan(plan, root)
    return dict(schema_version=1, profile_sha256=PROFILE_HASH, plan=copy.deepcopy(plan), plan_sha256=digest(plan), actions=[])


def replay(l, root=ROOT):
    fields(l, 'ledger')
    if type(l['schema_version']) is not int or l['schema_version'] != 1 or l['profile_sha256'] != PROFILE_HASH or digest(l['plan']) != l['plan_sha256']:
        raise ValueError('Ledger protocol/plan hash mismatch')
    events, slots = check_plan(l['plan'], root)
    sequence(l['actions'], 20000)
    state = dict(decisions={}, forecasts={s: [] for s in slots}, resolutions={e: [] for e in events})
    parent = l['plan_sha256']; last = timestamp(l['plan']['created_at'])
    for i, a in enumerate(l['actions'], 1):
        fields(a, 'action'); body = {k: v for k, v in a.items() if k != 'sha256'}
        if type(a['sequence']) is not int or a['sequence'] != i or a['parent_sha256'] != parent or a['sha256'] != digest(body):
            raise ValueError('Action chain mismatch')
        v = a['payload']; kind = a['kind']
        if kind == 'decision':
            result = decision(v); at = timestamp(v['observed_at'])
            if v['decision_id'] in state['decisions'] or v['domain'] != l['plan']['domain']:
                raise ValueError('Duplicate decision or incompatible domain')
            state['decisions'][v['decision_id']] = result
        elif kind == 'forecast':
            fields(v, 'forecast'); identifier(v['forecast_id']); probability(v['probability']); boolean(v['outcome_known'])
            at = timestamp(v['at'])
            for k in ('confidence', 'notes'): text(v[k], 20000)
            nonempty(v['reason'])
            if v['forecast_id'] not in slots: raise ValueError('Unplanned forecast slot')
            versions = state['forecasts'][v['forecast_id']]
            expected = versions[-1]['sha256'] if versions else None
            if v['parent_sha256'] != expected: raise ValueError('Wrong original/amendment parent hash')
            if v['decision_id'] is not None and v['decision_id'] not in state['decisions']:
                raise ValueError('Unknown decision link;probability must be separately submitted')
            versions.append(dict(record=copy.deepcopy(v), sha256=digest(v), sequence=i))
        elif kind == 'resolve':
            fields(v, 'resolution'); identifier(v['event_id']); at = timestamp(v['at'])
            if v['event_id'] not in events or v['status'] not in ('resolved', 'unresolved', 'disputed', 'void'):
                raise ValueError('Unknown event or resolution status')
            if v['status'] == 'resolved':
                if type(v['outcome']) is not int or v['outcome'] not in (0, 1): raise ValueError('Resolved binary outcome required')
            elif v['outcome'] is not None: raise ValueError('Nonresolved outcome must remain null')
            for k in ('occurrence_at', 'publication_at', 'discovery_at'):
                if v[k] is not None and timestamp(v[k]) > at: raise ValueError('Resolution cannot precede declared event information')
            if v['evidence'] is not None: evidence(v['evidence'], root)
            old = state['resolutions'][v['event_id']]
            if old and old[-1]['status'] == 'resolved' and v['status'] == 'resolved':
                raise ValueError('Resolved outcome cannot silently be replaced;record dispute first')
            old.append(copy.deepcopy(v))
        else: raise ValueError('Unsupported ledger action')
        if at < last: raise ValueError('Actions must be appended in nondecreasing declared time')
        last = at; parent = a['sha256']
    return state


def append(l, kind, payload, root=ROOT):
    replay(l, root)
    out = copy.deepcopy(l)
    a = dict(sequence=len(l['actions'])+1, kind=kind, payload=copy.deepcopy(payload),
             parent_sha256=l['actions'][-1]['sha256'] if l['actions'] else l['plan_sha256'])
    a['sha256'] = digest(a); out['actions'].append(a)
    replay(out, root)
    return out


def evaluate(l, root=ROOT):
    state = replay(l, root); p = l['plan']; events = {e['event_id']: e for e in p['events']}
    bins = [dict(index=i, lower=str(Fraction(i, 10)), upper=str(Fraction(i+1, 10)), upper_inclusive=i == 9,
                 count=0, events=0, mean_probability=None, observed_frequency=None, unscored_count=0) for i in range(10)]
    bucket = [[] for _ in bins]; rows = []; scored = []; baseline_losses = []; version_count = late = amended = on_time = 0
    for slot in p['slots']:
        e = events[slot['event_id']]; versions = state['forecasts'][slot['forecast_id']]
        history = state['resolutions'][e['event_id']]; r = history[-1] if history else None
        candidates = []; vr = []
        amended += max(0, len(versions)-1); version_count += len(versions)
        for version in versions:
            v = version['record']; at = timestamp(v['at']); reasons = []
            if at > timestamp(e['cutoff']): reasons.append('after_cutoff'); late += 1
            if v['outcome_known']: reasons.append('outcome_known')
            if r and r['occurrence_at'] is not None and at >= timestamp(r['occurrence_at']): reasons.append('at_or_after_occurrence')
            vr.append(dict(**version, exclusion_reasons=reasons))
            if not reasons: candidates.append(version)
        selected = candidates[-1] if candidates else None
        reasons = []; loss = None; b_loss = None
        if not versions: reasons.append('unsubmitted')
        elif selected is None: reasons.append('no_eligible_forecast_version')
        if selected is not None: on_time += 1
        status = r['status'] if r else 'unresolved'
        if status != 'resolved': reasons.append(status)
        if r is None or r['occurrence_at'] is None: reasons.append('occurrence_time_unknown')
        elif not timestamp(e['window_start']) <= timestamp(r['occurrence_at']) <= timestamp(e['window_end']): reasons.append('outside_event_window')
        if r is None or r['evidence'] is None: reasons.append('missing_resolution_evidence')
        q = probability(selected['record']['probability']) if selected else None
        index = min(9, (q*10).numerator//(q*10).denominator) if q is not None else None
        if not reasons:
            loss = (q-r['outcome'])**2; scored.append((slot, q, r['outcome'], loss))
            bucket[index].append((q, r['outcome']))
            if p['baseline'] is not None:
                b_loss = (probability(p['baseline']['probability'])-r['outcome'])**2; baseline_losses.append(b_loss)
        elif index is not None: bins[index]['unscored_count'] += 1
        rows.append(dict(slot=copy.deepcopy(slot),event=copy.deepcopy(e),versions=vr,selected_version_sha256=selected['sha256'] if selected else None,
                         status=status,resolution_history=copy.deepcopy(history),scored=loss is not None,exclusion_reasons=reasons,
                         loss=number(loss),baseline_loss=number(b_loss)))
    for b, values in zip(bins, bucket):
        if values:
            b.update(count=len(values), events=sum(y for _,y in values), mean_probability=number(sum(q for q,_ in values)/len(values)),
                     observed_frequency=number(Fraction(sum(y for _,y in values),len(values))))
    n = len(scored); bs = sum(x[3] for x in scored)/n if n else None
    bmean = sum(baseline_losses)/n if baseline_losses else None
    counts = dict(planned=len(p['slots']),submitted=sum(bool(v) for v in state['forecasts'].values()),versions=version_count,
                  on_time_selected=on_time,late_versions=late,amendments=amended,resolved_and_scored=n,
                  unresolved=sum(x['status']=='unresolved' for x in rows),disputed=sum(x['status']=='disputed' for x in rows),
                  void=sum(x['status']=='void' for x in rows),missing_resolution_evidence=sum('missing_resolution_evidence' in x['exclusion_reasons'] for x in rows),
                  excluded=sum(not x['scored'] for x in rows),unique_events=len(events),dependency_groups=len({e['dependency_group'] for e in events.values()}),
                  scored_unique_events=len({s['event_id'] for s,_,_,_ in scored}),scored_dependency_groups=len({events[s['event_id']]['dependency_group'] for s,_,_,_ in scored}))
    return dict(plan=copy.deepcopy(p), decisions=list(state['decisions'].values()),forecasts=rows,denominators=counts,
                denominator_units='Slots for submission/status counts;versions for late/amendment counts. Repeated events/forecasters are dependent;no effective independent sample size estimated.',
                brier=number(bs),two_category_positive_quadratic=number(2*bs) if bs is not None else None,
                calibration=bins,baseline=dict(frozen=copy.deepcopy(p['baseline']),brier=number(bmean),paired_absolute_improvement=number(bmean-bs) if bmean is not None else None,
                                              qualification='Same selected resolved pairs;training evidence/IDs/time/domain checks are declarations plus local byte checks;external completeness not attested.'),
                warnings=['Descriptive sample only;N does not establish calibration or expertise.','No empirical human benchmark validated.','Local owner can rewrite history;timestamps,knowledge and identity are declarations.','Rare-event base rates can produce low loss without individualized skill.'])


def reference(v):
    obj(v, ['context', 'rpd'])
    obj(v['rpd'], ['cues_noticed','situation','expectancies','anomalies','candidate_action','mental_simulation','revision_or_alternative','feedback_history'])
    for x in v['rpd'].values(): text(x, 20000)
    return dict(rpd=copy.deepcopy(v['rpd']),domain_review=context_review(v['context']),
                action_selected_by_software=False,qualification='Human-authored RPD documentation;completeness does not certify expertise or optimality.')


def read(request, root=ROOT, registry=None):
    obj(request,['schema_version','task'],['decision','plan','ledger','forecast','resolution','reference'])
    if type(request['schema_version']) is not int or request['schema_version'] != 1: raise ValueError('Unsupported request schema')
    task = request['task']; expected = {'recognition':'decision','take-the-best':'decision','create':'plan','forecast-record':'forecast',
        'forecast-amend':'forecast','resolve':'resolution','decision-record':'decision','decision-reference':'reference',
        'report':'ledger','forecast-score':'ledger','calibration':'ledger','baseline-compare':'ledger','reference':None}
    if task not in expected: raise ValueError('Unsupported intuition task')
    key = expected[task]; needed = {'schema_version','task'} | ({key} if key else set())
    if task in ('forecast-record','forecast-amend','resolve','decision-record'): needed.add('ledger')
    if set(request) != needed: raise ValueError('Task fields mismatch')
    if registry is not None:
        for s in load_input(ROOT/'knowledge/intuitive_prediction_sources.json'): registry.add_source(s)
    ledger = None
    if task in ('recognition','take-the-best'):
        if request['decision']['profile'] != PROFILES[task]: raise ValueError('Task/algorithm mismatch')
        result = decision(request['decision'])
    elif task == 'decision-reference': result = reference(request['reference'])
    elif task == 'reference': result = thaw(DATA)
    else:
        if task == 'create': ledger = create(request['plan'],root)
        elif task in ('forecast-record','forecast-amend','resolve','decision-record'):
            kind = 'forecast' if task in ('forecast-record','forecast-amend') else 'resolve' if task == 'resolve' else 'decision'
            if kind == 'forecast' and ((request['forecast']['parent_sha256'] is None) != (task == 'forecast-record')):
                raise ValueError('Original/amendment task distinction required')
            ledger = append(request['ledger'],kind,request[key],root)
        else: ledger = copy.deepcopy(request['ledger'])
        result = evaluate(ledger,root)
    return dict(technique_id=45,task=task,status='accepted',schema_version=1,profile_sha256=PROFILE_HASH,
                request_sha256=digest(request),source_manifest_sha256=DATA['source_manifest_sha256'],source_freeze_sha256=DATA['source_freeze_sha256'],
                sources=load_input(ROOT/'knowledge/intuitive_prediction_sources.json'),algorithm_profiles=thaw(PROFILES),
                catalog_sha256=digest(thaw(PROFILES)),catalog_scope='Named algorithm ID mapping embedded in the immutable profile',
                result=result,result_sha256=digest(result),ledger=ledger,ledger_sha256=digest(ledger) if ledger else None,
                interpretation_layers=dict(direct='Named inspected algorithm and mathematical rules',user='Recognition,cues,probabilities,context,times,outcomes,rights declarations',
                                           editorial='Abstention,tie,chronology,selection,calibration conventions',unsupported='Expert,psychic,universal-skill or optimal-action certification'),
                limitations=thaw(DATA['limits']))


def markdown(report):
    raw = json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)
    fence = '`'*(max([len(x) for x in re.findall(r'`+',raw)]+[2])+1)
    return '# Intuitive Prediction\n\n'+html.escape(report.get('status','unknown'))+' — explicit rules and descriptive forecast error.\n\n'+fence+'json\n'+raw+'\n'+fence+'\n'
