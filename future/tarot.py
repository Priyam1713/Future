"""Symbolic reading composition over source catalog and deterministic card draws."""
import copy
import hashlib
import html
import json
from pathlib import Path
from .card_random import PROTOCOL,seed_bytes,shuffle_pack,orientations
from .tarot_catalog import DATA,PROFILE,ORDER,CARDS,card,thaw,register_knowledge

SPREADS={'one':1,'three':3,'waite_celtic':10}


def _object(value,keys,path):
    if not isinstance(value,dict) or set(value)-set(keys):raise ValueError(path+': unknown fields or unsupported assessment inputs')


def _text(value,limit):
    if not isinstance(value,str) or not value.strip() or len(value)>limit or any(ord(c)<32 for c in value):return False
    try:value.encode('utf-8')
    except UnicodeError:return False
    return True


def validate(value):
    _object(value,['schema_version','profile','task','mode','spread','seed','protocol','orientation_policy','cards','positions','question','significator','final_card_uncertain'],'input')
    if type(value.get('schema_version')) is not int or value['schema_version']!=1:raise ValueError('schema_version must be integer1')
    if value.get('profile')!=PROFILE:raise ValueError('Unknown source profile;no Marseille,Thoth or Etteilla fallback')
    if value.get('task')!='symbolic_reading':raise ValueError('Only symbolic_reading;no factual prediction or diagnosis')
    spread=value.get('spread')
    if not isinstance(spread,str) or spread not in SPREADS:raise ValueError('Unknown spread')
    if 'question' in value and not _text(value['question'],1000):raise ValueError('Question must be nonempty plain text up to1000 characters')
    if 'positions' in value:
        p=value['positions']
        if spread!='three' or not isinstance(p,list) or len(p)!=3 or any(not _text(x,80) for x in p) or len(set(p))!=3:
            raise ValueError('Only three-card layout accepts three distinct editorial position labels')
    if spread=='waite_celtic':
        s=value.get('significator');_object(s,['card_id','facing','basis'],'significator');card(s.get('card_id'))
        if s.get('facing') not in ('left','right') or s.get('basis') not in ('matter','person_manual'):
            raise ValueError('Explicit significator facing and manual person/matter basis required;no appearance-based selection')
        court=CARDS[s['card_id']]['rank'] in ('page','knight','queen','king')
        if (s['basis']=='person_manual' and not court) or (s['basis']=='matter' and court):
            raise ValueError('Bounded Waite convention:person uses a manually chosen court;matter uses a trump or numbered card')
        if 'final_card_uncertain' in value and type(value['final_card_uncertain']) is not bool:raise ValueError('final_card_uncertain must be boolean')
    elif set(value)&{'significator','final_card_uncertain'}:raise ValueError('Significator/final-card follow-up applies only to Celtic layout')
    policy=value.get('orientation_policy')
    if value.get('mode')=='seeded':
        if 'cards' in value:raise ValueError('Do not mix manual and seeded draws')
        if value.get('protocol')!=PROTOCOL:raise ValueError('Exact supported seed protocol required;no silent version migration')
        seed_bytes(value.get('seed'))
        if policy not in ('upright_only','seeded_reversals'):raise ValueError('Unknown seeded orientation policy')
    elif value.get('mode')=='manual':
        if set(value)&{'seed','protocol'}:raise ValueError('Manual reading has no seed/protocol')
        if policy not in ('explicit','upright_only'):raise ValueError('Manual reading requires explicit or upright_only orientation policy')
        rows=value.get('cards')
        if not isinstance(rows,list) or len(rows)!=SPREADS[spread]:raise ValueError('Manual card count must match spread')
        ids=[]
        for r in rows:
            _object(r,['card_id','orientation'],'manual card');card(r.get('card_id'));ids.append(r['card_id'])
            orientation=r.get('orientation','upright' if policy=='upright_only' else None)
            if orientation not in ('upright','reversed') or (policy=='upright_only' and orientation!='upright'):raise ValueError('Invalid or conflicting manual orientation')
        if len(set(ids))!=len(ids):raise ValueError('No repeated cards within a draw')
        if spread=='waite_celtic' and value['significator']['card_id'] in ids:raise ValueError('Significator is removed and cannot be drawn again')
    else:raise ValueError('Use seeded or manual mode')
    return copy.deepcopy(value)


