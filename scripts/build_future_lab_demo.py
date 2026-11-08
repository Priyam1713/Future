"""Produce a fully synthetic lifecycle with separate forecast and outcome commits."""
import json
from pathlib import Path
from future.lab import create,forecast,resolve,evaluate,markdown
from future.lab.common import digest
from scripts.verify_future_lab import fixture
R=Path(__file__).resolve().parents[1]
def save(p,x):(R/p).parent.mkdir(parents=True,exist_ok=True);(R/p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def run():
    f=fixture();p=f['demo_plan'];save('data/future-lab-demo/dataset.json',p['dataset']);save('data/future-lab-demo/plan.json',p);created=create(p);save('data/future-lab-demo/created-ledger.json',created);l=forecast(created,'2025-01-02T00:00:00Z');save('data/future-lab-demo/forecast-ledger.json',l)
    for o in f['demo_outcomes']:save('data/future-lab-demo/outcome-'+o['target_id']+'.json',o);l=resolve(l,o,'2025-01-11T00:00:00Z')
    save('data/future-lab-demo/final-ledger.json',l);report=evaluate(l);save('data/future-lab-demo/research-report.json',report)
    out=dict(schema_version=1,mode='synthetic',synthetic=True,empirical_skill_certified=False,lifecycle=['Registered original synthetic dataset/source/rights/vintage','Specified three target identities and a binary target definition','Froze cutoff,splits,model andbaseline before outcomes','Executed unchanged51native forecast ledger','Committed immutable forecast/output/provenance SHA','Recorded separate later synthetic outcome evidence;one explicitlymissing','Evaluated two matched cases against fixed1/2baseline','Generated deterministic JSON andMarkdown research reports','Replayed native outputs andindependentFraction knownanswers'],ledger=l,research_report=report,independent_expected=f['demo_expected'],limits='All observations,clocks andrights are synthetic declarations. No real future outcomes or measured forecasting skill are represented.')
    out['demo_sha256']=digest(out);save('data/future-lab-experiment-demo.json',out)
    (R/'data/future-lab-experiment-demo.md').write_text('# Future Lab v1 — complete synthetic experiment\n\n**SYNTHETIC: no empirical superiority claim.**\n\nThree fictional questions were frozen before their declared outcomes. One outcome is missing; two are scored on the same sample as the fixed 1/2 baseline. Model Brier is 17/50; baseline Brier is 1/4; model-minus-baseline is 9/100, so this toy model underperforms.\n\nThe JSON artifact retains the full append-only ledger, original native forecast output, hashes, separate outcome evidence and research report. Dataset, plan and intermediate forecast snapshots are in `data/future-lab-demo/`.\n\n'+markdown(report),encoding='utf-8',newline='\n')
    examples=dict(schema_version=1,source_fixture_sha256=digest(f),entries={i:dict(request=c['request'],native_output_sha256=c['native_output_sha256']) for i,c in f['native_samples'].items()},limits='Existing source-scoped/synthetic native examples,not54empiricallyvalidatedpredictions.')
    save('data/future-lab-invocation-examples.json',examples)
    print('Synthetic lifecycle complete:3planned/2matched/1missing;Brier17/50vs1/4;54native invocation examples')
if __name__=='__main__':run()
