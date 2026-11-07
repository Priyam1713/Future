"""Offline fixed-b binary LMSR play-credit ledger; no real trading services."""
import copy,hashlib,json,re
from decimal import Decimal as D,Context,localcontext,ROUND_HALF_EVEN,ROUND_CEILING,FloatOperation,InvalidOperation,DivisionByZero,Overflow
from pathlib import Path
from .remote_viewing import digest,obj,identifier,integer,text,timestamp
from .scrying import load_input,freeze
ROOT=Path(__file__).resolve().parents[1]
PROFILE_HASH='d36cca55bf080adabc57d6190820812802ec4386ffe5199676a6ef0b17aad000'
CONTEXT=Context(prec=80,rounding=ROUND_HALF_EVEN,Emin=-999999,Emax=999999,capitals=1,clamp=0,flags=[],traps=[InvalidOperation,DivisionByZero,Overflow,FloatOperation])
QUANTUM=D('1e-24');TOLERANCE=D('1e-60');SIDES=('YES','NO')
def assets():
    p=load_input(ROOT/'knowledge/prediction_markets_profile_v1.json')
    if digest(p)!=PROFILE_HASH:raise ValueError('Pinned play-market profile mismatch')
    for name,key in [('prediction_markets_sources.json','source_manifest_sha256'),('prediction_markets_source_freeze_v1.json','source_freeze_sha256')]:
        if digest(load_input(ROOT/'knowledge'/name))!=p[key]:raise ValueError('Pinned source integrity mismatch')
    return p
DATA=freeze(assets())
def fields(v,key):obj(v,DATA['schema'][key])
def seq(v,limit):
    if not isinstance(v,list) or len(v)>limit:raise ValueError('Bounded list required')
    return v
def ds(v):
    if not v:return '0'
    s=format(v,'f');return s.rstrip('0').rstrip('.') if '.' in s else s
def decimal(v,places):
    if not isinstance(v,str) or re.fullmatch(r'-?(?:0|[1-9][0-9]{0,9})(?:\.[0-9]{1,'+str(places)+r'})?',v) is None:raise ValueError('Bounded decimal string required')
    value=D(v)
    if not value.is_finite() or value==0 and value.is_signed():raise ValueError('Finite canonical decimal required')
    return value
def at(v):
    if not isinstance(v,str) or not v.endswith('Z'):raise ValueError('UTC-Z timestamp required')
    return timestamp(v)
def nonempty(v):
    if not text(v,4000).strip():raise ValueError('Nonempty bounded text required')
def cost_prices(q,b):
    """Stable max-shift; each positive softmax numerator evaluated separately."""
    with localcontext(CONTEXT):
        if not isinstance(b,D) or not b.is_finite() or not D('0.01')<=b<=D('1000000'):raise ValueError('Bounded positive liquidity required')
        if set(q)!=set(SIDES) or any(not isinstance(v,D) or not v.is_finite() or not 0<=v<=1000*b for v in q.values()):raise ValueError('Bounded nonnegative quantities required')
        high=max(q.values());terms={s:((q[s]-high)/b).exp() for s in SIDES};den=sum(terms.values(),D(0));cost=high+b*den.ln();prices={s:terms[s]/den for s in SIDES}
        if any(p<=0 for p in prices.values()) or abs(sum(prices.values(),D(0))-1)>TOLERANCE:raise ValueError('Numerical price normalization failed')
        return dict(cost=cost,potential=cost.quantize(QUANTUM,rounding=ROUND_HALF_EVEN),prices=prices)
def funding(b):
    with localcontext(CONTEXT):return (b*D(2).ln()+2*QUANTUM).quantize(QUANTUM,rounding=ROUND_CEILING)
