"""Manual, edition-bounded geomantic arithmetic; no house or predictive judgment."""
import copy
import html
import json
from pathlib import Path
import re
from types import MappingProxyType
from .knowledge import Rule
from .scrying import freeze, thaw, digest, _object, _optional_text, load_input

ROOT = Path(__file__).resolve().parents[1]
DATA = freeze(json.loads((ROOT/'knowledge/geomancy_profile_v1.json').read_text(encoding='utf-8')))
PROFILE = DATA['profile']
CONVENTION = DATA['figure_convention']
PROFILE_HASH = digest(thaw(DATA))
FIGURES = MappingProxyType({f['pattern']: f for f in DATA['figures']})
ALIASES = MappingProxyType({s.casefold(): f['pattern'] for f in DATA['figures']
                           for s in (f['id'], f['name'], *f['aliases'])})
PARENTS = tuple(tuple(DATA['parents'][str(i)]) for i in range(9, 16))
ROLES = ('mother',)*4+('daughter',)*4+('niece',)*4+('witness',)*2+('judge',)
TIERS = ((1,2,3,4,5,6,7,8), (9,10,11,12), (13,14), (15,))


def pattern(value):
    if isinstance(value, str) and re.fullmatch('[12]{4}', value):
        return value
    if isinstance(value, (list, tuple)) and len(value) == 4 and all(type(x) is int and x in (1,2) for x in value):
        return ''.join(map(str, value))
    raise ValueError('Figure requires four top-to-bottom rows, each integer 1 or 2, or four 1/2 digits')


def lookup(value):
    if not isinstance(value, str):
        raise ValueError('Figure lookup requires exact text ID, name, alias or four-digit pattern')
    p = value if value in FIGURES else ALIASES.get(value.casefold())
    if p is None:
        raise ValueError('Unknown figure in named Turner convention')
    return thaw(FIGURES[p])


def add(a, b):
    a, b = pattern(a), pattern(b)
    return ''.join(str(1 if (int(x)+int(y)) % 2 else 2) for x,y in zip(a,b))


def chart(mothers):
    if not isinstance(mothers, (list, tuple)) or len(mothers) != 4:
        raise ValueError('Exactly four ordered Mothers required')
    figures = [pattern(m) for m in mothers]
    figures.extend(''.join(m[row] for m in figures[:4]) for row in range(4))
    for a,b in PARENTS:
        figures.append(add(figures[a-1], figures[b-1]))
    return figures


def validate(value):
    _object(value, ['schema_version','profile','figure_convention','task','mode','input_mode',
                    'mothers','mark_counts','figure_ids','lookup','layout','origin',
                    'question','commentary','association'])
    if type(value.get('schema_version')) is not int or value['schema_version'] != 1:
        raise ValueError('schema_version must be integer 1')
    if value.get('profile') != PROFILE or value.get('mode') != 'manual':
        raise ValueError('Exact Turner profile and manual mode required; seeded mode unsupported')
    if value.get('figure_convention', CONVENTION) != CONVENTION:
        raise ValueError('Unknown or unsupported figure convention')
    if value.get('layout','right_to_left') not in ('right_to_left','left_to_right'):
        raise ValueError('Unsupported display orientation')
    if value.get('origin','unknown') not in ('reported_real','hypothetical','synthetic','unknown'):
        raise ValueError('Unsupported declared origin')
    for key in ('question','commentary','association'):
        _optional_text(value,key,10000)
    task = value.get('task')
    fields = set(value) & {'input_mode','mothers','mark_counts','figure_ids'}
    if task == 'figure_catalog':
        if fields:
            raise ValueError('Catalog request must not supply shield inputs')
        if 'lookup' in value:
            values = value['lookup']
            if not isinstance(values,list) or not 1 <= len(values) <= 16:
                raise ValueError('lookup must contain 1–16 exact figure references')
            for v in values:
                lookup(v)
    elif task == 'shield':
        if 'lookup' in value:
            raise ValueError('Use figure_catalog task for lookup')
        mode = value.get('input_mode')
        field = {'patterns':'mothers','mark_counts':'mark_counts','figure_ids':'figure_ids'}.get(mode) if isinstance(mode,str) else None
        if field is None or fields != {'input_mode',field}:
            raise ValueError('One explicit patterns, mark_counts or figure_ids input mode required; mixed inputs rejected')
        rows = value[field]
        size = 16 if mode == 'mark_counts' else 4
        if not isinstance(rows,list) or len(rows) != size:
            raise ValueError(f'{field} requires exactly {size} ordered values')
        if mode == 'patterns':
            for row in rows:pattern(row)
        elif mode == 'mark_counts':
            if any(type(n) is not int or not 1 <= n <= 1000000 for n in rows):
                raise ValueError('Each mark count must be a positive integer at most 1000000; booleans rejected')
        else:
            for row in rows:lookup(row)
    else:
        raise ValueError('Supported tasks: shield and figure_catalog; house projection and horary judgment unsupported')
    return copy.deepcopy(value)


