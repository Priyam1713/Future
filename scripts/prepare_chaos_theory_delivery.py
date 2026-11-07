"""Prepare inherited CLI/checkout/acceptance harnesses; no numerical oracle changes."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run():
    p=R/'future/__main__.py';s=p.read_text(encoding='utf-8');anchor='    args = parser.parse_args()'
    parser="    ct=sub.add_parser('chaos-theory')\n    ct.add_argument('input',help='Bounded synthetic Lorenz63 RK4 paired trajectories JSON')\n    ct.add_argument('--format',choices=['json','markdown'],default='json')\n"
    start=s.index("    if args.command=='prediction-markets':");end=s.index("    if args.command=='collective-intelligence':",start)
    dispatch=s[start:end].replace('prediction-markets','chaos-theory').replace('prediction_markets','chaos_theory').replace('Offline LMSR play-credit request rejected','Finite Lorenz63 request rejected').replace('        from decimal import DecimalException\n','').replace(',DecimalException','')
    s=s.replace(anchor,parser+anchor+'\n'+dispatch.rstrip(),1);p.write_text(s,encoding='utf-8',newline='\n')
    for old,new in [('smoke_prediction_markets_core.py','smoke_chaos_theory_core.py'),('check_prediction_markets_checkout.py','check_chaos_theory_checkout.py'),('accept_prediction_markets_core.py','accept_chaos_theory_core.py')]:
        t=(R/'scripts'/old).read_text(encoding='utf-8').replace('prediction-markets','chaos-theory').replace('prediction_markets','chaos_theory').replace('future58-checkout-','future59-checkout-').replace('play-credit LMSR engine','Lorenz63 RK4 engine')
        if old.startswith('accept_'):
            t=t.replace('collective-intelligence-acceptance-checks.json','prediction-markets-acceptance-checks.json').replace("!= 58","!= 59").replace('(2219, 3247, 37)','(2276, 3345, 38)').replace('== 4816','== 5050').replace('inherited_tests=2144, new_tests=tests-2144','inherited_tests=2219, new_tests=tests-2219').replace('inherited_cli_cases=3113, new_cli_cases=cli-3113','inherited_cli_cases=3247, new_cli_cases=cli-3247')
        (R/'scripts'/new).write_text(t,encoding='utf-8',newline='\n')
    with (R/'README.md').open('a',encoding='utf-8') as f:f.write('\n### Technique59: finite Lorenz63 simulation\n\n`python -m future chaos-theory data/chaos-theory-cli/one-step-input.json --format markdown`\n\nClassical scalar RK4 integrates explicit synthetic initial pairs at h and h/2. Reports separate initial-condition separation from step-refinement differences. Dimensionless finite horizons; no certified Lyapunov exponent, rigorous error bound, weather skill or empirical predictability. Exact contract: `knowledge/chaos_theory_profile_v1.json`.\n')
if __name__=='__main__':run()
