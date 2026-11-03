"""Manual observations and bounded, source-scoped historic symbolic interpretation."""
import copy
import hashlib
import json
import math
from pathlib import Path
from .knowledge import Rule

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'knowledge/palmistry_cheiro_v1.json').read_text(encoding='utf-8'))
PROFILE=DATA['profile']
UNKNOWN=('unknown','uncertain')
QUALITATIVE_TERMS={
    'head.length.short':'Barely reaches mid-palm (p89); not the excluded abnormally-short medical category.',
    'head.length.very_long':'Reaches the outer/little-finger-side edge of the palm (p88),not merely longer than average.',
    'head.curvature.straight_then_sloping':'Straight first half followed by a slight slope (p88).',
    'heart.origin.jupiter':'Central Mount of Jupiter,not the finger itself (p98).',
    'heart.origin.saturn':'Central Mount of Saturn,not the finger itself (p99).',
    'life.branch_to.jupiter':'An ascending branch toward or into Jupiter (p81); no timing inferred.',
    'mounts.developed':'Developed/well-developed ordinary mount,not an excessive enlargement (pp64-65).'}
COMMON=dict(presence=['present','absent'],length=['short','long','very_long'],depth=['deep','shallow'],
    clarity=['clear','unclear'],curvature=['straight','slight_slope','very_sloping','straight_then_sloping'],
    continuity=['unbroken','broken','chained'],branches=['none','upward','downward','both'])
LINE_FIELDS={
    'life':dict(COMMON,origin=['jupiter_base','side'],branch_to=['none','jupiter']),
    'head':dict(COMMON),
    'heart':dict(COMMON,origin=['jupiter','between_jupiter_saturn','saturn'],
        branch_position=['commencement','other'],fork=['none','small_jupiter','jupiter_and_between','jupiter_and_saturn'])}
LIMITS=[
    'Historic symbolic interpretation; not evidence of personality, health, longevity or future outcomes.',
    'Observations are supplied by a person; no photo analysis or independent verification of their accuracy.',
    'Only Cheiro Ninth Edition procedures selected here; no Benham, Saint-Germain or Indian rules substituted.',
    'Missing/uncertain values remain unevaluated; no inference from an absent line to ability or character.',
    'Life-line length,depth and breaks are recorded without health,death or accident interpretations.',
    'Minor markings,elementary type,dermatoglyphics,timing and broad whole-person judgments are unsupported.',
    'Shape subtypes,mount leaning/excess and mixed-hand strong-Head modifications remain unsupported.']


def _object(value,allowed,path):
    if not isinstance(value,dict):raise ValueError(path+' must be an object')
    extra=set(value)-set(allowed)
    if extra:raise ValueError(path+': unknown fields '+','.join(sorted(extra)))


def _enum(value,choices,path):
    if not isinstance(value,str) or value not in list(choices)+list(UNKNOWN):
        raise ValueError(path+': expected '+', '.join(list(choices)+list(UNKNOWN)))


def _notes(values,path):
    if not isinstance(values,list) or len(values)>50 or any(not isinstance(v,str) or not v.strip() or len(v)>500 for v in values):
        raise ValueError(path+' must be a list of up to50 nonempty strings,each <=500 characters')