def _mothers(q):
    if q['input_mode'] == 'patterns':return [pattern(p) for p in q['mothers']]
    if q['input_mode'] == 'figure_ids':return [lookup(v)['pattern'] for v in q['figure_ids']]
    values = q['mark_counts']
    return [''.join('1' if n%2 else '2' for n in values[i:i+4]) for i in range(0,16,4)]


def _positions(figures):
    positions = []
    for i,p in enumerate(figures,1):
        role = ROLES[i-1]
        if i <= 4:
            parents, trace, operation = [], [], 'manual_mother'
        elif i <= 8:
            parents, operation = [1,2,3,4], 'row_transposition'
            trace = [dict(parent=j,parent_row=i-4,dot_count=int(figures[j-1][i-5])) for j in parents]
        else:
            parents = list(PARENTS[i-9]);operation = 'parity_addition'
            trace = [dict(row=j+1,inputs=[int(figures[k-1][j]) for k in parents],
                          sum=sum(int(figures[k-1][j]) for k in parents),result=int(p[j])) for j in range(4)]
        positions.append(dict(position=i,role=role,pattern=p,rows=list(map(int,p)),figure=lookup(p),
                              parents=parents,operation=operation,line_trace=trace,
                              source_id=DATA['source']['id'],locator=DATA['construction_locator']))
    return positions


def register_knowledge(registry):
    registry.add_source(thaw(DATA['source']))
    for f in DATA['figures']:
        registry.add_rule(Rule('geomancy.figure.'+f['id'],1,33,'16 figures',CONVENTION,
            DATA['source']['id'],f['locator'],f['name']+' = '+f['pattern'],
            'geomancy_pattern_identity',dict(pattern=f['pattern']),'proposed','traditional',[]))
    registry.add_rule(Rule('geomancy.shield',1,33,'European shield chart',PROFILE,
        DATA['source']['id'],DATA['construction_locator'],'Fifteen-position common shield parity construction',
        'geomancy_manual_shield',dict(parents=thaw(DATA['parents'])),'proposed','traditional',[]))


