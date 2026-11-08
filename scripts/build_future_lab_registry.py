"""Derive all54 capabilities and real Python/CLI contracts from frozen records/code."""
import ast,hashlib,json
from pathlib import Path
from future.remote_viewing import digest
from future.scrying import load_input
R=Path(__file__).resolve().parents[1]
def save(p,x):(R/p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def normalized(path):return hashlib.sha256((R/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
def command_contracts():
    tree=ast.parse((R/'future/__main__.py').read_text(encoding='utf-8'));main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');variables={};contracts={}
    for n in main.body:
        if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='add_parser':
            command=ast.literal_eval(n.value.args[0]);variables[n.targets[0].id]=command;contracts[command]=[]
        if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='add_argument' and isinstance(n.value.func.value,ast.Name) and n.value.func.value.id in variables:
            call=n.value;contracts[variables[call.func.value.id]].append(dict(names=[ast.literal_eval(a) for a in call.args],options={k.arg:ast.unparse(k.value) for k in call.keywords}))
    branches={}
    for n in main.body:
        if not isinstance(n,ast.If) or not isinstance(n.test,ast.Compare) or ast.unparse(n.test.left)!='args.command':continue
        compare=n.test.comparators[0];names=[compare.value] if isinstance(compare,ast.Constant) else [x.value for x in compare.elts]
        for name in names:branches[name]=n
    return contracts,branches
def run():
    if (R/'knowledge/future_lab_registry_freeze_v1.json').exists():raise ValueError('Registry v1 already frozen')
    matrix=load_input(R/'data/future-54-technique-completion-matrix.json');contracts,branches=command_contracts();entries=[]
    for item in matrix['retained']:
        i=item['technique_id'];core=load_input(R/item['core_record']);operations=[];native_paths=set()
        for command in item['cli_commands']:
            branch=branches[command];imports={alias.asname or alias.name:'future.'+n.module+'.'+alias.name for n in ast.walk(branch) if isinstance(n,ast.ImportFrom) and n.level==1 for alias in n.names}
            calls=[n.value for n in ast.walk(branch) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='result' for t in n.targets) and isinstance(n.value,ast.Call)]
            direct=next((c for c in calls if isinstance(c.func,ast.Name) and c.func.id in ('read','reference') and c.func.id in imports),None)
            functions=sorted({imports[c.func.id] for c in calls if isinstance(c.func,ast.Name) and c.func.id in imports})
            if direct:
                entry=imports[direct.func.id];module,function=entry.rsplit('.',1);path=module.replace('.','/')+'.py';tree=ast.parse((R/path).read_text(encoding='utf-8'));definition=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==function);native_paths.add(path);adapter='native_request';signature=ast.unparse(definition.args)
            else:entry='future.__main__.main';path='future/__main__.py';adapter='legacy_cli_inprocess';signature='existing argparse arguments; captured JSON/stdout/stderr/exit status'
            operations.append(dict(command=command,adapter=adapter,python_entry_point=entry,python_signature=signature,native_callables=functions,cli_arguments=contracts[command],input_kind='native_json_object' if direct else 'cli_argument_strings',output_contract='Native structured JSON result unchanged; no artificial common prediction score.',implementation_file=path,implementation_sha256=normalized(path)))
        stem=Path(item['core_record']).name.removesuffix('_core_v1.json');stem='horary' if i==5 else stem
        profiles=[]
        for path in sorted((R/'knowledge').glob(stem+'*v1.json')):
            value=load_input(path)
            if 'profile' in path.name or path.relative_to(R).as_posix()==core.get('profile_record') or path.relative_to(R).as_posix()==core.get('profile_file'):profiles.append(dict(path=path.relative_to(R).as_posix(),sha256=digest(value),contract=value.get('schema',value.get('contract',value.get('exact_contract')))))
        native_schema=next((p['contract'] for p in profiles if p['contract']),None)
        # This is a Lab admission policy backed by the named existing score contracts,
        # not a claim that every other native engine lacks its own diagnostic metrics.
        metrics={49:['mae','rmse','bias'],51:['brier','two_category_brier','calibration'],57:['brier','two_category_brier','calibration']}.get(i,[])
        evaluation=dict(lab_v1_supported=bool(metrics),metrics=metrics,empirical_skill_certified=False,status='eligible_with_frozen_target_rights_and_chronology' if metrics else 'native_protocol_review_required' if i in [43,44,45,53,55] else 'not_an_admitted_empirical_forecast',evidence_record=item['core_record'],evidence_fields=[k for k in ['metric_contract','scoring_policy','probability','chronology','configuration_matrix','certification_scope'] if k in core],boundary='Native scores or symbolic output do not establish empirical validity. Only49/51/57 admitted toLabv1 evaluation;53/55 empirical ingestion remains deferred.')
        if i==49:kind='statistical_time_series_forecast_and_retrospective_evaluation'
        elif i in [51,57]:kind='binary_probability_ledger' if i==51 else 'versioned_binary_probability_aggregation'
        elif i==55:kind='synthetic_trial_window_classification_diagnostic'
        elif i==56:kind='assumption_bound_finite_causal_analysis'
        elif i==58:kind='synthetic_play_credit_market_mechanism'
        elif i==59:kind='finite_numerical_dynamics_simulation'
        elif i==60:kind='editorial_finite_scenario_thought_experiment'
        elif i in [50,52,53,54]:kind='bounded_numerical_reference_or_synthetic_simulation'
        elif i<=7:kind='astronomical_calculation_and_historical_symbolic_reference'
        else:kind='historical_symbolic_or_procedural_reference'
        resources=[]
        if i<=7:resources=['data/de440s.bsp']
        if i==49:resources=[core['dataset']['path']]
        entries.append(dict(technique_id=i,name=item['name'],release_status=core['status'],core_record=item['core_record'],core_sha256=digest(core),profile_identifiers=item['profile_identifier'],profile_identifier_kind=item['profile_identifier_kind'],profile_sha256=item['profile_sha256'],profiles=profiles,operations=operations,callable_lab_entry_point='future.lab.invoke',input_contract=native_schema or dict(authoritative_release=item['core_record'],cli_argument_contract='See operations; validation uses the unchanged native implementation.'),output_contract=dict(native=True,scope=item['supported_scope'],provenance='Native source/profile/code/report fields preserved; Lab adds a separate invocation envelope.'),sources=[dict(path=p,sha256=digest(load_input(R/p))) for p in item['source_catalogs']],supported_scope=item['supported_scope'],limitations=item['limitations'],unsupported_operations=core.get('configuration_matrix',{}).get('unsupported',core.get('unsupported',item['limitations'])),required_data=dict(offline_assets=[dict(path=p,raw_sha256=hashlib.sha256((R/p).read_bytes()).hexdigest()) for p in resources],caller_data='Native input object or explicit CLI arguments as declared in operations; no implicit external acquisition.'),capability_type=kind,type_evidence=dict(record=item['core_record'],status=core['status'],scope=item['supported_scope']),evaluation=evaluation))
    assert len(entries)==54 and sorted(e['technique_id'] for e in entries)==[i for i in range(1,61) if i not in [25,27,41,42,47,48]]
    registry=dict(schema_version=1,id='future-lab-capability-registry-v1',core_release='core-v1.0.0',core_commit='685a32936727e7bfd83bee94cdba00a080f0e857',completion_matrix_sha256=digest(matrix),excluded_ids=[25,27,41,42,47,48],entries=entries,classification_policy='Lab admission/type labels are versioned metadata derived from the linked frozen scope and native scoring contracts; no engine capability or empirical validation is added.',native_dispatch_counts={kind:sum(o['adapter']==kind for e in entries for o in e['operations']) for kind in ['native_request','legacy_cli_inprocess']})
    save('data/future-lab-capability-registry.json',registry);save('knowledge/future_lab_registry_freeze_v1.json',dict(version=1,registry_sha256=digest(registry),completion_matrix_sha256=digest(matrix),native_main_sha256=normalized('future/__main__.py'),entry_ids=[e['technique_id'] for e in entries]))
    print(digest(registry),registry['native_dispatch_counts'])
if __name__=='__main__':run()
