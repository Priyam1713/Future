"""Source-bounded manual symbols and a separately framed digital categorical model."""
import copy
import hashlib
import html
import json
from pathlib import Path
from types import MappingProxyType
from .card_random import Stream, seed_bytes
from .knowledge import Rule


def freeze(v):
    if isinstance(v,dict):return MappingProxyType({k:freeze(x) for k,x in v.items()})
    if isinstance(v,list):return tuple(freeze(x) for x in v)
    return v


def thaw(v):
    if isinstance(v,(dict,MappingProxyType)):return {k:thaw(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [thaw(x) for x in v]
    return v


def digest(v):
    return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')).hexdigest()


ROOT=Path(__file__).resolve().parents[1]
DATA=freeze(json.loads((ROOT/'knowledge/pendulum_profile_v1.json').read_text(encoding='utf-8')))
PROFILE=DATA['profile']
PROTOCOL=DATA['simulation']['protocol']
DISTRIBUTION=DATA['simulation']['distribution']
PROFILE_HASH=digest(thaw(DATA))
CATEGORIES=DATA['simulation']['categories']
WEIGHTS=DATA['simulation']['weights']


class SymbolicStream(Stream):
    """Inherit unchanged integer/rejection methods;use independent Pendulum framing."""
    def __init__(self,seed):
        encoded=seed_bytes(seed)
        self.prefix=b'FuturePendulum\0v1\0symbolic-response\0'+len(encoded).to_bytes(4,'big')+encoded
        self.counter=0;self.pending=[];self.words_used=0;self.rejections=0


def category(index):
    if type(index) is not int or not 0<=index<5:raise ValueError('Index must be integer0..4')
    return 'yes' if index<2 else 'no' if index<4 else 'unresolved'


def simulate(seed):
    stream=SymbolicStream(seed);index=stream.below(5)
    return category(index),dict(protocol=PROTOCOL,distribution=DISTRIBUTION,index=index,
        categories=list(CATEGORIES),weights=list(WEIGHTS),total_weight=5,
        probability_kind='Exact digital sampling allocation;not truth confidence',
        words_used=stream.words_used,rejected_words=stream.rejections,blocks_generated=stream.counter,
        first_block=hashlib.sha256(stream.prefix+bytes(8)).hexdigest(),
        seed_encoding='strict UTF8,1..256 bytes',normalization='none',
        framing=DATA['simulation']['framing'],question_in_rng=False,physical_motion_generated=False)


def _object(v,allowed):
    if not isinstance(v,dict) or set(v)-set(allowed):raise ValueError('Expected object with supported fields only')


def _text(v,limit):
    if not isinstance(v,str) or not v.strip() or len(v)>limit or any(ord(c)<32 for c in v):return False
    try:v.encode('utf-8',errors='strict')
    except UnicodeError:return False
    return True


def calibration(rows):
    if not isinstance(rows,list) or len(rows)>len(DATA['calibration']['mappable_signals']):
        raise ValueError('Calibration must be a list of up to5 distinct signal/response pairs')
    mapping={}
    for row in rows:
        _object(row,['signal','response'])
        signal,response=row.get('signal'),row.get('response')
        if not isinstance(signal,str) or signal not in DATA['calibration']['mappable_signals']:
            raise ValueError('Calibration signal must be a mappable movement category;neutral states are reserved')
        if not isinstance(response,str) or response not in DATA['calibration']['responses']:
            raise ValueError('Unknown calibrated response')
        if signal=='irregular' and response in ('yes','no'):
            raise ValueError('Irregular movement remains unresolved;calibrate a distinct full movement for yes/no')
        if signal in mapping:raise ValueError('Duplicate or contradictory calibration for '+signal+';rejected without repair')
        mapping[signal]=response
    missing=[x for x in ('yes','no') if x not in mapping.values()]
    return dict(mapping=mapping,complete=not missing,missing_responses=missing,
        coverage='user_declared_symbolic_mapping',truth_validated=False)


def validate(value):
    _object(value,['schema_version','profile','task','mode','calibration','observations','seed','protocol','distribution','question'])
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:raise ValueError('schema_version must be integer1')
    if value.get('profile')!=PROFILE or value.get('task')!='symbolic_response':raise ValueError('Exact procedural profile and symbolic_response task required')
    if 'question' in value and not _text(value['question'],1000):raise ValueError('Question must be nonempty plain UTF8 text up to1000 characters')
    if value.get('mode')=='manual':
        if set(value)&{'seed','protocol','distribution'}:raise ValueError('Manual observations cannot include simulation metadata')
        calibration(value.get('calibration'))
        observations=value.get('observations')
        if not isinstance(observations,list) or not 1<=len(observations)<=64:raise ValueError('Provide1..64 recorded observations')
        for row in observations:
            _object(row,['signal','quality'])
            if not _text(row.get('signal'),80):raise ValueError('Signal must be a recorded plain-text category')
            if row.get('quality','full') not in DATA['observations']['quality']:raise ValueError('Unknown observation quality')
    elif value.get('mode')=='seeded':
        if set(value)&{'calibration','observations'}:raise ValueError('Simulation cannot include manual observations/calibration')
        if value.get('protocol')!=PROTOCOL or value.get('distribution')!=DISTRIBUTION:raise ValueError('Exact Pendulum protocol and editorial distribution required')
        seed_bytes(value.get('seed'))
    else:raise ValueError('Use manual or seeded mode')
    return copy.deepcopy(value)


def interpret_observation(row,config):
    signal=row['signal'];quality=row.get('quality','full');mapped=config['mapping'].get(signal)
    reasons=[]
    if not config['complete']:reasons.append('incomplete_calibration')
    if signal not in DATA['signals']:reasons.append('unrecognized_signal')
    elif signal in ('searching','still','irregular','partial','conflicting','unknown'):reasons.append('neutral_or_unclear_signal')
    if quality!='full':reasons.append('observation_'+quality)
    if mapped is None:reasons.append('unmapped_signal')
    elif mapped not in ('yes','no'):reasons.append('calibrated_'+mapped)
    resolved=not reasons
    return dict(signal=signal,signal_definition=DATA['signals'].get(signal,'Unrecognized user-reported category'),
        quality=quality,coverage='user_reported_observation',calibrated_response=mapped,
        symbolic_response=mapped if resolved else 'unresolved',resolved=resolved,reasons=reasons)


def register_knowledge(registry):
    source=thaw(DATA['source']);registry.add_source(source)
    for rule in DATA['rules']:
        registry.add_rule(Rule(rule['id'],1,20,'Yes/no ideomotor',PROFILE,source['id'],rule['locator'],
            rule['statement'],'pendulum_procedure_reference',{},'proposed','traditional',[]))


def read(value,registry=None):
    request=validate(value)
    if registry is not None:register_knowledge(registry)
    if request['mode']=='manual':
        config=calibration(request['calibration'])
        observations=[interpret_observation(row,config) for row in request['observations']]
        responses={r['symbolic_response'] for r in observations}
        resolved=len(responses)==1 and 'unresolved' not in responses
        outcome=next(iter(responses)) if resolved else 'unresolved'
        conflict=len({r['calibrated_response'] for r in observations if r['calibrated_response'] in ('yes','no')})>1 or any(r['signal']=='conflicting' or r['quality']=='conflicting' for r in observations)
        reasons=sorted({reason for row in observations for reason in row['reasons']})
        if conflict:reasons.append('conflicting_observations')
        trace=None;generated=None
    else:
        outcome,trace=simulate(request['seed']);resolved=outcome!='unresolved'
        config=dict(coverage='editorial_digital_distribution',distribution=DISTRIBUTION,
            categories=list(CATEGORIES),weights=list(WEIGHTS),total_weight=5,truth_validated=False)
        observations=[];generated=outcome;conflict=False
        reasons=[] if resolved else ['generated_unresolved_category']
    reflection={'yes':'Use the affirmative symbol to examine what would support proceeding;check real evidence independently.',
        'no':'Use the negative symbol to examine objections or alternatives;it supplies no factual verdict.',
        'unresolved':'Keep the question open. Clarify the wording or the recorded signals;do not force a binary conclusion.'}[outcome]
    replay=dict(request=request,profile=PROFILE,profile_sha256=PROFILE_HASH,source_id=DATA['source']['id'],
        protocol=PROTOCOL if trace else None,seed=request.get('seed'),simulation=trace,
        calibration=config if request['mode']=='manual' else None,aggregation=DATA['observations']['aggregation'] if not trace else None,
        generated_response=generated,generated_signal=None,physical_motion_generated=False,question_in_rng=False)
    return dict(schema_version=1,technique_id=20,profile=PROFILE,task='symbolic_response',mode=request['mode'],question=request.get('question'),
        procedure=dict(source_id=DATA['source']['id'],rules=thaw(DATA['rules']),source_scope='Author-associated website;not print Kit charts or Lethbridge rates'),
        configuration=config,observations=observations,generated_response=generated,generated_signal=None,
        outcome=dict(symbolic_response=outcome,resolved=resolved,resolution_scope='Symbolic category only;not factual assurance',conflicting=conflict,reasons=reasons),
        reflection=dict(coverage='modern_editorial',text=reflection),replay=replay,sources=[thaw(DATA['source'])],
        limitations=list(DATA['limits']),factual_prediction=False,truth_confidence=None,
        physical_motion_observed_by_engine=False)


def markdown(result):
    def safe(v):return html.escape(str(v)).replace('|','&#124;').replace('\n',' ')
    lines=['# Pendulum — symbolic response','','Profile: '+safe(result['profile']),
        '', 'Mode: '+result['mode']+'. '+('User-reported observations.' if result['mode']=='manual' else 'Digital categories only;no motion generated.')]
    if result['question']:lines+=['','Question/context: '+safe(result['question'])]
    lines+=['','## Configuration','','```json',json.dumps(result['configuration'],ensure_ascii=True,indent=2),'```']
    for n,row in enumerate(result['observations'],1):
        lines+=['',str(n)+'. Reported '+safe(row['signal'])+' ('+safe(row['quality'])+'); calibrated '+safe(row['calibrated_response'])+
            '; symbolic '+row['symbolic_response']+'. Reasons: '+safe(', '.join(row['reasons']) or 'none')+'.']
    outcome=result['outcome']
    lines+=['','Symbolic response: **'+outcome['symbolic_response']+'**; resolved: '+str(outcome['resolved'])+
        '; conflicting: '+str(outcome['conflicting'])+'. Reasons: '+safe(', '.join(outcome['reasons']) or 'none')+'.',
        '',safe(outcome['resolution_scope']), '', 'Modern editorial reflection: '+safe(result['reflection']['text']),
        '', '## Source-grounded procedural context']
    for rule in result['procedure']['rules']:
        lines+=['','- '+safe(rule['statement'])+' Source: '+safe(result['procedure']['source_id'])+'; '+safe(rule['locator'])+'; '+rule['id']+'.']
    lines+=['','[Author-associated procedure]('+result['sources'][0]['url']+')','',
        '## Limits','',safe(' '.join(result['limitations'])),'','No engine-observed motion or truth confidence.',
        '', '## Exact replay metadata','','```json',json.dumps(result['replay'],ensure_ascii=True,indent=2),'```','']
    return '\n'.join(lines)


def load_input(path):
    def pairs(items):
        result={}
        for k,v in items:
            if k in result:raise ValueError('Duplicate JSON key: '+k)
            result[k]=v
        return result
    def invalid(v):raise ValueError('Nonfinite JSON: '+v)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,parse_constant=invalid)


def rejection(message,fmt):
    """A rejected request has no reading/outcome;CLI exits2 in either output format."""
    if fmt=='json':return json.dumps(dict(status='rejected',error=str(message),reading=None),indent=2)
    return '# Pendulum request rejected\n\n'+html.escape(str(message))+'\n\nNo symbolic reading was produced.\n'