def _positions(request):
    if request['spread']=='waite_celtic':
        positions=thaw(DATA['celtic']['positions']);facing=request['significator']['facing']
        placement=['center_cover','crosswise_cover','above','below','right' if facing=='left' else 'left',
            facing,'staff_right_bottom','staff_right_second','staff_right_third','staff_right_top']
        for p,where in zip(positions,placement):
            p.update(placement=where,source_id=DATA['source']['id'],locator=DATA['celtic']['locator'],rule_id=DATA['celtic']['rule_id'],version=1,coverage='direct_source_layout')
        return positions
    labels=['Focus'] if request['spread']=='one' else request.get('positions',['Past','Present','Future'])
    roles=['A single symbolic focus for reflection.'] if len(labels)==1 else ['Editorial reflection position: '+s+'. A time label is a narrative frame,not evidence about actual events.' for s in labels]
    return [dict(id='position-'+str(i+1),order=i+1,label=s,role=role,placement='ordered_'+str(i+1),
        coverage='editorial_application_layout',source_id=None,locator=None,rule_id=None,version=1) for i,(s,role) in enumerate(zip(labels,roles))]


def _draw(request):
    if request['mode']=='manual':
        rows=[dict(card_id=r['card_id'],orientation=r.get('orientation','upright')) for r in request['cards']]
        return rows,dict(mode='manual',algorithm='manual-transcript-v1',cards=copy.deepcopy(rows),seed=None,
            protocol=None,significator=copy.deepcopy(request.get('significator')),physical_ritual_verified=False)
    removed=request.get('significator',{}).get('card_id')
    available=[k for k in ORDER if k!=removed]
    celtic=request['spread']=='waite_celtic'
    pack,trace=shuffle_pack(available,request['seed'],rounds=3 if celtic else 1,cut=celtic)
    orientations_=orientations(request['seed'],SPREADS[request['spread']],request['orientation_policy'])
    rows=[dict(card_id=k,orientation=o) for k,o in zip(pack,orientations_)]
    replay=dict(mode='seeded',protocol=PROTOCOL,profile=PROFILE,seed=request['seed'],seed_encoding='UTF-8 strict',normalization='none',
        canonical_order=list(ORDER),canonical_order_sha256=hashlib.sha256('\n'.join(ORDER).encode('utf-8')).hexdigest(),
        available_order=available,removed_significator=removed,significator=copy.deepcopy(request.get('significator')),
        shuffled_pack=pack,draw_count=len(rows),cards=copy.deepcopy(rows),orientation_policy=request['orientation_policy'],
        shuffle=trace,orientation_domain='orientation',deck_domain='deck',physical_ritual_verified=False,
        convention='Versioned digital adaptation,not a cryptographic-security or historical ritual claim.')
    return rows,replay


def read(value,registry=None):
    request=validate(value)
    if registry is not None:register_knowledge(registry)
    rows,replay=_draw(request);replay['request']=copy.deepcopy(request);positions=_positions(request);readings=[]
    for selected,p in zip(rows,positions):
        c=card(selected['card_id']);meaning=c['meanings'][selected['orientation']]
        base=c['meanings']['upright'] if selected['orientation']=='reversed' and any(t in meaning['text'].lower() for t in ['the same','these qualities','meaning remains unaltered']) else None
        composition='At '+p['label']+', read the source-derived motifs ('+meaning['symbolic_focus']+') through this role: '+p['role']
        warnings=list(meaning['flags'])
        if c['additional_meanings']:warnings.append('Additional section4 account retained separately;not automatically merged.')
        reflection='How could '+meaning['symbolic_focus']+' illuminate or complicate the role '+p['label']+' in a symbolic reading? Which source alternative remains unresolved?'
        readings.append(dict(card={k:c[k] for k in ['id','name','source_name','arcana','number','suit','rank','rank_number']},
            orientation=selected['orientation'],position=p,direct_component=meaning,upright_reference=base,
            additional_source_account=c['additional_meanings'],additional_account_applied=False,
            composition=dict(coverage='compositional',text=composition,reflection=reflection),
            ambiguity=warnings,qualifications=c['qualifications']))
    threads=[r['position']['label']+': '+r['direct_component']['symbolic_focus'] for r in readings]
    if request['spread']=='one':
        overview='Use '+threads[0]+' as a reflection lens. Consider its alternatives and qualifications rather than taking it as an answer about what must happen.'
    elif request['spread']=='three':
        overview='Read the sequence as a symbolic narrative: '+threads[0]+'; then '+threads[1]+'; then '+threads[2]+'. Compare what changes across the three roles;the arrangement does not establish a real past,present or future.'
    else:
        overview=('The central atmosphere ('+readings[0]['direct_component']['symbolic_focus']+') meets the crossing motif ('+readings[1]['direct_component']['symbolic_focus']+
            '). Compare the aim ('+readings[2]['direct_component']['symbolic_focus']+') with the established basis ('+readings[3]['direct_component']['symbolic_focus']+
            '),then read the passing and approaching influences in order. The right-hand staff moves from stance through environment and hopes/fears to a symbolic culmination ('+
            readings[-1]['direct_component']['symbolic_focus']+'). This is a compositional reading,not a forecast or a source-documented card-pair rule.')
    follow_up=None
    if request['spread']=='waite_celtic':
        court=readings[-1]['card']['rank'] in ('page','knight','queen','king')
        follow_up=dict(source_id=DATA['source']['id'],locator='PartIII section7,p304',
            final_court_card=court,final_uncertainty_user_selected=request.get('final_card_uncertain',False),
            option_applicable=court or request.get('final_card_uncertain',False),automatic_redraw=False,
            proposed_significator=readings[-1]['card']['id'],
            instruction='Source permits a fresh reading with final card as significator when dubious or a court card. Requires a new explicit request/seed;no automatic repeat-until-favourable behavior.')
    return dict(schema_version=1,technique_id=16,profile=PROFILE,task='symbolic_reading',mode=request['mode'],spread=request['spread'],
        question=request.get('question'),question_usage='User context only;not used to select cards or infer hidden facts.',
        significator=dict(selection=request['significator'],card=card(request['significator']['card_id']),orientation='upright',
            source_id=DATA['source']['id'],locator='PartIII section7,pp299-302',selection_method='explicit_manual_not_appearance_inference') if 'significator' in request else None,
        readings=readings,overall=dict(coverage='compositional',summary=overview,threads=threads,source_card_pair_rules_applied=False,
            conditional_source_rules='Retained in source accounts;not automatically evaluated without a verified condition/adjacency profile.'),
        follow_up=follow_up,replay=replay,source=thaw(DATA['source']),conventions=thaw(DATA['conventions']),
        celtic_procedure=thaw(DATA['celtic']) if request['spread']=='waite_celtic' else None,
        limitations=thaw(DATA['limitations'])+['Source vocabulary is documentary,not a medical finding or verified fact about any person.'],
        predictive_validity='Not established;no numerical predictive confidence or outcome probability.',factual_prediction=False)


