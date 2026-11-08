"""Prepare isolated CLI and inherited delivery harnesses for the final technique."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run():
    p=R/'future/__main__.py';s=p.read_text(encoding='utf-8');anchor='    args = parser.parse_args()';parser="    mv=sub.add_parser('multiverse')\n    mv.add_argument('input',help='Educational finite exact rational editorial scenario tree JSON')\n    mv.add_argument('--format',choices=['json','markdown'],default='json')\n";start=s.index("    if args.command=='chaos-theory':");end=s.index("    if args.command=='prediction-markets':",start);dispatch=s[start:end].replace('chaos-theory','multiverse').replace('chaos_theory','multiverse').replace('Finite Lorenz63 request rejected','Finite editorial scenario request rejected');s=s.replace(anchor,parser+anchor+'\n'+dispatch.rstrip(),1);p.write_text(s,encoding='utf-8',newline='\n')
    for old,new in [('smoke_chaos_theory_core.py','smoke_multiverse_core.py'),('check_chaos_theory_checkout.py','check_multiverse_checkout.py'),('accept_chaos_theory_core.py','accept_multiverse_core.py')]:
        t=(R/'scripts'/old).read_text(encoding='utf-8')
        if old.startswith('accept_'):t=t.replace('prediction-markets-acceptance-checks.json','__PREVIOUS__')
        t=t.replace('chaos-theory','multiverse').replace('chaos_theory','multiverse').replace('future59-checkout-','future60-checkout-').replace('Lorenz63 RK4 engine','finite rational scenario engine')
        if old.startswith('accept_'):t=t.replace('__PREVIOUS__','chaos-theory-acceptance-checks.json').replace('!= 59','!= 60').replace('(2276, 3345, 38)','(2402, 3453, 39)').replace('== 5050','== 5231').replace('inherited_tests=2219, new_tests=tests-2219','inherited_tests=2276, new_tests=tests-2276').replace('inherited_cli_cases=3247, new_cli_cases=cli-3247','inherited_cli_cases=3345, new_cli_cases=cli-3345')
        (R/'scripts'/new).write_text(t,encoding='utf-8',newline='\n')
    with (R/'README.md').open('a',encoding='utf-8') as f:f.write('\n### Technique60: educational finite scenario tree\n\n`python -m future multiverse data/multiverse-cli/reference-input.json --format markdown`\n\nExact rational local weights,complete path/leaf probabilities,declared expected utility and node-event conditional queries. Editorial probabilities are separate from quantum amplitudes. No observing or forecasting other universes,Everett empirical proof or quantum-state dynamics. Contract: `knowledge/multiverse_profile_v1.json`.\n')
if __name__=='__main__':run()
