"""One-time pre-engine contract capture; never used by production."""
import hashlib
import json
import subprocess
from pathlib import Path

R=Path(__file__).resolve().parents[1]
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def save(p,v):(R/p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')

def run():
    baseline=R/'data/psychohistory-engine-preservation-baseline.json'
    if baseline.exists():raise ValueError('Capture is immutable; refusing replacement')
    files=subprocess.check_output(['git','ls-files'],cwd=R,text=True).splitlines()
    allowed=['PROGRESS.md','README.md','future/__main__.py','knowledge/gaps.json']
    hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in files if (R/p).is_file()}
    save(baseline,dict(baseline_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),allowed_existing_edits=allowed,pre_engine_sha256=hashes,protected_count=len(set(hashes)-set(allowed))))
    audit=json.loads((R/'knowledge/psychohistory_resource_audit.json').read_text(encoding='utf-8'))
    sources=json.loads((R/'knowledge/psychohistory_sources.json').read_text(encoding='utf-8'))
    freeze=dict(version=1,technique_id=52,audit_sha256=digest(audit),source_manifest_sha256=digest(sources),
        source_boundaries={'Asimov':'Fictional inspiration; no operational or validated population law.','Pentland':'Empirical measurement/privacy context; detailed book formulas uninspected.','Page':'Many-model comparison context; detailed book algorithms uninspected.','Watts2002':'Model Specification p5767: irreversible >= fractional activation; random asynchronous source schedule. Our synchronous finite explicit graph is editorial; no experiment/theorem replication.'},
        rights='Facts and original synthetic examples only. No source body, figure, contact data or book redistribution. SocioPatterns CC BY-NC-SA3.0 is not adopted for synthetic code. Real-data ingestion unsupported.')
    save('knowledge/psychohistory_source_freeze_v1.json',freeze)
    profile=dict(id='psychohistory-synthetic-threshold-dynamics-v1',version=1,technique_id=52,
        scope='Synthetic Population Threshold Dynamics and Scenario Simulation — Bounded Reference Scope',
        source_manifest_sha256=digest(sources),source_freeze_sha256=digest(freeze),
        schema={'root':['schema_version','profile','population','runs','rounds','trace_states','rng','scenarios','reference_scenario','provenance'],
                'profile':['id','sha256','catalog_sha256'],'population':['size','nodes'],'rng':['algorithm','seed'],
                'scenario':['id','edges','thresholds','initial'],'threshold':['node','phi'],
                'initial':['mode','probability','fixed_seeds','run_seeds','overrides'],'override':['node','state'],
                'provenance':['synthetic','source_ref','rights','attribution','snapshot','snapshot_sha256']},
        contract=['Strict exact fields; schema_version integer1. All IDs ASCII [A-Za-z0-9][A-Za-z0-9_.-]{0,63}. Nodes sorted unique; population.size matches. Scenarios unique IDs; reference must exist.',
            'Edges lexicographically sorted unique two-ID lists with u<v. Threshold rows cover nodes in their order. Exact probability strings: unsigned integer or fraction, each integer <=32digits; value0..1; no floats/bools/decimals.',
            'next_i = current_i OR (degree_i>0 AND active_neighbors_i*denominator_i >= degree_i*numerator_i). One previous-round snapshot. Activation irreversible; unseeded isolates never activate even phi0; seeded isolates persist; phi0 positive-degree nodes activate without active neighbors.',
            'Static graphs, thresholds and semantic identities. Rounds0..N are dimensionless. Include t0, append only changing states. At cap inspect one additional candidate state to distinguish fixed point from truncation. No-change candidate is not appended.',
            'Initial modes fixed, bernoulli, explicit_runs. Fixed requires null probability, empty run_seeds; bernoulli requires exact probability and empty fixed_seeds/run_seeds; explicit_runs requires null probability, empty fixed_seeds and exactly R ordered seed lists. Seed lists sorted unique known IDs. Overrides sorted unique known nodes, exact binary integer state; overrides win.',
            'xorshift32-v1 seed exact JSON integer1..4294967295. Mask32 after left13, right17, left5 XORs. Stream starts after first update. One word per run then sorted semantic node, including fixed/explicit/overridden nodes; shared table across all scenarios. Success iff word*denominator < 2**32*numerator. No draws during cascades. Endpoints0/1 exact. Stream hash commits algorithm/seed/nodes/runs/words.',
            'Per-run initial/final count/fraction; active/inactive actual trajectories; state vectors only when trace_states true, otherwise state hashes. Per-round means through cap hold final absorbing states. Persistence baseline shares initial state, never activates; gains paired per run.',
            'Exact rational means and population variance divide by R; sample variance divides by R-1 and is not_estimable for R1. Fraction variance scales by N**2. IID Bernoulli initial moments with overrides are ideal theoretical values; finite PRNG results are deterministic sample summaries and cascades correlated. Explicit runs are supplied equal-weight design, not Monte Carlo.',
            'Static scenarios share semantic draws; comparisons use scenario minus reference per run, list changed edges/thresholds/initial parameters, and report identical-configuration controls. No guaranteed CRN variance reduction, causal inference or real-world predictive validity.',
            'Provenance synthetic must be true; source_ref in frozen catalog; rights self_authored or permission_granted. Nonempty attribution/snapshot <=4000UTF8 characters with SHA256 over exact snapshot UTF8. Rights are declarations, not external certification. Unknown/empirical/causal/calendar fields reject.',
            'Preflight BEFORE words/transition execution: work=sum(R*(cap+1)*(N+2E)); count_cells=S*(2*(R+1)*(cap+1)+12*R+32); state_cells=trace*S*R*(cap+1)*N. Conservative generated count/trace-cell reservation; input echo, hashes and fixed descriptive metadata excluded. Maxima cannot freely combine.'],
        bounds={'nodes':128,'edges':2048,'runs':256,'scenarios':8,'count_cells':100000,'state_cells':10000,'work_units':10000000},
        unsupported=['Real population forecasting','Empirical calibration','Held-out predictive validation','Causal inference','Asimovian population laws','Dynamic/weighted graphs','Births/deaths/migration','Learning/adaptation','Infection/recovery','Per-contact transmission','Watts random-asynchronous experiment reproduction'],
        runtime='Python stdlib CPU, offline; no new dependencies')
    save('knowledge/psychohistory_profile_v1.json',profile)
    with (R/'PROGRESS.md').open('a',encoding='utf-8') as f:f.write('\n## 2026-11-07 — #52 frozen executable contract\n- Frozen synthetic synchronous exact-threshold profile, source/rights boundaries, strict schema, shared xorshift32 initialization and combined preflight budgets before engine code. Actual pre-engine protected count: '+str(len(set(hashes)-set(allowed)))+'. Independent fixtures follow before production.\n')
    print(digest(profile),len(set(hashes)-set(allowed)))

if __name__=='__main__':run()
