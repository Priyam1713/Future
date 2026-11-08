"""Reconcile original IDs with authoritative bounded releases, not filename counts."""
import hashlib,json,re,subprocess
from pathlib import Path
from future.scrying import load_input
from future.remote_viewing import digest
R=Path(__file__).resolve().parents[1]
EXCLUDED=[25,27,41,42,47,48]
CLI={1:['natal','forecast','progressions','doctrines','profections','solar-return','election','releasing'],2:['jyotish'],3:['bazi'],5:['horary'],6:['mundane-ingress','mundane-cycle'],9:['face-reference'],10:['phrenology-reference'],11:['moleosophy-reference'],12:['podomancy-reference'],13:['graphology-reference'],14:['aura-reference'],15:['iridology-reference'],22:['mirror-scrying'],26:['akashic-reference'],29:['coffee-reading']}
def save(p,x):(R/p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def texts(x):
    if isinstance(x,str):return [x]
    if isinstance(x,list):return [s for v in x for s in texts(v)]
    if isinstance(x,dict):return [s for v in x.values() for s in texts(v)]
    return []
def core_records():
    records={}
    for path in sorted((R/'knowledge').glob('*core_v1.json')):
        value=load_input(path)
        if 'technique_id' not in value:continue
        i=value['technique_id'];assert i not in records,('Duplicate releaseID',i);records[i]=(path,value)
    path=R/'knowledge/horary_engine_v1.json';value=load_input(path);assert value['technique_id']==5 and 5 not in records;records[5]=(path,value)
    return records
def run():
    inventory=load_input(R/'knowledge/inventory.json');sheets=inventory['sheets'];methods={r[0]:r for r in sheets['60 Methods'] if r and type(r[0]) is int and 1<=r[0]<=60};assert sorted(methods)==list(range(1,61));gaps=load_input(R/'knowledge/gaps.json');bygap={g['technique_id']:g for g in gaps};retained=[i for i in methods if bygap[i]['retained']];assert len(retained)==54 and sorted(set(methods)-set(retained))==EXCLUDED
    records=core_records();assert sorted(records)==sorted(retained)
    parsers=set(re.findall(r"add_parser\('([^']+)'",(R/'future/__main__.py').read_text(encoding='utf-8')));rows=[];per_backlog=[];source_ids=set()
    for path in (R/'knowledge').glob('*sources.json'):
        data=load_input(path)
        if isinstance(data,list):source_ids.update(x['id'] for x in data if isinstance(x,dict) and 'id' in x)
    embedded=[]
    for path in (R/'knowledge').glob('*.json'):
        data=load_input(path)
        if isinstance(data,dict) and isinstance(data.get('source'),dict) and 'id' in data['source']:
            assert data['source']['id'] in source_ids,(path,data['source']['id']);embedded.append(dict(path=path.relative_to(R).as_posix(),source_id=data['source']['id']))
    for i in retained:
        path,c=records[i];g=bygap[i];assert g['name']==methods[i][2] and c['status'].startswith('Core v1 Ready'),(i,g['status'],c['status'])
        stem=path.stem.removesuffix('_core_v1');stem='horary' if i==5 else stem;commands=CLI.get(i,[stem.replace('_','-')]);assert set(commands)<=parsers,(i,commands)
        profile=c.get('profile',c.get('algorithm_profiles'))
        kind='named_algorithm_profile'
        if i==1:profile=c['release'];kind='release_identifier; multiple named configurations in supported scope'
        if i==3:profile=sorted(c['supported']['profiles']);kind='three named clock profiles'
        assert profile is not None
        catalogs=['knowledge/'+stem+'_sources.json']
        if i==1:catalogs=['knowledge/sources.json','knowledge/doctrine_sources.json']
        if i==5:catalogs=['knowledge/sources.json','knowledge/horary_lilly_v1.json']
        assert all((R/p).is_file() for p in catalogs)
        supported=c.get('configuration_matrix',{}).get('supported',c.get('supported',c.get('certification_scope',c['status'])))
        limits={k:c[k] for k in ['unsupported','experimental','scientific_limits','statistical_limits','scope_limits','limitations','source_limits','meaning','metric_limits','rights','licensing'] if k in c}
        if 'configuration_matrix' in c:limits['configuration_matrix']=c['configuration_matrix']
        if i==5:assert c['judgment_certified'] is False;limits.update(judgment_certified=False,judgment_status=c['judgment_status'])
        backlog=c.get('backlog',{k:c[k] for k in ['P1','P2'] if k in c})
        if i==1:backlog=load_input(R/'knowledge/western_refinement_backlog.json')
        if not backlog:backlog=dict(unprioritized_legacy_items=g['gaps'],note='Original legacy wording preserved; grouped final priorities are separate editorial scheduling guidance.')
        refs=sorted(set(s for s in texts(c) if s.startswith(('data/','knowledge/','tests/','scripts/')) and (R/s).is_file()))
        verify='scripts/verify_'+stem+'.py';smoke='scripts/smoke_'+stem+'_core.py'
        if i==5:smoke='scripts/smoke_horary.py'
        if i==3:smoke='scripts/smoke_chinese_core.py'
        assert (R/smoke).is_file(),(i,smoke)
        evidence=dict(authoritative_release_sha256=digest(c),existing_evidence_paths=refs,release_verification={k:c[k] for k in ['acceptance','verification','acceptance_evidence','verification_evidence','acceptance_criteria_results'] if k in c},smoke_script=smoke,current_final_acceptance='data/future-final-acceptance-checks.json',independent_verifier=verify if (R/verify).is_file() else None)
        variations=[r for r in sheets['Variations'] if r and r[0]==i];ranks=[r for r in sheets['Ranked Sources'] if r and r[0]==i];assert len(variations)==g['variation_count'] and len(ranks)==g['source_count']
        entry=dict(technique_id=i,name=methods[i][2],release_name=c.get('name',methods[i][2]),release_status=c['status'],profile_identifier=profile,profile_identifier_kind=kind,profile_sha256=c.get('profile_sha256'),supported_scope=supported,core_record=path.relative_to(R).as_posix(),cli_commands=commands,source_catalogs=catalogs,original_method_row=methods[i],original_variation_rows=variations,original_ranked_source_rows=ranks,verification_evidence=evidence,backlog=backlog,limitations=limits)
        rows.append(entry);per_backlog.append(dict(technique_id=i,name=methods[i][2],source_record=entry['core_record'],items=backlog))
    discrepancies=[dict(technique_id=i,index_status=bygap[i]['status'],authoritative_status=records[i][1]['status']) for i in retained if bygap[i]['status']!=records[i][1]['status']]
    out=dict(version=1,date='2026-11-08',inventory_reconciled=True,status_index_discrepancies=discrepancies,inventory_sha256=digest(inventory),original_workbook_sha256=inventory['source_sha256'],total_inventory_ids=60,retained_count=54,completed_bounded_core_count=len(rows),excluded_ids=EXCLUDED,excluded=[dict(technique_id=i,name=methods[i][2],original_method_row=methods[i],core_record=None,retained=False) for i in EXCLUDED],retained=rows,embedded_source_references=embedded,aggregate_phase_record_not_counted='knowledge/phase3_core_v1.json',horary_index_reconciliation='data/future-gap-index-reconciliation.json',completion_meaning='Bounded software Corev1 readiness;not exhaustive variations,scientific validation,personal assessment orsupernaturalprediction.')
    save('data/future-54-technique-completion-matrix.json',out)
    groups=[
      dict(priority='P1',group='Scientific/empirical validation',value='Highest before broader accuracy claims',correctness_risk='High if software verification ispresentedasempiricalproof',effort='High;requiresindependentdata/protocols',actions=['Preregister held-out scoring,matched baselines andinformation-availability rules beforeclaimingskill','Keep historical/appearance/speculative cores inreference scopes;validateeach advertised empiricaluse separately'],technique_ids=retained),
      dict(priority='P1',group='Missing source access and rights',value='High;unblocks defensible rules anddistribution',correctness_risk='High',effort='Medium/high depending onpermissions',actions=['Obtain permitted edition-specific passages andresolveprovisionalvariationlocators','Retain existinglicense/kernel/data notices anddistributionrestrictions;readingaccessisnotredistributionpermission'],technique_ids=retained),
      dict(priority='P1',group='Real dataset ingestion',value='High forforecasting research',correctness_risk='High;leakage/rights/vintage',effort='High',actions=['Freeze lawful datasets,units,identities,timestamps andsourcevintages','Prioritize50independentforecastdatasets onlywhenmatchedcontrols andtrain/testavailabilitycanbepreserved'],technique_ids=[43,44,45,46,49,51,53,55,56,57,58,59]),
      dict(priority='P1/P2',group='Advanced mathematical extensions',value='Medium/high onlyafterindependentanchors',correctness_risk='High if scopeexpanded prematurely',effort='High',actions=['Prioritize source-boundedjudgmentidentification,numericalerror andcausalassumption gapsbeforeparameterexpansion','Keepgeneraldo-calculus,advancedEEG/quantum/Lyapunov/reservoir/marketmodels separate versionedprofiles'],technique_ids=[1,2,3,5,6,7,49,50,51,52,53,54,55,56,57,58,59,60]),
      dict(priority='P1/P2',group='Historical/source variation expansion',value='Medium;selected practicaltraditions',correctness_risk='High if conflictingconventionsaremerged',effort='Medium/high',actions=['Resolve mostuseful directsourcecomponents andpublish workedexamples','Retain exactinventorynames,traditionseparation andunsupportedlabels;deferobscurevariations'],technique_ids=[i for i in retained if i<=46]),
      dict(priority='P2',group='Cross-engine integrations',value='Medium;onlywithreal sharedusecase',correctness_risk='High at semanticboundaries',effort='Medium/high',actions=['Use sevencompatibilitywitnesses todesignexplicitfuturemappings','Reconcilequestionidentity,resolution/cutoff,units,availability andcausal/conditionalmeaning beforeconnectorcode'],technique_ids=[49,50,51,52,53,54,55,56,57,58,59,60]),
      dict(priority='P2',group='Performance/scalability',value='Medium after practical workloademand',correctness_risk='Medium;determinism/tolerancepreservation',effort='Medium/high',actions=['Benchmark realworkloads beforechangingbounds','Preserveexactoracles,completehorizons,canonicalreplay andnamednumericaltolerances whenoptimizing'],technique_ids=retained),
      dict(priority='P2',group='Optional UI/API/product integration',value='Lower until concreteuserflow exists',correctness_risk='Medium;misleadingclaims/externalstate',effort='Medium/high',actions=['Buildonlyrequestedproductflows aroundstableCLI/Pythoninterfaces','Keep source/scope/provenancevisible;avoidnewframeworkorliveexternalservice dependencies duringcoreclosure'],technique_ids=retained)]
    groups[2]['actions'][1]='Prioritizeindependentforecastdatasets onlywhenmatchedcontrols andtrain/testavailabilitycanbepreserved'
    save('data/future-prioritized-refinement-backlog.json',dict(version=1,prioritization_basis='Practicalvalue,correctnessrisk andeffort;editorial schedulingguidance,not extraimplementedfeatures.',groups=groups,per_technique=per_backlog))
    print('60IDs reconciled;54unique boundedrelease records;6exclusions;allvariation/rankrows preserved;'+str(len(embedded))+'embeddedsourceIDs catalogued')
if __name__=='__main__':run()
