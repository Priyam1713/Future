"""Local, declared writing events and independently preserved drafts; no text inference."""
import copy
from datetime import datetime
import html
import json
from pathlib import Path
import re
from .knowledge import Rule
from .scrying import freeze, thaw, digest, _object, _raw, _optional_text, _timestamp, load_input

ROOT = Path(__file__).resolve().parents[1]
DATA = freeze(json.loads((ROOT/'knowledge/automatic_writing_profile_v1.json').read_text(encoding='utf-8')))
PROFILE = DATA['profile']
PROFILE_HASH = digest(thaw(DATA))
STATES = ('prepared', 'writing', 'paused', 'resumed', 'stopped', 'under_review', 'completed')
TRANSITIONS = {
    'begin': ({'prepared'}, 'writing'),
    'append': ({'writing', 'resumed'}, None),
    'pause': ({'writing', 'resumed'}, 'paused'),
    'interruption': ({'writing', 'resumed'}, 'paused'),
    'resume': ({'paused'}, 'resumed'),
    'restart': ({'paused'}, 'resumed'),
    'stop': ({'prepared', 'writing', 'resumed', 'paused'}, 'stopped'),
    'review': ({'stopped'}, 'under_review'),
    'revise': ({'under_review'}, None),
    'complete': ({'stopped', 'under_review'}, 'completed'),
}


def _id(value):
    return isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}', value) is not None


def _moment(value):
    if not isinstance(value, str) or 'T' not in value:
        return None
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def interval(start, end):
    """Only declared complete datetime endpoints with compatible awareness yield duration."""
    a, b = _moment(start), _moment(end)
    if a is None or b is None or (a.tzinfo is None) != (b.tzinfo is None):
        return dict(seconds=None, status='unavailable_missing_or_incompatible_endpoints')
    delta = b-a
    if delta.total_seconds() < 0:
        raise ValueError('Comparable declared timestamps must not run backwards')
    microseconds = (delta.days*86400+delta.seconds)*1000000+delta.microseconds
    return dict(seconds=microseconds/1000000, status='declared_endpoints_only')


def metrics(text):
    """Code points; maximal non-whitespace tokens; CRLF/CR/LF delimiters, trailing empty line."""
    return dict(characters=len(text), unicode_code_points=len(text), words=len(text.split()),
                lines=0 if text == '' else 1+len(re.findall(r'\r\n|\r|\n', text)))