def validate(observations):
    _object(observations,['schema_version','profile','dominance','hands','unsupported_features'],'input')
    if type(observations.get('schema_version')) is not int or observations['schema_version']!=1:
        raise ValueError('schema_version must be integer1')
    if observations.get('profile')!=PROFILE:raise ValueError('Unsupported source profile')
    _enum(observations.get('dominance','unknown'),['right','left','ambidextrous'],'dominance')
    hands=observations.get('hands')
    if not isinstance(hands,list) or not 1<=len(hands)<=2:raise ValueError('Supply one or two hand observations')
    seen=set()
    for h in hands:
        _object(h,['side','shape','proportions_mm','lines','mounts','head_life_gap','markings'],'hand')
        side=h.get('side')
        if not isinstance(side,str) or side not in ('left','right') or side in seen:raise ValueError('Unique explicit left/right side required')
        seen.add(side)
        shape=h.get('shape',{})
        _object(shape,['type','firmness'],'shape')
        _enum(shape.get('type','unknown'),DATA['shapes'],'shape.type')
        _enum(shape.get('firmness','unknown'),['firm','soft'],'shape.firmness')
        measures=h.get('proportions_mm',{})
        _object(measures,['palm_length','palm_width','middle_finger_length'],'proportions_mm')
        for k,v in measures.items():
            if isinstance(v,str) and v in UNKNOWN:continue
            if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v<=0:
                raise ValueError('Measurements must be finite positive millimeters or unknown/uncertain')
        _enum(h.get('head_life_gap','unknown'),['joined','medium','wide'],'head_life_gap')
        lines=h.get('lines',{})
        _object(lines,LINE_FIELDS,'lines')
        for name,line in lines.items():
            _object(line,LINE_FIELDS[name],name)
            for key,value in line.items():_enum(value,LINE_FIELDS[name][key],name+'.'+key)
        mounts=h.get('mounts',{})
        _object(mounts,DATA['mounts'],'mounts')
        for name,m in mounts.items():
            _object(m,['prominence'],name)
            _enum(m.get('prominence','unknown'),['flat','developed','excessive'],name+'.prominence')
        _notes(h.get('markings',[]),'markings')
    _notes(observations.get('unsupported_features',[]),'unsupported_features')
    return copy.deepcopy(observations)


def _get(h,path):
    v=h
    for key in path.split('.'):
        if not isinstance(v,dict) or key not in v:return 'unknown'
        v=v[key]
    return v


def _contradictions(h):
    """Conflicting observations suppress affected rules; neither value is guessed away."""
    conflicts=[]
    def add(paths,reason):conflicts.append(dict(paths=paths,reason=reason,resolution='withheld; correct observations'))
    for name,line in h.get('lines',{}).items():
        if line.get('presence')=='absent' and any(v not in UNKNOWN for k,v in line.items() if k!='presence'):
            add(['lines.'+name],name+' is absent but has observed properties')
        if line.get('presence') in UNKNOWN or 'presence' not in line:
            # Properties may be entered while presence is unknown; rules retain unknown status.
            continue
        if name=='heart' and line.get('fork','none') not in ('none',*UNKNOWN) and line.get('branches')=='none':
            add(['lines.heart'],'Heart fork conflicts with explicit no branches')
        if name=='heart' and line.get('fork')=='small_jupiter' and line.get('origin') in ('between_jupiter_saturn','saturn'):
            add(['lines.heart'],'Small fork commencing on Jupiter conflicts with the declared non-Jupiter origin')
        if name=='life' and line.get('branch_to')=='jupiter' and line.get('branches') in ('none','downward'):
            add(['lines.life'],'Ascending Jupiter branch conflicts with branch direction')
    gap=h.get('head_life_gap','unknown')
    if gap not in UNKNOWN and any(h.get('lines',{}).get(n,{}).get('presence')=='absent' for n in ('head','life')):
        add(['head_life_gap','lines.head','lines.life'],'Head/Life relationship requires both lines')
    return conflicts


def register_knowledge(registry):
    registry.add_source(DATA['source'])
    for r in DATA['rules']:
        registry.add_rule(Rule(r['id'],r['version'],8,r['section'],PROFILE,r['source_id'],r['locator'],r['text'],
            'palm_observation_match',dict(conditions=r['conditions'],exceptions=r['exceptions']),
            'proposed','traditional',[]))