def validate(q):
    fields(q,'root');integer(q['schema_version'],1,1);fields(q['profile'],'profile');integer(q['profile']['version'],1,1)
    if q['profile']!=dict(id=DATA['id'],version=1,sha256=PROFILE_HASH,catalog_sha256=DATA['source_manifest_sha256']):raise ValueError('Profile identity mismatch')
    m=q['market'];fields(m,'market')
    for key in ('id','question_id','event_id','resolver'):identifier(m[key])
    integer(m['version'],1,1);integer(m['question_version'],1,1)
    if m['outcomes']!=list(SIDES) or m['exhaustive'] is not True or m['money_unit']!='play_credit':raise ValueError('Only exhaustive binary YES/NO play-credit markets supported')
    for key in ('definition','positive_rule','negative_rule'):nonempty(m[key])
    created,close=at(m['created_at']),at(m['close_at'])
    if created>=close:raise ValueError('Creation must precede close')
    b=decimal(m['liquidity'],8)
    if not D('0.01')<=b<=D('1000000'):raise ValueError('Liquidity outside supported positive bounds')
    accounts=seq(q['accounts'],8);events=seq(q['events'],512)
    if not accounts:raise ValueError('At least one account required')
    balances={}
    for a in accounts:
        fields(a,'account');identifier(a['id']);credit=decimal(a['initial_credit'],24)
        if a['id'] in balances:raise ValueError('Duplicate account identity')
        if not 0<=credit<=D('1000000000'):raise ValueError('Bounded nonnegative initial play credit required')
        balances[a['id']]=credit
    previous=created
    for e in events:
        if not isinstance(e,dict) or e.get('type') not in ('quote','execute','close','resolve'):raise ValueError('Unsupported play-market action')
        fields(e,e['type'])
        for key in ('id','actor'):identifier(e[key])
        delivery=at(e['at'])
        if delivery<previous:raise ValueError('Event delivery times must be nondecreasing after creation')
        previous=delivery
        if e['type'] in ('quote','execute'):identifier(e['quote_id'])
        if e['type'] in ('quote','resolve') and e['outcome'] not in SIDES:raise ValueError('Unknown binary outcome')
        if e['type']=='quote':
            delta=decimal(e['delta'],8)
            if not delta or abs(delta)>D('1000000000'):raise ValueError('Nonzero bounded share delta required')
    p=q['provenance'];fields(p,'provenance')
    if p['synthetic'] is not True or p['rights']!='self_authored':raise ValueError('Self-authored synthetic play records required')
    if p['source_ref'] not in [s['id'] for s in load_input(ROOT/'knowledge/prediction_markets_sources.json')]:raise ValueError('Unknown source')
    nonempty(p['attribution']);nonempty(p['snapshot'])
    if p['snapshot_sha256']!=hashlib.sha256(p['snapshot'].encode()).hexdigest():raise ValueError('Snapshot hash mismatch')
    budget=dict(work=len(events)*(64+len(accounts)*16),returned_cells=len(events)*(64+len(accounts)*8)+len(accounts)*32)
    for k,v in budget.items():
        if v>DATA['bounds'][k]:raise ValueError('Combined '+k+' cap exceeded')
    return b,balances,close,budget
def finance(state):
    return dict(q={s:ds(state['q'][s]) for s in SIDES},accounts={a:dict(cash=ds(v['cash']),positions={s:ds(v['positions'][s]) for s in SIDES}) for a,v in sorted(state['accounts'].items())},maker_cash=ds(state['maker_cash']),maker_reserve=ds(state['reserve']),net_charges=ds(state['net_charges']),total_payout=ds(state['total_payout']))
def invariants(state,b,initial_total,initial_potential):
    users=state['accounts'];q=state['q'];total=sum((v['cash'] for v in users.values()),D(0))+state['maker_cash']
    if total!=initial_total or state['maker_cash']<0 or any(v['cash']<0 or any(p<0 for p in v['positions'].values()) for v in users.values()):raise ValueError('Play cash conservation/nonnegative balance invariant failed')
    if any(sum((v['positions'][s] for v in users.values()),D(0))!=q[s] for s in SIDES):raise ValueError('Position/quantity invariant failed')
    if state['maker_cash']!=state['reserve']+state['net_charges']-state['total_payout']:raise ValueError('Maker cash identity failed')
    if state['net_charges']!=cost_prices(q,b)['potential']-initial_potential:raise ValueError('Rounded potential telescoping invariant failed')
    if max(q.values())-state['net_charges']>state['reserve']:raise ValueError('Funded maker loss bound failed')
    if state['settled']:
        if state['status']!='resolved' or state['total_payout']!=q[state['winner']]:raise ValueError('Settlement identity failed')
    elif state['total_payout']!=0:raise ValueError('Unsettled payout invariant failed')
def append_entry(state,ledger,entry):
    entry=dict(entry,index=len(ledger)+1,previous_sha256=ledger[-1]['sha256'] if ledger else None,economic_revision=state['revision']);entry['sha256']=digest(entry);ledger.append(entry);return entry['sha256']