def validate(value):
    _object(value, ['schema_version', 'profile', 'task', 'mode', 'session_id', 'intention',
                    'start_time', 'state', 'constraints', 'review_policy', 'events', 'comments',
                    'associations', 'editorial_questions'])
    if type(value.get('schema_version')) is not int or value['schema_version'] != 1:
        raise ValueError('schema_version must be integer1')
    if value.get('profile') != PROFILE or value.get('task') != 'guided_writing' or value.get('mode') != 'manual':
        raise ValueError('Exact Breton subset profile, guided_writing task and manual mode required')
    if not _id(value.get('session_id')):
        raise ValueError('session_id must be a bounded plain identifier')
    if value.get('state') not in STATES:
        raise ValueError('Declare a supported session state')
    if value.get('review_policy', 'optional') not in ('optional', 'required', 'no_review'):
        raise ValueError('Unknown review_policy')
    for field in ('intention', 'comments'):
        _optional_text(value, field, 10000)
    for field in ('constraints', 'associations'):
        if field in value and (not isinstance(value[field], list) or len(value[field]) > 32 or
                              any(not _raw(x, 2000) for x in value[field])):
            raise ValueError(field+' must be an optional bounded user-text list')
    if 'editorial_questions' in value and type(value['editorial_questions']) is not bool:
        raise ValueError('editorial_questions must be boolean')
    _timestamp(value.get('start_time'))
    events = value.get('events', [])
    if not isinstance(events, list) or len(events) > 512:
        raise ValueError('Use at most512 events')
    state = 'prepared'; event_ids = set(); segment_ids = set(); revision_ids = {'first_draft'}
    last_order = 0; last_parent = 'first_draft'; total = 0
    # Compare aware and naive timestamps separately; do not infer timezone for either.
    latest = {True: None, False: None}
    start = _moment(value.get('start_time'))
    if start is not None: latest[start.tzinfo is not None] = start
    for event in events:
        _object(event, ['id', 'type', 'timestamp', 'comment', 'segment', 'revision'])
        identifier = event.get('id'); kind = event.get('type')
        if not _id(identifier) or identifier in event_ids:
            raise ValueError('Event IDs must be unique plain identifiers')
        event_ids.add(identifier)
        if not isinstance(kind, str) or kind not in TRANSITIONS or state not in TRANSITIONS[kind][0]:
            raise ValueError('Illegal event transition from '+state)
        _optional_text(event, 'comment', 2000); _timestamp(event.get('timestamp'))
        moment = _moment(event.get('timestamp'))
        if moment is not None:
            awareness = moment.tzinfo is not None
            if latest[awareness] is not None and moment < latest[awareness]:
                raise ValueError('Comparable declared event timestamps must not run backwards')
            latest[awareness] = moment
        if ('segment' in event) != (kind == 'append') or ('revision' in event) != (kind == 'revise'):
            raise ValueError('Only append/revise events carry their required segment/revision payload')
        if kind == 'append':
            row = event['segment']
            _object(row, ['id', 'text', 'order', 'timestamp', 'elapsed_seconds', 'authorship'])
            if not _id(row.get('id')) or row['id'] in segment_ids:
                raise ValueError('Segment IDs must be unique')
            segment_ids.add(row['id'])
            if type(row.get('order')) is not int or not last_order < row['order'] <= 1000000:
                raise ValueError('Segment orders must strictly increase; input is never sorted')
            last_order = row['order']
            if not _raw(row.get('text'), 20000) or row.get('authorship') != 'user':
                raise ValueError('Segment requires raw UTF8 user-authored text, up to20000 code points')
            total += len(row['text'])
            if total > 200000 or len(segment_ids) > 256:
                raise ValueError('First draft limited to200000 code points and256 segments')
            _timestamp(row.get('timestamp'))
            if row.get('timestamp') is not None and event.get('timestamp') is not None and row['timestamp'] != event['timestamp']:
                raise ValueError('Segment and containing event timestamps must be identical when both declared')
            segment_moment = _moment(row.get('timestamp'))
            if segment_moment is not None:
                awareness = segment_moment.tzinfo is not None
                if latest[awareness] is not None and segment_moment < latest[awareness]:
                    raise ValueError('Comparable segment timestamps must not run backwards')
                latest[awareness] = segment_moment
            elapsed = row.get('elapsed_seconds')
            if elapsed is not None and (type(elapsed) is not int or not 0 <= elapsed <= 604800):
                raise ValueError('Declared segment interval is integer seconds0..604800 or null')
        if kind == 'review' and value.get('review_policy') == 'no_review':
            raise ValueError('Review conflicts with no_review policy')
        if kind == 'complete' and state == 'stopped' and value.get('review_policy') == 'required':
            raise ValueError('Required review must precede completion')
        if kind == 'revise':
            row = event['revision']
            _object(row, ['id', 'parent', 'text', 'authorship', 'comment'])
            if not _id(row.get('id')) or row['id'] in revision_ids or len(revision_ids) > 32:
                raise ValueError('Use up to32 uniquely identified revisions')
            if row.get('parent') != last_parent:
                raise ValueError('Revision parent must be the immediately preceding version, initially first_draft')
            if not _raw(row.get('text'), 200000) or row.get('authorship') != 'user':
                raise ValueError('Revision requires independent raw UTF8 user-authored text')
            _optional_text(row, 'comment', 2000)
            revision_ids.add(row['id']); last_parent = row['id']
        state = TRANSITIONS[kind][1] or state
    if state != value['state']:
        raise ValueError('Declared state disagrees with event replay: '+state)
    return copy.deepcopy(value)


def register_knowledge(registry):
    registry.add_source(thaw(DATA['source']))
    for rule in DATA['rules']:
        registry.add_rule(Rule(rule['id'], 1, 24, 'Surrealist free writing', PROFILE,
                               rule['source_id'], rule['locator'], rule['statement'],
                               'automatic_writing_historical_reference', {}, 'proposed', 'traditional', []))


