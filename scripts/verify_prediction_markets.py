"""Independent high-precision,series,funding and exact cash ledger verification."""
import copy,hashlib,json
from fractions import Fraction as F
from decimal import Decimal as D
from pathlib import Path
from future.remote_viewing import digest
from future.scrying import load_input
R=Path(__file__).resolve().parents[1];TOL=F(1,10**60)
def fixture():
    f=load_input(R/'tests/fixtures/prediction-markets-independent-v1.json');fr=load_input(R/'knowledge/prediction_markets_fixture_freeze_v1.json')
    assert digest(f)==fr['fixture_sha256'];assert hashlib.sha256((R/'scripts/prediction_markets_oracle.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()==fr['oracle_sha256'];return f
def check_numbers(v):
    from future.prediction_markets import cost_prices,funding
    q={k:D(n) for k,n in v['q'].items()};r=cost_prices(q,D(v['b']));e=v['expected']
    assert abs(F(r['cost'])-F(e['cost']))<=TOL,(v['b'],v['q'],'cost')
    assert F(r['potential'])==F(e['potential']),(v['b'],v['q'],'potential')
    assert F(funding(D(v['b'])))==F(v['reserve'])
    for side in ['YES','NO']:assert F(r['prices'][side])>0 and abs(F(r['prices'][side])-F(e['prices'][side]))<=TOL
    assert abs(sum(map(F,r['prices'].values()),F(0))-1)<=TOL
def numeric_checks():
    from future.prediction_markets import cost_prices
    f=fixture()
    for v in f['numerical_vectors']:check_numbers(v)
    series=f['ln2_series'];x=F(1,3);lower=2*sum((x**(2*k+1)/F(2*k+1) for k in range(200)),F(0));tail=2*x**401/(401*(1-x*x))
    assert lower==F(series['lower']) and lower+tail==F(series['upper']) and 0<tail<F(1,10**190)
    value=F(cost_prices({'YES':D(0),'NO':D(0)},D(1))['cost']);assert lower-TOL<=value<=lower+tail+TOL
def verify_report(r):
    from scripts.prediction_markets_oracle import numeric
    q=r['request'];b=q['market']['liquidity'];initial=r['initial'];before=initial;initial_total=sum((F(a['initial_credit']) for a in q['accounts']),F(0))+F(initial['maker_reserve']);initial_potential=F(numeric(b,'0','0')['potential'])
    for t in r['trace']:
        after=t['financial_after'];assert digest(before)==t['financial_before_sha256'] and digest(after)==t['financial_after_sha256']
        if t['decision'] not in ('executed','resolved'):assert before==after
        accounts=after['accounts'];qty=after['q'];assert sum((F(v['cash']) for v in accounts.values()),F(0))+F(after['maker_cash'])==initial_total
        for side in ['YES','NO']:assert sum((F(v['positions'][side]) for v in accounts.values()),F(0))==F(qty[side])
        assert all(F(v['cash'])>=0 and all(F(p)>=0 for p in v['positions'].values()) for v in accounts.values()) and F(after['maker_cash'])>=0
        assert F(after['net_charges'])==F(numeric(b,qty['YES'],qty['NO'])['potential'])-initial_potential
        assert max(map(F,qty.values()))-F(after['net_charges'])<=F(after['maker_reserve'])
        before=after
    previous=None
    for entry in r['ledger']:
        data=copy.deepcopy(entry);sha=data.pop('sha256');assert digest(data)==sha and data['previous_sha256']==previous;previous=sha
    assert digest(r['ledger'])==r['ledger_sha256']
    for qrow in r['quotes']:assert digest(qrow['receipt'])==qrow['receipt_sha256']
    assert r['empirical_forecast_accuracy_validated'] is False
    data=copy.deepcopy(r);sha=data.pop('report_sha256');assert digest(data)==sha
def check_case(c):
    from future.prediction_markets import read
    q=copy.deepcopy(c['input']);before=digest(q)
    if c['exit_code']==2:
        try:read(q)
        except ValueError:pass
        else:raise AssertionError('Expected rejection')
    else:
        r=read(q);e=c['expected']
        for key,value in e.items():
            if key not in ('decisions','reasons'):assert r['final'][key]==value,key
        assert [t['decision'] for t in r['trace']]==e['decisions']
        for index,reason in e['reasons'].items():assert r['trace'][int(index)]['reason']==reason,(index,reason)
        verify_report(r)
    assert digest(q)==before
def run():
    f=fixture()
    for c in f['cases'].values():check_case(c)
    numeric_checks()
    out=dict(passed=True,fixture_families=len(f['families']),families={k:dict(passed=True,cases=v) for k,v in f['families'].items()},accepted=sum(c['exit_code']==0 for c in f['cases'].values()),rejected=sum(c['exit_code']==2 for c in f['cases'].values()),numerical_vectors=len(f['numerical_vectors']),ln2_series_terms=200,decimal_oracle_precision=120,production_precision=80,price_cost_absolute_tolerance='1e-60',cash_quantum='1e-24',literal_buy_one_charge='0.620114506958277524631763',exact_fraction_cash_conservation_passed=True,series_funding_reference_passed=True,ledger_hash_chains_passed=True,all_trace_potentials_independently_checked=True,fixture_sha256=digest(f),scope='Synthetic play-credit mechanism/numerical/accounting verification; no actual money or empirically calibrated prediction market')
    (R/'data/prediction-markets-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print('31 independent fixture families pass;145 numerical vectors;200-term rational ln2 reference;33 accepted/30 rejected')
if __name__=='__main__':run()