def run_actions(q,b,balances,close):
    reserve=funding(b);state=dict(q={s:D(0) for s in SIDES},accounts={a:dict(cash=v,positions={s:D(0) for s in SIDES}) for a,v in sorted(balances.items())},maker_cash=reserve,reserve=reserve,net_charges=D(0),total_payout=D(0),status='open',settled=False,winner=None,revision=0)
    initial=finance(state);initial_total=sum(balances.values(),D(0))+reserve;initial_potential=cost_prices(state['q'],b)['potential'];quotes={};used=set();seen={};ledger=[];trace=[]
    def reject(reason):return dict(decision='rejected',reason=reason,data=None)
    def handle(e):
        kind=e['type'];actor=e['actor']
        if kind in ('quote','execute'):
            if state['status']!='open':return reject('market_closed')
            qid=e['quote_id']
            if kind=='quote':
                if actor not in state['accounts']:return reject('unknown_actor')
                if qid in quotes:return reject('duplicate_quote_id')
                delta=decimal(e['delta'],8);side=e['outcome'];newq=dict(state['q']);newq[side]+=delta
                if any(v<0 for v in newq.values()):return reject('negative_global_quantity')
                if any(v>1000*b for v in newq.values()):return reject('quantity_cap')
                old=cost_prices(state['q'],b);new=cost_prices(newq,b);charge=new['potential']-old['potential'];problems=[];account=state['accounts'][actor]
                if account['positions'][side]+delta<0:problems.append('insufficient_position')
                if account['cash']-charge<0:problems.append('insufficient_credit')
                if state['maker_cash']+charge<0:problems.append('maker_funding')
                receipt=dict(id=qid,actor=actor,outcome=side,delta=ds(delta),created_at=e['at'],economic_revision=state['revision'],q_before={s:ds(state['q'][s]) for s in SIDES},q_after={s:ds(newq[s]) for s in SIDES},potential_before=ds(old['potential']),potential_after=ds(new['potential']),charge=ds(charge),modeled_prices_before={s:ds(old['prices'][s]) for s in SIDES},modeled_prices_after={s:ds(new['prices'][s]) for s in SIDES},executable_now=not problems,feasibility_reasons=problems)
                quotes[qid]=receipt;return dict(decision='quoted',reason=None,data=dict(receipt=copy.deepcopy(receipt),receipt_sha256=digest(receipt)))
            if qid not in quotes:return reject('unknown_quote')
            quote=quotes[qid]
            if actor!=quote['actor']:return reject('quote_actor_mismatch')
            if qid in used:return reject('quote_already_executed')
            if quote['economic_revision']!=state['revision']:return reject('stale_quote')
            delta=D(quote['delta']);side=quote['outcome'];account=state['accounts'][actor];newq=dict(state['q']);newq[side]+=delta;charge=D(quote['charge'])
            if account['positions'][side]+delta<0:return reject('insufficient_position')
            if any(v<0 for v in newq.values()):return reject('negative_global_quantity')
            if any(v>1000*b for v in newq.values()):return reject('quantity_cap')
            if account['cash']-charge<0:return reject('insufficient_credit')
            if state['maker_cash']+charge<0:return reject('maker_funding')
            old=finance(state);account['cash']-=charge;account['positions'][side]+=delta;state['q']=newq;state['maker_cash']+=charge;state['net_charges']+=charge;state['revision']+=1;used.add(qid)
            entry_hash=append_entry(state,ledger,dict(kind='trade',event_id=e['id'],at=e['at'],actor=actor,quote_id=qid,quote_sha256=digest(quote),outcome=side,delta=ds(delta),charge=ds(charge),potential_before=quote['potential_before'],potential_after=quote['potential_after'],q_before=old['q'],q_after={s:ds(newq[s]) for s in SIDES},actor_cash_before=old['accounts'][actor]['cash'],actor_cash_after=ds(account['cash']),maker_cash_before=old['maker_cash'],maker_cash_after=ds(state['maker_cash'])))
            return dict(decision='executed',reason=None,data=dict(ledger_entry_sha256=entry_hash,charge=ds(charge)))
        if actor!=q['market']['resolver']:return reject('unauthorized')
        if at(e['at'])<close:return reject('too_early')
        if state['settled']:return reject('already_resolved')
        if kind=='close':return dict(decision='closed',reason=None,data=dict(authorization='Declared resolver ID equality only'))
        side=e['outcome'];payouts={a:v['positions'][side] for a,v in sorted(state['accounts'].items())};paid=sum(payouts.values(),D(0))
        if paid>state['maker_cash']:return reject('maker_funding')
        old=finance(state)
        for a,amount in payouts.items():state['accounts'][a]['cash']+=amount
        state['maker_cash']-=paid;state['total_payout']=paid;state['winner']=side;state['settled']=True;state['status']='resolved';state['revision']+=1
        entry_hash=append_entry(state,ledger,dict(kind='settlement',event_id=e['id'],at=e['at'],actor=actor,outcome=side,payouts={a:ds(v) for a,v in payouts.items()},total_payout=ds(paid),maker_cash_before=old['maker_cash'],maker_cash_after=ds(state['maker_cash']),authorization='Declared resolver ID equality; not external authentication'))
        return dict(decision='resolved',reason=None,data=dict(ledger_entry_sha256=entry_hash,total_payout=ds(paid),winning_outcome=side))
    invariants(state,b,initial_total,initial_potential)
    for index,e in enumerate(q['events']):
        before=finance(state);clock_closed=False
        if state['status']=='open' and at(e['at'])>=close:state['status']='closed';state['revision']+=1;clock_closed=True
        intent=digest({k:v for k,v in e.items() if k!='at'})
        if e['id'] in seen:
            old=seen[e['id']]
            result=dict(decision='idempotent_noop',reason=None,data=dict(original_decision=old['decision'],original_reason=old['reason'])) if old['intent']==intent else reject('intent_id_conflict')
        else:
            result=handle(e);seen[e['id']]=dict(intent=intent,decision=result['decision'],reason=result['reason'])
        invariants(state,b,initial_total,initial_potential);after=finance(state)
        if result['decision'] not in ('executed','resolved') and before!=after:raise ValueError('Non-execution changed financial state')
        trace.append(dict(index=index,event=copy.deepcopy(e),intent_sha256=intent,**result,clock_closed=clock_closed,market_status_after=state['status'],economic_revision_after=state['revision'],financial_before_sha256=digest(before),financial_after_sha256=digest(after),financial_after=after))
    final_calc=cost_prices(state['q'],b);final=finance(state);trade_entries=[e for e in ledger if e['kind']=='trade']
    final.update(market_status=state['status'],winning_outcome=state['winner'],settled=state['settled'],economic_revision=state['revision'],executed_trades=len(trade_entries),settlements=sum(e['kind']=='settlement' for e in ledger),charges=[e['charge'] for e in trade_entries],realized_maker_profit=ds(state['net_charges']-state['total_payout']) if state['settled'] else None,remaining_payout_liability='0' if state['settled'] else ds(max(state['q'].values())),ideal_loss_bound_approx=ds(b*D(2).ln()),funded_loss_bound=ds(reserve),worst_modeled_loss_before_settlement=ds(max(state['q'].values())-state['net_charges']),raw_cost_approx=ds(final_calc['cost']),rounded_cost_potential=ds(final_calc['potential']),modeled_prices={s:ds(final_calc['prices'][s]) for s in SIDES},price_scope='Historical model diagnostics; not executable after market close/resolution')
    return initial,final,trace,ledger,[dict(receipt=v,receipt_sha256=digest(v),used=k in used) for k,v in sorted(quotes.items())]
