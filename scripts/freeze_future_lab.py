"""Freeze the completed milestone and Lab integration preservation boundary."""
import hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def save(p,x):(R/p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def run():
    path=R/'data/future-lab-preservation-baseline.json'
    if path.exists():raise ValueError('Lab baseline already frozen')
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert head.startswith('685a329')
    assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=R,text=True)
    files={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in subprocess.check_output(['git','ls-files'],cwd=R,text=True).splitlines() if (R/p).is_file()};allowed=['README.md','PROGRESS.md']
    save(path.relative_to(R),dict(version=1,baseline_commit=head,allowed_existing_edits=allowed,pre_lab_sha256=files,protected_count=len(set(files)-set(allowed))))
    selected={p:h for p,h in files.items() if p.startswith(('knowledge/','resources/','tests/fixtures/','future/')) or p in ['data/future-final-acceptance-checks.json','data/future-54-technique-completion-matrix.json','data/future-final-summary.md']}
    save('knowledge/future_lab_source_freeze_v1.json',dict(version=1,date='2026-11-09',completed_core_commit=head,release_tag='core-v1.0.0',files=selected,inherited_acceptance=dict(tests=2402,cli_cases=3453,independent_verifiers=51),rights='All inherited source/data/kernel rights restrictions preserved; no new third-party ingestion or redistribution.',boundary='Lab integration only. No engine, frozen release, profile, fixture, inventory or resource edits. README/PROGRESS are the only existing mutable files.'))
    print(head,len(set(files)-set(allowed)),'protected files')
if __name__=='__main__':run()
