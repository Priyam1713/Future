"""Pre-engine independent Decimal120/direct-exp and Fraction cash known answers."""
import copy,hashlib,json
from decimal import Decimal as D,localcontext,ROUND_HALF_EVEN
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
R=Path(__file__).resolve().parents[1];Q=F(1,10**24)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def ds(v):
    if isinstance(v,F):
        with localcontext() as c:c.prec=120;v=D(v.numerator)/D(v.denominator)
    if not v:return '0'
    s=format(v,'f');return s.rstrip('0').rstrip('.') if '.' in s else s
def ln2_interval():
    x=F(1,3);n=200;lower=2*sum((x**(2*k+1)/F(2*k+1) for k in range(n)),F(0));tail=2*x**(2*n+1)/(F(2*n+1)*(1-x*x))
    return lower,lower+tail
LOWER,UPPER=ln2_interval()
def reserve(b):
    # Rigorous rational upper bound,independent of Decimal.ln.
    raw=(F(b)*UPPER+2*Q)/Q;ceiling=-(-raw.numerator//raw.denominator);return ceiling*Q
@lru_cache(None)
def numeric(b,y,n):
    with localcontext() as ctx:
        ctx.prec=120;bd,yd,nd=map(D,(b,y,n));a=(yd/bd).exp();c=(nd/bd).exp();s=a+c;cost=bd*s.ln();potential=cost.quantize(D('1e-24'),rounding=ROUND_HALF_EVEN)
        return dict(cost=ds(cost),potential=ds(potential),prices={'YES':ds(a/s),'NO':ds(c/s)})
def request():
    p=json.loads((R/'knowledge/prediction_markets_profile_v1.json').read_text(encoding='utf-8'));snapshot='Original fictional LMSR play-credit ledger; no actual money or traders.'
    return dict(schema_version=1,profile=dict(id=p['id'],version=1,sha256=digest(p),catalog_sha256=p['source_manifest_sha256']),market=dict(id='market1',version=1,question_id='question1',question_version=1,event_id='event1',definition='Does synthetic event1 occur?',positive_rule='YES pays1playcredit per recordedshare',negative_rule='NO pays1playcredit per recordedshare',outcomes=['YES','NO'],exhaustive=True,created_at='2025-01-01T00:00:00Z',close_at='2025-01-10T00:00:00Z',resolver='admin',liquidity='1',money_unit='play_credit'),accounts=[dict(id='alice',initial_credit='10'),dict(id='bob',initial_credit='10')],events=[],provenance=dict(synthetic=True,source_ref='prediction-markets-cost-function-v1',rights='self_authored',attribution='Future original synthetic play-credit example',snapshot=snapshot,snapshot_sha256=hashlib.sha256(snapshot.encode()).hexdigest()))
def event(kind,eid,day=2,minute=0,actor='alice',**kwargs):return dict(id=eid,type=kind,at='2025-01-'+str(day).zfill(2)+'T00:'+str(minute).zfill(2)+':00Z',actor=actor,**kwargs)
def buy(q,actor='alice',side='YES',delta='1',start=1,day=2):
    quote='quote'+str(start);q['events'] += [event('quote','e'+str(start),day,actor=actor,quote_id=quote,outcome=side,delta=delta),event('execute','e'+str(start+1),day,1,actor=actor,quote_id=quote)]
def expected(q,trades=(),settle=None,status='open',decisions=(),reasons=None):
    # Successful trades and resolution passed as explicit fixture literals,not inferred from events.
    b=q['market']['liquidity'];cash={a['id']:F(a['initial_credit']) for a in q['accounts']};positions={a:{'YES':F(0),'NO':F(0)} for a in cash};qty={'YES':F(0),'NO':F(0)};fund=reserve(b);maker=fund;charges=[]
    for actor,side,amount in trades:
        previous=F(numeric(b,ds(qty['YES']),ds(qty['NO']))['potential']);qty[side]+=F(amount);after=F(numeric(b,ds(qty['YES']),ds(qty['NO']))['potential']);charge=after-previous;charges.append(ds(charge));cash[actor]-=charge;maker+=charge;positions[actor][side]+=F(amount)
        assert cash[actor]>=0 and positions[actor][side]>=0
    net=sum(map(F,charges),F(0));paid=F(0)
    if settle:
        for actor in cash:cash[actor]+=positions[actor][settle];paid+=positions[actor][settle]
        maker-=paid
    assert maker>=0 and sum(cash.values(),F(0))+maker==sum((F(a['initial_credit']) for a in q['accounts']),F(0))+fund
    return dict(q={k:ds(v) for k,v in qty.items()},accounts={a:dict(cash=ds(cash[a]),positions={k:ds(v) for k,v in positions[a].items()}) for a in sorted(cash)},maker_cash=ds(maker),maker_reserve=ds(fund),net_charges=ds(net),total_payout=ds(paid),realized_maker_profit=ds(net-paid) if settle else None,charges=charges,executed_trades=len(trades),settlements=1 if settle else 0,settled=settle is not None,winning_outcome=settle,market_status='resolved' if settle else status,decisions=list(decisions),reasons=reasons or {})
def build():
    path=R/'tests/fixtures/prediction-markets-independent-v1.json'
    if path.exists():raise ValueError('Immutable fixture exists')
    cases={}
    def add(name,q,trades=(),settle=None,status='open',decisions=(),reasons=None,good=True):cases[name]=dict(input=q,exit_code=0 if good else 2,expected=expected(q,trades,settle,status,decisions,reasons) if good else None)
    add('initial',request())
    x=request();x['events']=[event('quote','e1',quote_id='q1',outcome='YES',delta='1')];add('quote-only',x,decisions=['quoted'])
    x=request();buy(x);add('buy-one',x,[('alice','YES','1')],decisions=['quoted','executed'])
    y=copy.deepcopy(x);buy(y,delta='-1',start=3,day=3);add('reverse',y,[('alice','YES','1'),('alice','YES','-1')],decisions=['quoted','executed','quoted','executed'])
    y=copy.deepcopy(x);buy(y,actor='bob',side='NO',start=3,day=3);add('balanced',y,[('alice','YES','1'),('bob','NO','1')],decisions=['quoted','executed','quoted','executed'])
    for side in ['YES','NO']:
        y=copy.deepcopy(x);y['events'].append(event('resolve','settle',11,actor='admin',outcome=side));add('settle-'+side.lower(),y,[('alice','YES','1')],settle=side,decisions=['quoted','executed','resolved'])
    y=copy.deepcopy(cases['balanced']['input']);y['events'].append(event('resolve','settle',11,actor='admin',outcome='YES'));add('balanced-settlement',y,[('alice','YES','1'),('bob','NO','1')],settle='YES',decisions=['quoted','executed','quoted','executed','resolved'])
    y=copy.deepcopy(x);retry=copy.deepcopy(y['events'][1]);retry['at']='2025-01-03T00:00:00Z';y['events'].append(retry);add('idempotent',y,[('alice','YES','1')],decisions=['quoted','executed','idempotent_noop'])
    y=copy.deepcopy(x);retry=copy.deepcopy(y['events'][1]);retry.update(at='2025-01-03T00:00:00Z',actor='bob');y['events'].append(retry);add('id-conflict',y,[('alice','YES','1')],decisions=['quoted','executed','rejected'],reasons={2:'intent_id_conflict'})
    y=copy.deepcopy(cases['settle-yes']['input']);retry=copy.deepcopy(y['events'][1]);retry['at']='2025-01-12T00:00:00Z';y['events'].append(retry);add('idempotent-after-settlement',y,[('alice','YES','1')],settle='YES',decisions=['quoted','executed','resolved','idempotent_noop'])
    y=copy.deepcopy(cases['settle-yes']['input']);y['events'].append(event('resolve','again',12,actor='admin',outcome='NO'));add('duplicate-resolution',y,[('alice','YES','1')],settle='YES',decisions=['quoted','executed','resolved','rejected'],reasons={3:'already_resolved'})
    y=copy.deepcopy(cases['settle-yes']['input']);retry=copy.deepcopy(y['events'][-1]);retry['at']='2025-01-12T00:00:00Z';y['events'].append(retry);add('resolution-idempotent',y,[('alice','YES','1')],settle='YES',decisions=['quoted','executed','resolved','idempotent_noop'])
    y=request();y['events']=[event('quote','a',quote_id='qa',outcome='YES',delta='1'),event('quote','b',minute=1,actor='bob',quote_id='qb',outcome='NO',delta='1'),event('execute','c',minute=2,quote_id='qa'),event('execute','d',minute=3,actor='bob',quote_id='qb')];add('stale-quote',y,[('alice','YES','1')],decisions=['quoted','quoted','executed','rejected'],reasons={3:'stale_quote'})
    y=request();y['accounts'][0]['initial_credit']='0.1';buy(y);add('budget',y,decisions=['quoted','rejected'],reasons={1:'insufficient_credit'})
    y=request();buy(y,actor='bob');buy(y,delta='-1',start=3,day=3);add('naked-short',y,[('bob','YES','1')],decisions=['quoted','executed','quoted','rejected'],reasons={3:'insufficient_position'})
    y=request();buy(y);y['events'][1]['actor']='bob';add('actor-mismatch',y,decisions=['quoted','rejected'],reasons={1:'quote_actor_mismatch'})
    y=copy.deepcopy(x);y['events'].append(event('execute','newid',3,quote_id='quote1'));add('used-quote',y,[('alice','YES','1')],decisions=['quoted','executed','rejected'],reasons={2:'quote_already_executed'})
    y=copy.deepcopy(x);y['events'].append(event('resolve','unauth',11,actor='alice',outcome='YES'));add('unauthorized-resolution',y,[('alice','YES','1')],status='closed',decisions=['quoted','executed','rejected'],reasons={2:'unauthorized'})
    y=copy.deepcopy(x);y['events'].append(event('resolve','early',3,actor='admin',outcome='YES'));add('early-resolution',y,[('alice','YES','1')],decisions=['quoted','executed','rejected'],reasons={2:'too_early'})
    y=request();y['events']=[event('quote','late',10,quote_id='q1',outcome='YES',delta='1')];add('quote-at-cutoff',y,status='closed',decisions=['rejected'],reasons={0:'market_closed'})
    y=request();buy(y);y['events'][1]['at']='2025-01-10T00:00:00Z';add('execute-at-cutoff',y,status='closed',decisions=['quoted','rejected'],reasons={1:'market_closed'})
    for name,actor,day,decision,reason in [('close','admin',10,'closed',None),('unauthorized-close','alice',10,'rejected','unauthorized'),('early-close','admin',3,'rejected','too_early')]:
        y=request();y['events']=[event('close',name,day,actor=actor)];add(name,y,status='closed' if day==10 else 'open',decisions=[decision],reasons={0:reason} if reason else None)
    y=request();y['events']=[event('execute','unknown',quote_id='noquote')];add('unknown-quote',y,decisions=['rejected'],reasons={0:'unknown_quote'})
    y=request();y['events']=[event('quote','unknown',actor='ghost',quote_id='q1',outcome='YES',delta='1')];add('unknown-actor',y,decisions=['rejected'],reasons={0:'unknown_actor'})
    y=request();y['events']=[event('quote','one',quote_id='q1',outcome='YES',delta='1'),event('quote','two',minute=1,actor='bob',quote_id='q1',outcome='NO',delta='1'),event('execute','three',minute=2,quote_id='q1')];add('duplicate-quote-id',y,[('alice','YES','1')],decisions=['quoted','rejected','executed'],reasons={1:'duplicate_quote_id'})
    for name,delta,reason in [('quantity-cap','1001','quantity_cap'),('negative-global','-1','negative_global_quantity')]:
        y=request();y['events']=[event('quote','cap',quote_id='q1',outcome='YES',delta=delta)];add(name,y,decisions=['rejected'],reasons={0:reason})
    y=request();y['accounts'][0]['initial_credit']='1000';buy(y,delta='1000');add('extreme',y,[('alice','YES','1000')],decisions=['quoted','executed'])
    for name,b,delta in [('small-b','0.01','0.01'),('large-b','1000000','1000000')]:
        y=request();y['market']['liquidity']=b;y['accounts'][0]['initial_credit']='1000000000';buy(y,delta=delta);add(name,y,[('alice','YES',delta)],decisions=['quoted','executed'])
    mutations={
     'zero-b':lambda q:q['market'].update(liquidity='0'),
     'negative-b':lambda q:q['market'].update(liquidity='-1'),
     'float-b':lambda q:q['market'].update(liquidity=1.0),
     'nan-b':lambda q:q['market'].update(liquidity='NaN'),
     'infinite-b':lambda q:q['market'].update(liquidity='Infinity'),
     'exponent-b':lambda q:q['market'].update(liquidity='1e0'),
     'too-small-b':lambda q:q['market'].update(liquidity='0.001'),
     'too-large-b':lambda q:q['market'].update(liquidity='1000001'),
     'negative-credit':lambda q:q['accounts'][0].update(initial_credit='-1'),
     'boolean-credit':lambda q:q['accounts'][0].update(initial_credit=True),
     'duplicate-account':lambda q:q['accounts'].append(copy.deepcopy(q['accounts'][0])),
     'unsupported-outcomes':lambda q:q['market'].update(outcomes=['YES','NO','MAYBE']),
     'nonexhaustive':lambda q:q['market'].update(exhaustive=False),
     'real-money-unit':lambda q:q['market'].update(money_unit='USD'),
     'bad-market-chronology':lambda q:q['market'].update(close_at='2024-01-01T00:00:00Z'),
     'empirical':lambda q:q['provenance'].update(synthetic=False),
     'rights':lambda q:q['provenance'].update(rights='unknown'),
     'source':lambda q:q['provenance'].update(source_ref='unknown'),
     'snapshot':lambda q:q['provenance'].update(snapshot_sha256='0'*64),
     'profile':lambda q:q['profile'].update(sha256='0'*64),
     'extra-field':lambda q:q.update(external_exchange=True),
     'account-cap':lambda q:q.update(accounts=[dict(id='a'+str(i),initial_credit='0') for i in range(9)]),
     'event-cap':lambda q:q.update(events=[event('close','many',10,actor='admin')]*513)}
    for name,change in mutations.items():y=request();change(y);add(name,y,good=False)
    for name,delta in [('zero-delta','0'),('fine-delta','0.000000001'),('negative-zero','-0'),('float-delta',1.0)]:
        y=request();y['events']=[event('quote','bad',quote_id='q1',outcome='YES',delta=delta)];add(name,y,good=False)
    y=request();buy(y);y['events'][0]['at']='2025-01-03T00:00:00Z';add('event-time-order',y,good=False)
    y=request();y['events']=[event('close','early',1,actor='admin')];y['events'][0]['at']='2024-01-01T00:00:00Z';add('before-created',y,good=False)
    y=request();y['events']=[dict(id='bad',type='deposit',at='2025-01-02T00:00:00Z',actor='alice')];add('unsupported-action',y,good=False)
    points={('1',str(y),str(n)) for y in range(11) for n in range(11)}
    for b in ['0.01','1','2.5','1000000']:
        for y,n in [(0,0),(1,0),(0,1),(10,10),(1000,0),(0,1000),(1000,1000)]:points.add((b,ds(F(b)*y),ds(F(b)*n)))
    vectors=[dict(b=b,q={'YES':y,'NO':n},expected=numeric(b,y,n),reserve=ds(reserve(b))) for b,y,n in sorted(points)]
    assert abs(F(numeric('1','0','0')['cost'])-LOWER)<F(1,10**118)
    assert cases['buy-one']['expected']['charges']==['0.620114506958277524631763']
    assert cases['reverse']['expected']['net_charges']=='0' and cases['balanced-settlement']['expected']['realized_maker_profit']=='0'
    families={'initial-half-prices':['initial'],'positive-normalized-prices':['numeric-vectors'],'positive-liquidity':['zero-b','negative-b'],'stable-extreme-pricing':['extreme','numeric-vectors'],'monotone-buy':['buy-one'],'cost-difference-charge':['buy-one'],'quantized-potential-accounting':['buy-one','balanced'],'buy-sell-reversal':['reverse'],'balanced-shares':['balanced-settlement'],'common-shift-invariance':['numeric-vectors'],'cash-conservation':['settle-yes','settle-no'],'funding-reserve':['numeric-vectors'],'maker-loss-bound':['extreme','settle-yes'],'budget-refusal':['budget'],'no-naked-short':['naked-short'],'positions-equal-quantities':['balanced'],'stale-quote-refusal':['stale-quote'],'quote-no-execution':['quote-only'],'quote-actor-match':['actor-mismatch'],'idempotent-retry':['idempotent','idempotent-after-settlement'],'trade-id-conflict':['id-conflict'],'event-time-order':['event-time-order'],'close-cutoff-refusal':['quote-at-cutoff','execute-at-cutoff'],'authorized-resolution':['unauthorized-resolution','early-resolution'],'deterministic-settlement':['settle-yes','settle-no'],'duplicate-resolution':['duplicate-resolution','resolution-idempotent'],'ordered-ledger-replay':['balanced-settlement'],'strict-schema':['unsupported-action','extra-field'],'source-rights':['empirical','rights','source','snapshot'],'resource-bounds':['quantity-cap','account-cap','event-cap'],'raw-json-markdown-replay':['profile','buy-one']}
    out=dict(version=1,technique_id=58,profile_sha256=request()['profile']['sha256'],families=families,cases=cases,numerical_vectors=vectors,ln2_series=dict(terms=200,x='1/3',lower=str(LOWER),upper=str(UPPER),method='ln2=2sum x^(2k+1)/(2k+1),x=1/3;positive omitted tail<=2*x^(401)/(401*(1-x*x));exact Fraction bounds independent of Decimal.ln'),independence='Created before production; direct exp/log Decimal120 versus planned stable max-shift80. Successful trades/resolution are explicit literals,not inferred by an event handler; cash grid ledger uses exact Fraction arithmetic and funding from convergent-series upper bound.')
    path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n');freeze=dict(version=1,fixture_sha256=digest(out),oracle_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),fixture_families=len(families),numerical_vectors=len(vectors),ln2_series_terms=200,accepted=sum(c['exit_code']==0 for c in cases.values()),rejected=sum(c['exit_code']==2 for c in cases.values()),literal_buy_one_charge='0.620114506958277524631763',cash_quantum='1e-24',price_cost_tolerance='1e-60')
    (R/'knowledge/prediction_markets_fixture_freeze_v1.json').write_text(json.dumps(freeze,indent=2)+'\n',encoding='utf-8',newline='\n');print(freeze)
if __name__=='__main__':build()