def _hand(h):
    conflicts=_contradictions(h);traces=[];readings=[];used=set()
    for rule in DATA['rules']:
        conditions=[dict(path=k,expected=v,observed=_get(h,k)) for k,v in rule['conditions'].items()]
        blocked=any(c['path']==p or c['path'].startswith(p+'.') for c in conditions for conflict in conflicts for p in conflict['paths'])
        status=('conflicting_observations' if blocked else 'not_matched' if any(c['observed'] not in UNKNOWN and c['observed']!=c['expected'] for c in conditions)
                else 'unknown' if any(c['observed'] in UNKNOWN for c in conditions) else 'matched')
        trace=dict(rule_id=rule['id'],version=rule['version'],section=rule['section'],status=status,conditions=conditions,
                   source_id=rule['source_id'],locator=rule['locator'])
        traces.append(trace)
        if status=='matched':
            used.update(c['path'] for c in conditions)
            readings.append({k:copy.deepcopy(rule[k]) for k in ('id','version','section','text','coverage','source_id','locator','exceptions','tags')})
    tensions=[]
    # Presentation comparisons only, not new historical prediction rules or weighted synthesis.
    for a,b in [('practical','imaginative'),('steady','changeable'),('cautious','impulsive'),('warm','reserved')]:
        left=[r['id'] for r in readings if a in r['tags']];right=[r['id'] for r in readings if b in r['tags']]
        if left and right:
            tensions.append(dict(topics=[a,b],rule_ids=sorted(set(left+right)),coverage='compositional',
                explanation='Different documented themes coexist; neither overrides the other. This comparison is a presentation aid,not a sourced verdict.'))
    unresolved=[]
    for name in LINE_FIELDS:
        line=h.get('lines',{}).get(name,{})
        for field,value in line.items():
            path=f'lines.{name}.{field}'
            if value not in UNKNOWN and field!='presence' and path not in used:
                unresolved.append(dict(path=path,value=value,coverage='unsupported',reason='Recorded but no fully matched supported interpretation; no inverse or omitted condition assumed.'))
    for name,m in h.get('mounts',{}).items():
        if m.get('prominence') in ('flat','excessive'):
            unresolved.append(dict(path='mounts.'+name,value=m['prominence'],coverage='unsupported',reason='No inverse or excessive-mount reading in this profile.'))
    if h.get('shape',{}).get('type')=='spatulate':
        unresolved.append(dict(path='shape.firmness',coverage='unsupported',reason='p32 distinguishes firm/soft spatulate variants; base action/independence only,not a full subtype reading.'))
    measurements=h.get('proportions_mm',{});ratios={}
    for numerator,denominator in [('palm_length','palm_width'),('middle_finger_length','palm_length')]:
        a,b=measurements.get(numerator),measurements.get(denominator)
        if isinstance(a,(int,float)) and isinstance(b,(int,float)):
            ratio=a/b
            if not math.isfinite(ratio) or ratio==0:raise ValueError('Measurement ratio exceeds supported floating-point range')
            ratios[numerator+'_over_'+denominator]=ratio
    missing=[p for p in ['shape.type','lines.life.presence','lines.head.presence','lines.heart.presence']+
             ['mounts.'+n+'.prominence' for n in DATA['mounts']] if _get(h,p) in UNKNOWN]
    return dict(side=h['side'],source_role='natural/inherited context' if h['side']=='left' else 'acquired/training context',
        observations=copy.deepcopy(h),measurement_ratios=ratios,readings=readings,rule_trace=traces,
        observation_conflicts=conflicts,interpretive_tensions=tensions,unsupported_observations=unresolved,
        unknown_core_observations=missing,unsupported_markings=h.get('markings',[]),
        coverage='partial' if missing or conflicts or unresolved or h.get('markings') else 'supported observations only',
        summary=f"{len(readings)} source-backed symbolic components; {len(conflicts)} observation conflicts; no whole-person verdict.")