def _md(value):return html.escape(str(value),quote=False).replace('|','&#124;').replace('\n',' ')


def markdown(report):
    lines=['# Tarot — symbolic reading','','**Symbolic interpretation;no certain prediction or diagnosis.**','',
        'Profile: '+report['profile']+'; spread: '+report['spread'],'',
        'Question/context: '+_md(report['question'] or 'Not supplied'),'',report['overall']['summary'],'',
        '| Position | Card | Orientation | Source-derived motifs |','|---|---|---|---|']
    for r in report['readings']:
        lines.append('| '+' | '.join(_md(v) for v in [r['position']['label'],r['card']['name'],r['orientation'],r['direct_component']['symbolic_focus']])+' |')
    if report['significator']:
        s=report['significator'];lines+=['','Significator: '+s['card']['name']+';facing '+s['selection']['facing']+';removed from draw.']
    for r in report['readings']:
        m=r['direct_component'];p=r['position']
        lines+=['','## '+str(p['order'])+'. '+_md(p['label'])+' — '+r['card']['name']+' ('+r['orientation']+')','',
            'Role: '+_md(p['role'])+' Placement: '+p['placement'],
            'Historical source wording (attributed;not a fact or diagnosis):','', '> '+m['text'],'',
            'Source: '+m['source_id']+'; ['+m['locator']+']('+m['page_url']+')','Rule: '+m['rule_id']+' v'+str(m['version']),
            '',r['composition']['text'],'',r['composition']['reflection']]
        if r['upright_reference']:lines+=['','Reversal refers back to upright vocabulary: '+r['upright_reference']['text']]
        if r['additional_source_account']:
            a=r['additional_source_account'];lines+=['','Separate additional account (not merged),'+a['locator']+': '+a['text']]
        lines+=['- '+w for w in r['ambiguity']]
    if report['follow_up']:lines+=['','## Source follow-up option','',report['follow_up']['instruction'],
        'Court-card trigger: '+str(report['follow_up']['final_court_card'])+'; user-marked uncertainty: '+str(report['follow_up']['final_uncertainty_user_selected'])]
    lines+=['','## Replay and limitations','', 'Mode: '+report['mode']+'; protocol: '+str(report['replay'].get('protocol'))]
    if report['mode']=='seeded':lines+=['Seed (exact Unicode): '+_md(json.dumps(report['replay']['seed'],ensure_ascii=True)),
        'Canonical deck hash: '+report['replay']['canonical_order_sha256'],'Shuffle rounds/cuts: '+str(report['replay']['shuffle'])]
    lines+=['Full pack,draw and orientations are recorded in the JSON report. No automatic redraw.']
    lines+=['- '+v for v in report['limitations']]+['',report['source']['rights_note'],'']
    return '\n'.join(lines)


def load_input(path):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('Duplicate JSON key: '+k)
            out[k]=v
        return out
    def invalid(value):raise ValueError('Nonfinite JSON: '+value)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,parse_constant=invalid)