def read(value, registry=None):
    request = validate(value)
    if registry is not None: register_knowledge(registry)
    events = request.get('events', []); segments = []; revisions = []; timeline = []; state = 'prepared'
    begin = None; stop = None
    for event in events:
        before = state; state = TRANSITIONS[event['type']][1] or state
        timeline.append(dict(event=copy.deepcopy(event), before=before, after=state,
                             provenance='user_declared_event', event_sha256=digest(event)))
        if event['type'] == 'begin': begin = event.get('timestamp')
        if event['type'] == 'stop': stop = event.get('timestamp')
        if event['type'] == 'append':
            row = copy.deepcopy(event['segment'])
            segments.append(dict(record=row, event_id=event['id'], state=state, content_sha256=digest(row)))
    draft = ''.join(row['record']['text'] for row in segments)
    original_hash = digest(dict(id='first_draft', text=draft, segments=[r['record'] for r in segments]))
    parent_hash = original_hash
    for event in events:
        if event['type'] == 'revise':
            row = copy.deepcopy(event['revision'])
            version_hash = digest(dict(record=row, parent_sha256=parent_hash))
            revisions.append(dict(record=row, event_id=event['id'], parent_sha256=parent_hash,
                                  content_sha256=version_hash, metrics=metrics(row['text'])))
            parent_hash = version_hash
    durations = [r['record'].get('elapsed_seconds') for r in segments]
    counts = metrics(draft) | dict(segments=len(segments), pauses=sum(e['type']=='pause' for e in events),
        interruptions=sum(e['type']=='interruption' for e in events), restarts=sum(e['type']=='restart' for e in events),
        revisions=len(revisions), duration=interval(begin, stop),
        declared_segment_seconds=sum(durations) if durations and all(d is not None for d in durations) else None)
    return dict(schema_version=1, technique_id=24, profile=PROFILE, task='guided_writing', mode='manual',
        session=dict(id=request['session_id'], state=state, review_policy=request.get('review_policy','optional'),
                     user_record={k:copy.deepcopy(request[k]) for k in ('intention','start_time','constraints','comments','associations') if k in request}),
        procedure=thaw(DATA), timeline=timeline, original_segments=segments,
        first_draft=dict(id='first_draft', text=draft, content_sha256=original_hash,
                         concatenation='Exact ordered segment text concatenation with empty separator; no normalization'),
        revisions=revisions, metrics=counts,
        metric_conventions=dict(characters='Python Unicode code points; no normalization or grapheme counting',
            words='Maximal nonempty runs separated by Python str.isspace Unicode whitespace; punctuation/emoji remain in tokens',
            lines='Empty text0; otherwise1 plus CRLF/CR/LF delimiters; CRLF is one delimiter, final empty line counted',
            duration='Begin-to-stop declared compatible datetime endpoints only; includes pauses; no inferred active typing time',
            segment_intervals='Sum only when every segment declares an integer interval; not inferred or equated to wall duration'),
        evidence_layers=dict(direct='Seven attributed Breton French-excerpt procedure facts only', user_authored='Raw events, segments, revisions, comments, constraints and associations',
            editorial='State machine, controls, hashes, metrics, review and revision model; constraints may differ from historical procedure',
            unsupported='Spirit contact, trance/unconscious-origin/authorship verification, diagnosis, hidden memories, future prediction'),
        editorial_questions=['Which first-draft passages do you choose to retain?', 'What did you change during review, if anything?'] if request.get('editorial_questions', True) else [],
        limitations=thaw(DATA['limits'])+['Events and authorship are declarations, not mental-state or historical-compliance verification.',
            'Append-only validation applies within each supplied session log; no persistent database, authentication or cross-file tamper protection. Preserve replay files to retain versions.'],
        replay=dict(request=request, input_sha256=digest(request), profile_sha256=PROFILE_HASH,
                    serialization='Canonical UTF8 sorted-key compact JSON, unescaped Unicode, no terminal LF; exact text line endings retained',
                    external_calls=False, rng=False, generated_text=False))


def markdown(result):
    def block(value, language=''):
        fence = '`' * max(3, 1+max((len(x) for x in re.findall(r'`+', value)), default=0))
        return fence+language+'\n'+value+'\n'+fence
    lines = ['# Automatic Writing session', '', 'Profile: '+PROFILE, '',
             'State: '+result['session']['state'], '', '## Historical procedure', '',
             html.escape(result['procedure']['source']['edition']), '',
             '['+result['procedure']['source']['id']+']('+result['procedure']['source']['url']+')', '',
             html.escape(result['procedure']['source']['locator'])]
    for rule in result['procedure']['rules']:
        lines += ['', '- '+html.escape(rule['statement'])+' ['+rule['id']+']']
    lines += ['', html.escape(result['procedure']['translation_comparison']), '',
              html.escape(result['procedure']['source']['rights_note']), '', '## Editorial application conventions', '',
              block(json.dumps(result['procedure']['editorial'], ensure_ascii=False, indent=2), 'json')]
    for title, data in [('Session declarations', result['session']), ('Event timeline', result['timeline']),
                        ('Original writing segments', result['original_segments'])]:
        lines += ['', '## '+title, '', block(json.dumps(data, ensure_ascii=False, indent=2), 'json')]
    lines += ['', '## Original first draft', '', block(result['first_draft']['text']), '',
              'Original content SHA256: '+result['first_draft']['content_sha256'], '', '## Separate revision history']
    for row in result['revisions']:
        lines += ['', '### '+html.escape(row['record']['id'])+' (parent '+html.escape(row['record']['parent'])+')', '',
                  block(row['record']['text']), '', block(json.dumps(row, ensure_ascii=False, indent=2), 'json')]
    for title, data in [('Objective metrics', result['metrics']), ('Metric conventions', result['metric_conventions']),
                        ('Evidence layers', result['evidence_layers']), ('Editorial review questions', result['editorial_questions']),
                        ('Limits', result['limitations']), ('Exact replay metadata', result['replay'])]:
        lines += ['', '## '+title, '', block(json.dumps(data, ensure_ascii=False, indent=2), 'json')]
    return '\n'.join(lines)+'\n'


def rejection(message, fmt):
    if fmt == 'json': return json.dumps(dict(status='rejected', error=str(message), automatic_writing_report=None), indent=2)
    return '# Automatic Writing request rejected\n\n'+html.escape(str(message))+'\n'