def read(observations,registry=None):
    observations=validate(observations)
    if registry is not None:register_knowledge(registry)
    hands=[_hand(h) for h in sorted(observations['hands'],key=lambda h:h['side'])]
    comparison=[]
    if len(hands)==2:
        for rule in DATA['rules']:
            for path in rule['conditions']:
                a,b=(_get(h['observations'],path) for h in hands)
                row=dict(path=path,left=a,right=b)
                if a not in UNKNOWN and b not in UNKNOWN and a!=b and row not in comparison:comparison.append(row)
    release=ROOT/'knowledge/palmistry_core_v1.json'
    return dict(technique_id=8,profile=PROFILE,tradition=DATA['tradition'],schema_version=1,
        release_status=json.loads(release.read_text(encoding='utf-8'))['status'] if release.exists() else 'Developing',
        observations=observations,hands=hands,observed_hand_differences=comparison,
        hand_use=dict(convention=DATA['conventions']['hand_use'],locator='Part II,chIV,pp77-78',
                      dominance=observations.get('dominance','unknown'),dominance_reversal_applied=False,
                      comparison_scope='both hands' if len(hands)==2 else 'single hand; other-hand context missing'),
        unsupported_features=observations.get('unsupported_features',[]),source=DATA['source'],limits=LIMITS,
        observation_guide=dict(line_definitions=DATA['line_definitions'],line_locator='Part II,chII,p72',
            hand_types=DATA['shapes'],mount_locations=DATA['mounts'],qualitative_terms=QUALITATIVE_TERMS,
            interpretation_thresholds='Qualitative source terms; no invented millimeter cutoffs.'),
        reproducibility=dict(profile_version=1,source_scan_sha256=DATA['source']['sha256'],
            observations_sha256=hashlib.sha256(json.dumps(observations,sort_keys=True,ensure_ascii=True,separators=(',',':')).encode()).hexdigest(),
            rules_sha256=hashlib.sha256(json.dumps(DATA['rules'],sort_keys=True).encode()).hexdigest()))


def load_observations(path):
    def unique(pairs):
        result={}
        for k,v in pairs:
            if k in result:raise ValueError('Duplicate JSON field: '+k)
            result[k]=v
        return result
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),object_pairs_hook=unique,
                      parse_constant=lambda x:(_ for _ in ()).throw(ValueError('Non-finite JSON constant '+x)))


def markdown(r):
    out=['# Palmistry reading',f"{r['release_status']} | {r['profile']}",
        'Historical symbolic interpretation, not evidence about personality, health, longevity or future events.',
        '\n'+r['hand_use']['convention'],f"Dominance: {r['hand_use']['dominance']}; automatic reversal: false.",
        'Source: ['+r['source']['edition']+']('+r['source']['url']+')']
    for h in r['hands']:
        out.extend(['\n## '+h['side'].title()+' hand',h['source_role']+'; '+h['summary'],
            '\n### Observations','```json',json.dumps(h['observations'],indent=2,ensure_ascii=False),'```',
            '\n### Source-backed symbolic reading'])
        for section in ('Hand shape','Life line','Head line','Heart line','Mounts'):
            rows=[x for x in h['readings'] if x['section']==section]
            out.append('\n**'+section+'**')
            if not rows:out.append('No fully matched supported reading; observations may be missing,uncertain or outside this profile.')
            for row in rows:
                out.append(f"- Cheiro associates this formation with: {row['text']} [direct; {row['id']} v{row['version']}; {row['locator']}]")
                if row['exceptions']:out.append('  Scope: '+' '.join(row['exceptions']))
        out.extend(['\n### Conflicts and coverage'])
        out.extend('- '+c['reason']+'; affected readings withheld.' for c in h['observation_conflicts'])
        out.extend('- Compositional comparison: '+', '.join(t['topics'])+'. '+t['explanation'] for t in h['interpretive_tensions'])
        out.extend('- Unknown: '+p for p in h['unknown_core_observations'])
        out.extend('- Unsupported: '+c['path']+'. '+c['reason'] for c in h['unsupported_observations'])
        out.extend('- Unsupported marking: '+m for m in h['unsupported_markings'])
    if r['observed_hand_differences']:out.extend(['\n## Observed differences',json.dumps(r['observed_hand_differences'],indent=2)])
    out.extend(['\n## Limits']+['- '+x for x in r['limits']]+['- Unsupported requested feature: '+x for x in r['unsupported_features']])
    return '\n'.join(out)+'\n'