def read(value, registry=None):
    q = validate(value)
    if registry is not None:register_knowledge(registry)
    mothers = _mothers(q) if q['task'] == 'shield' else None
    figures = chart(mothers) if mothers is not None else None
    layout = q.get('layout','right_to_left')
    tiers = [list(reversed(t)) if layout == 'right_to_left' else list(t) for t in TIERS] if figures else []
    return dict(schema_version=1,technique_id=33,profile=PROFILE,figure_convention=CONVENTION,
        source=thaw(DATA['source']),source_limits=DATA['source_limits'],source_collation=thaw(DATA['source_collation']),
        task=q['task'],mode='manual',origin=q.get('origin','unknown'),
        representation=dict(rows='top_to_bottom',dot_counts={'1':'one dot / odd','2':'two dots / even'},binary=DATA['binary']),
        input_mothers=mothers,original_mark_counts=q.get('mark_counts'),
        mark_parity_trace=[dict(index=i+1,mother=i//4+1,row=i%4+1,count=n,result=1 if n%2 else 2) for i,n in enumerate(q.get('mark_counts',[]))],
        positions=_positions(figures) if figures else [],
        layout=dict(orientation=layout,logical_order=DATA['logical_order'],tiers_left_to_right=tiers,
                    convention='Editorial shield display; logical positions are never renumbered. Top tier groups Mothers and Daughters; each tier reverses only for display.'),
        judge=lookup(figures[14]) if figures else None,
        invariants=dict(position_count=len(figures or []),judge_even_total_points=sum(map(int,figures[14]))%2==0 if figures else None),
        figure_catalog=[lookup(v) for v in q['lookup']] if 'lookup' in q else thaw(DATA['figures']) if q['task']=='figure_catalog' else None,
        alias_policy=DATA['alias_policy'],optional_sixteenth=DATA['optional_sixteenth'],
        provenance_matrix=dict(direct='Edition-located figure names, patterns and construction rules',compositional='Explicit transposition, parent lineage and parity arithmetic; no inferred prediction',user_attributed='Unmodified request, counts, question, comments and associations',unsupported='House/horary judgment, universal tradition or predictive validity'),
        user_text={k:q[k] for k in ('question','commentary','association') if k in q},
        limitations=thaw(DATA['unsupported']),qualification='Historical mathematical construction only. A correct Judge is not a certified yes/no answer or prediction.',
        replay=dict(request=q,input_sha256=digest(q),profile_sha256=PROFILE_HASH,source_sha256=DATA['source']['snapshot_sha256'],
                    serialization='SHA256 of canonical UTF8 sorted-key compact JSON, unescaped Unicode, no terminal LF; raw field whitespace retained',external_calls=False,rng=False))


def markdown(result):
    def block(obj):
        text=json.dumps(obj,ensure_ascii=False,indent=2)
        fence='`'*max(3,1+max((len(x) for x in re.findall(r'`+',text)),default=0))
        return fence+'json\n'+text+'\n'+fence
    lines=['# Western Geomancy shield construction','',html.escape(result['qualification']),
           '',f'Profile: {PROFILE}; figure convention: {CONVENTION}']
    if result['positions']:
        lines+=['','## Shield layout','', 'Rows are top-to-bottom. Cells below run left-to-right on the page; labels retain logical position.', '', '```text']
        for tier in result['layout']['tiers_left_to_right']:
            lines.append(' | '.join(f'{i:02d} {result["positions"][i-1]["pattern"]}' for i in tier))
        lines+=['```','','| Position | Role | Pattern | Figure | Parents |','| --- | --- | --- | --- | --- |']
        for row in result['positions']:
            lines.append(f'| {row["position"]} | {row["role"]} | {row["pattern"]} | {row["figure"]["name"]} | {row["parents"]} |')
    for title,key in [('Source edition and rights','source'),('Source limits','source_limits'),('Collation','source_collation'),
        ('Row representation','representation'),('Display convention','layout'),('Original counts','original_mark_counts'),
        ('Count-to-parity trace','mark_parity_trace'),('Complete derivation trace','positions'),('Judge identity','judge'),
        ('Construction invariants','invariants'),('Figure catalog','figure_catalog'),('Alias convention','alias_policy'),
        ('Optional sixteenth','optional_sixteenth'),('User text','user_text'),('Evidence layers','provenance_matrix'),
        ('Unsupported coverage','limitations'),('Exact replay metadata','replay')]:
        lines+=['','## '+title,'',block(result[key])]
    return '\n'.join(lines)+'\n'


def rejection(message,fmt):
    if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),geomancy_report=None),indent=2)
    return '# Geomancy request rejected\n\n'+html.escape(str(message))+'\n'