def read(request,registry=None):
    q=copy.deepcopy(request)
    with localcontext(CONTEXT):
        b,balances,close,budget=validate(q);initial,final,trace,ledger,quotes=run_actions(q,b,balances,close)
        sources=load_input(ROOT/'knowledge/prediction_markets_sources.json')
        if registry is not None:
            for source in sources:registry.add_source(source)
        result=dict(status='accepted',technique_id=58,schema_version=1,profile=q['profile'],request=q,input_sha256=digest(q),market_sha256=digest(q['market']),initial_accounts_sha256=digest(sorted(q['accounts'],key=lambda a:a['id'])),schema_sha256=digest(dict(DATA['schema'])),source_manifest_sha256=DATA['source_manifest_sha256'],source_freeze_sha256=DATA['source_freeze_sha256'],code_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),initial=initial,final=final,trace=trace,ledger=ledger,ledger_sha256=digest(ledger),quotes=quotes,budget=budget,numerics=dict(DATA['numeric']),invariants=dict(cash_conservation=True,nonnegative_balances_positions=True,positions_equal_quantities=True,quantized_potential_telescoping=True,funded_maker_bound=True,one_time_settlement=True,scope='Exact finite decimal cash-grid accounting; ln/exp prices/costs are finite-precision approximations'),counters=dict(actions=len(trace),quotes=len(quotes),executed_trades=final['executed_trades'],settlements=final['settlements'],rejected_actions=sum(t['decision']=='rejected' for t in trace),idempotent_replays=sum(t['decision']=='idempotent_noop' for t in trace)),sources=sources,empirical_forecast_accuracy_validated=False,limitations=list(DATA['configuration_matrix']['unsupported'])+['Synthetic play credits only; no deposits,trading or external settlement occur.','Actor/authority/clock/rights declarations are not external authentication or consent certification.','Quantized total potentials telescope exactly on the cash grid; transcendental functions are not exact rational calculations.','Local owner can rewrite all history; retain external anchors for independent immutability assurance.','Trades use strict-before-close timing,not51/57inclusive forecast cutoff semantics.'])
        result['report_sha256']=digest(result);return result
def markdown(result):
    body=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False);fence='`'*max(3,1+max([len(x) for x in re.findall(r'`+',body)]+[0]))
    return '# Prediction markets — offline binary LMSR play credits\n\n'+fence+'json\n'+body+'\n'+fence+'\n'
