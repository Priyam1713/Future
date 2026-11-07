import copy
import unittest
from pathlib import Path
from future import superforecasting as e
from future.scrying import load_input
from scripts.superforecasting_oracle import plan,reference_class,sha

FIX=load_input(Path('tests/fixtures/superforecasting_reference_v1.json'))
class SuperforecastingTests(unittest.TestCase):
    def test_original_plan_and_hash(self):
        p=plan();self.assertEqual(p,FIX['original_plan']);l=e.create(p);self.assertEqual(l['plan_sha256'],sha(p));l['plan']['questions'][0]['text']='changed';self.assertEqual(p,plan())
    def test_question_lock(self):
        q=plan()['questions'][0];q['locked_at']='2025-01-04T00:00:00Z'
        with self.assertRaises(ValueError):e.question(q)
    def test_ambiguous_question_declaration(self):
        q=plan()['questions'][0];q['clarity_confirmed']=False
        with self.assertRaises(ValueError):e.question(q)
    def test_missing_resolution_rule(self):
        q=plan()['questions'][0];q['resolution']['negative_rule']=' '
        with self.assertRaises(ValueError):e.question(q)
    def test_class_unknown_members_retained(self):
        c=reference_class([1,None,0]);c['members'][0]['eligibility']='ambiguous';r=e.reference_class(c);self.assertEqual(r['denominator'],1);self.assertEqual(r['base_rate']['exact'],'0');self.assertEqual(len(r['members']),3)
    def test_duplicate_historical_event(self):
        c=reference_class();c['members'][1]['event_id']=c['members'][0]['event_id']
        with self.assertRaises(ValueError):e.reference_class(c)
    def test_class_after_freeze(self):
        c=reference_class();c['members'][0]['observed_at']='2025-01-01T00:00:00Z'
        with self.assertRaises(ValueError):e.reference_class(c)
    def test_class_mutation_hash(self):
        p=plan();p['classes'][0]['members'][0]['outcome']=0
        with self.assertRaises(ValueError):e.create(p)
    def test_test_group_leak(self):
        p=plan();p['classes'][0]['members'][0]['dependency_group']='test1'
        with self.assertRaises(ValueError):e.create(p)
    def test_event_leak(self):
        p=plan();p['classes'][0]['members'][0]['event_id']='event1';p['questions'][0]['class_sha256']=sha(p['classes'][0])
        with self.assertRaises(ValueError):e.create(p)
    def test_duplicate_slot(self):
        p=plan();p['slots'].append(copy.deepcopy(p['slots'][0]))
        with self.assertRaises(ValueError):e.create(p)
    def test_invalid_class_type(self):
        p=plan();p['classes']=[None]
        with self.assertRaises(ValueError):e.create(p)
    def test_rights(self):
        c=reference_class();c['source']['rights']='unknown'
        with self.assertRaises(ValueError):e.reference_class(c)
    def test_snapshot_hash(self):
        c=reference_class();c['source']['snapshot']+='rewrite'
        with self.assertRaises(ValueError):e.reference_class(c)
    def test_source_identity(self):
        p=plan();p['questions'][1]['source']['locator']='different'
        with self.assertRaises(ValueError):e.create(p)
    def test_reference_baseline(self):
        p=plan();p['questions'][0]['baseline'].update(kind='reference_class',probability='3/10');e.create(p)
        p['questions'][0]['baseline']['probability']='1/2'
        with self.assertRaises(ValueError):e.create(p)
    def test_empirical_mode_reject(self):
        p=plan();p['evidence_mode']='validated_superforecaster'
        with self.assertRaises(ValueError):e.create(p)

for i,c in enumerate(FIX['base_rates']):
    def test(self,c=c):
        r=e.reference_class(reference_class(c['outcomes']));self.assertEqual((r['numerator'],r['denominator'],r['base_rate']['exact']),(c['k'],c['n'],c['rate']))
    setattr(SuperforecastingTests,f'test_reference_{i}',test)

from scripts.superforecasting_oracle import forecast,update,resolution
class SuperforecastingActionTests(unittest.TestCase):
    def setup_update(self):
        p=plan();v=forecast(p);l=e.append(e.create(p),'forecast',v);u=update(v,p);l=e.append(l,'update',u);return p,l,v,u
    def test_positive_update(self):
        p,l,v,u=self.setup_update();r=e.replay(l)['forecasts']['f1'][-1];self.assertEqual(r['calculation']['posterior']['exact'],'3/7');self.assertFalse(r['calculation']['empirically_validated'])
    def test_conditional_likelihoods(self):
        p=plan();v=forecast(p);u=update(v,p);u['bayes'].update(kind='conditional_likelihoods',ratio=None,likelihood_h='3/5',likelihood_not_h='1/5');l=e.append(e.append(e.create(p),'forecast',v),'update',u);self.assertEqual(e.replay(l)['forecasts']['f1'][-1]['record']['probability'],'3/7')
    def test_duplicate_evidence_attempt(self):
        p,l,v,u=self.setup_update();bad=update(u,p,at='2025-01-02T01:00:00Z',dependence='independent');out=e.append(l,'update',bad,keep_rejected=True);self.assertEqual(len(e.replay(out)['forecasts']['f1']),2);self.assertEqual(out['actions'][-1]['decision'],'rejected');self.assertIn('Duplicate evidence',out['actions'][-1]['reason']);self.assertEqual(out['actions'][-1]['record'],bad)
    def test_same_fact_new_article(self):
        p,l,v,u=self.setup_update();bad=update(u,p,evidence_id='e2',group='newgroup',fact='fact1',at='2025-01-02T01:00:00Z',dependence='independent')
        with self.assertRaises(ValueError):e.append(l,'update',bad)
    def test_same_snapshot_new_id(self):
        p,l,v,u=self.setup_update();bad=update(u,p,evidence_id='e2',group='newgroup',fact='fact2',at='2025-01-02T01:00:00Z',dependence='independent');bad['evidence'][0]['source']=copy.deepcopy(u['evidence'][0]['source'])
        with self.assertRaises(ValueError):e.append(l,'update',bad)
    def test_independence_both_hypotheses(self):
        p,l,v,u=self.setup_update();bad=update(u,p,evidence_id='e2',group='newgroup',fact='fact2',at='2025-01-02T01:00:00Z',dependence='independent');bad['bayes']['independent_given_not_h']=False
        with self.assertRaises(ValueError):e.append(l,'update',bad)
    def test_same_group_cannot_claim_independence(self):
        p,l,v,u=self.setup_update();bad=update(u,p,evidence_id='e2',group='evidence-group1',fact='fact2',at='2025-01-02T01:00:00Z',dependence='independent')
        with self.assertRaises(ValueError):e.append(l,'update',bad)
    def test_independent_new_facts(self):
        p,l,v,u=self.setup_update();new=update(u,p,evidence_id='e2',group='newgroup',fact='fact2',at='2025-01-02T01:00:00Z',dependence='independent');out=e.append(l,'update',new);self.assertEqual(e.replay(out)['forecasts']['f1'][-1]['record']['probability'],'9/13')
    def test_conditional_same_group_new_fact(self):
        p,l,v,u=self.setup_update();new=update(u,p,evidence_id='e2',fact='fact2',at='2025-01-02T01:00:00Z',dependence='conditional',conditioned_on=['evidence1']);e.append(l,'update',new);new['bayes']['conditioned_on']=[]
        with self.assertRaises(ValueError):e.append(l,'update',new)
    def test_wrong_posterior(self):
        p=plan();v=forecast(p);u=update(v,p);u['probability']='1/2'
        with self.assertRaises(ValueError):e.append(e.append(e.create(p),'forecast',v),'update',u)
    def test_manual_revision_not_backsolved(self):
        p,l,v,u=self.setup_update();m=forecast(p,probability='2/5',version=3,parent=sha(u),at='2025-01-02T02:00:00Z');l=e.append(l,'forecast',m);self.assertIsNone(e.replay(l)['forecasts']['f1'][-1]['calculation'])
    def test_late_forecast_retained(self):
        p=plan();v=forecast(p,at='2025-01-04T00:00:00Z');l=e.append(e.create(p),'forecast',v);self.assertEqual(len(e.replay(l)['forecasts']['f1']),1)
    def test_wrong_parent(self):
        p=plan();v=forecast(p,version=2,parent='0'*64)
        with self.assertRaises(ValueError):e.append(e.create(p),'forecast',v)
    def test_backward_action_time(self):
        p,l,v,u=self.setup_update();m=forecast(p,version=3,parent=sha(u),at='2025-01-01T20:00:00Z')
        with self.assertRaises(ValueError):e.append(l,'forecast',m)
    def test_resolution_negative_null_occurrence(self):
        p=plan();r=resolution(p,outcome=0);l=e.append(e.create(p),'resolve',r);self.assertIsNone(e.replay(l)['resolutions']['q1'][0]['record']['occurrence_at']);r['occurrence_at']=r['window_end']
        with self.assertRaises(ValueError):e.append(e.create(p),'resolve',r)
    def test_negative_before_window_close(self):
        p=plan();r=resolution(p,outcome=0);r['outcome_known_at']='2025-01-09T23:59:59Z'
        with self.assertRaises(ValueError):e.append(e.create(p),'resolve',r)
    def test_positive_window_end_excluded(self):
        p=plan();r=resolution(p);r['occurrence_at']=r['window_end']
        with self.assertRaises(ValueError):e.append(e.create(p),'resolve',r)
    def test_resolution_correction_history(self):
        p=plan();r=resolution(p);l=e.append(e.create(p),'resolve',r);new=resolution(p,outcome=0,version=2,parent=sha(r),at='2025-01-12T00:00:00Z')
        with self.assertRaises(ValueError):e.append(l,'resolve',new)
        dispute=resolution(p,status='disputed',version=2,parent=sha(r),at='2025-01-12T00:00:00Z');l=e.append(l,'resolve',dispute);new=resolution(p,outcome=0,version=3,parent=sha(dispute),at='2025-01-13T00:00:00Z');l=e.append(l,'resolve',new);self.assertEqual(len(e.replay(l)['resolutions']['q1']),3)
    def test_action_chain_mutation(self):
        p,l,v,u=self.setup_update();l['actions'][0]['record']['probability']='1'
        with self.assertRaises(ValueError):e.replay(l)
    def test_forged_rejection(self):
        p,l,v,u=self.setup_update();l['actions'][-1]['decision']='rejected';l['actions'][-1]['reason']='false';l['actions'][-1]['sha256']=sha({k:v for k,v in l['actions'][-1].items() if k!='sha256'})
        with self.assertRaises(ValueError):e.replay(l)
    def test_impossible_conditional_evidence(self):
        p=plan();v=forecast(p);u=update(v,p);u['bayes'].update(kind='conditional_likelihoods',ratio=None,likelihood_h='0',likelihood_not_h='0')
        with self.assertRaises(ValueError):e.append(e.append(e.create(p),'forecast',v),'update',u)

for i,c in enumerate(FIX['bayes']):
    def test(self,c=c):
        if c['status']=='undefined':
            with self.assertRaises(ValueError):e.posterior(c['prior'],c['ratio'])
        else:self.assertEqual(str(e.posterior(c['prior'],c['ratio'])),c['posterior'])
    setattr(SuperforecastingActionTests,f'test_bayes_{i}',test)

class SuperforecastingScoreTests(unittest.TestCase):
    def study(self,ps,ys):
        p=plan(len(ps));l=e.create(p)
        for i,prob in enumerate(ps):l=e.append(l,'forecast',forecast(p,i,prob))
        for i,y in enumerate(ys):l=e.append(l,'resolve',resolution(p,i,y))
        return p,l,e.evaluate(l)
    def test_paired(self):
        c=FIX['paired'];p,l,r=self.study(c['ps'],c['ys']);a=r['primary'];self.assertEqual(a['binary_brier']['exact'],'13/200');self.assertEqual(a['baseline']['baseline_brier']['exact'],c['baseline']);self.assertEqual(a['baseline']['absolute_improvement']['exact'],c['improvement']);self.assertEqual(a['baseline']['relative_skill']['exact'],c['skill'])
    def test_decomposition(self):
        c=FIX['decomposition'];p,l,r=self.study(c['ps'],c['ys']);d=r['primary']['decomposition'];self.assertEqual(r['primary']['binary_brier']['exact'],c['expected']['binary'])
        for k in ('reliability','resolution','uncertainty'):self.assertEqual(d[k]['exact'],c['expected'][k])
        self.assertTrue(d['identity_passed'])
    def test_coarse_bins_not_used_for_identity(self):
        p,l,r=self.study(['21/100','29/100'],[0,1]);d=r['primary']['decomposition'];self.assertEqual(len(d['groups']),2);self.assertEqual(r['primary']['calibration'][2]['count'],2);self.assertTrue(d['identity_passed'])
    def test_version_selection_and_late(self):
        p=plan(1);v=forecast(p);m=forecast(p,probability='2/5',version=2,parent=sha(v),at='2025-01-02T12:00:00Z');late=forecast(p,probability='9/10',version=3,parent=sha(m),at='2025-01-04T00:00:00Z');l=e.create(p)
        for row in (v,m,late):l=e.append(l,'forecast',row)
        l=e.append(l,'resolve',resolution(p));r=e.evaluate(l)['rows'][0];self.assertEqual(r['selected_version'],2);self.assertEqual(r['probability']['exact'],'2/5');self.assertEqual(len(r['versions']),3);self.assertIn('after_cutoff',r['versions'][-1]['exclusion_reasons'])
    def test_forecast_at_cutoff(self):
        p=plan(1);v=forecast(p,at='2025-01-03T00:00:00Z');l=e.append(e.append(e.create(p),'forecast',v),'resolve',resolution(p));self.assertEqual(e.evaluate(l)['primary']['denominator'],1)
    def test_positive_occurrence_before_forecast(self):
        p=plan(1);v=forecast(p,at='2025-01-02T12:00:00Z');r=resolution(p);r['occurrence_at']='2025-01-02T11:00:00Z';l=e.append(e.append(e.create(p),'forecast',v),'resolve',r);self.assertEqual(e.evaluate(l)['primary']['denominator'],0)
    def test_post_knowledge_retained_unscored(self):
        p=plan(1);p['questions'][0]['cutoff']='2025-01-07T00:00:00Z';v=forecast(p,at='2025-01-06T00:00:00Z');l=e.append(e.append(e.create(p),'forecast',v),'resolve',resolution(p));r=e.evaluate(l);self.assertEqual(r['denominators']['versions'],1);self.assertEqual(r['primary']['denominator'],0)
    def test_empty_scores(self):
        r=e.evaluate(e.create(plan()));self.assertIsNone(r['primary']['binary_brier']['exact']);self.assertEqual(r['primary']['denominator'],0);self.assertEqual(len(r['questions']),4)
    def test_disputed_void_unresolved_denominators(self):
        p=plan(4);l=e.create(p)
        for i in range(4):l=e.append(l,'forecast',forecast(p,i,'1/2'))
        for i,status in enumerate(('resolved','resolved','disputed','void')):l=e.append(l,'resolve',resolution(p,i,i%2,status))
        r=e.evaluate(l);self.assertEqual(r['primary']['denominator'],2);self.assertEqual(r['denominators']['planned_questions'],4);self.assertEqual(r['denominators']['question_statuses'],dict(resolved=2,unresolved=0,disputed=1,void=1));self.assertEqual(len(r['primary']['baseline']['excluded_pairs']),2)
    def test_two_people_one_event(self):
        p=plan(1);p['slots'].append(dict(forecast_id='f2',question_id='q1',participant='person2',participant_kind='individual'));l=e.create(p);v1=forecast(p,0,'1/5');v2=copy.deepcopy(v1);v2.update(forecast_id='f2',participant='person2',probability='4/5');l=e.append(e.append(l,'forecast',v1),'forecast',v2);l=e.append(l,'resolve',resolution(p));r=e.evaluate(l);self.assertEqual((r['primary']['denominator'],r['primary']['unique_events'],r['primary']['dependency_groups']),(2,1,1));self.assertIsNone(r['primary']['team_aggregation'])
    def test_mixed_train_test(self):
        p=plan(2);p['questions'][1]['partition']='train';p['partition']['test_groups'].remove('test2');p['partition']['train_groups'].append('test2');l=e.create(p)
        for i in (0,1):l=e.append(l,'forecast',forecast(p,i,'1/2'))
        for i in (0,1):l=e.append(l,'resolve',resolution(p,i,1))
        r=e.evaluate(l);self.assertEqual(r['primary']['denominator'],1);self.assertEqual(r['by_partition']['train']['denominator'],1);self.assertEqual(len(r['rows']),2)
    def test_zero_baseline_skill_not_estimable(self):
        p=plan(1);p['questions'][0]['baseline']['probability']='1';l=e.append(e.append(e.create(p),'forecast',forecast(p,0,'1/2')),'resolve',resolution(p));b=e.evaluate(l)['primary']['baseline'];self.assertEqual(b['baseline_brier']['exact'],'0');self.assertIsNone(b['relative_skill']['exact']);self.assertEqual(b['relative_skill']['reason'],'zero_baseline_loss')
    def test_unpaired_subset_uses_matched_model_score(self):
        p=plan(2);p['questions'][1]['baseline']=None;l=e.create(p)
        for i,prob in enumerate(('4/5','0')):l=e.append(l,'forecast',forecast(p,i,prob))
        for i in (0,1):l=e.append(l,'resolve',resolution(p,i,1))
        r=e.evaluate(l)['primary'];self.assertEqual(r['baseline']['denominator'],1);self.assertEqual(r['baseline']['forecast_brier_on_paired']['exact'],'1/25');self.assertNotEqual(r['binary_brier']['exact'],'1/25')
    def test_heldout_sentinel(self):
        p=plan(1);v=forecast(p);u=update(v,p);l=e.append(e.append(e.create(p),'forecast',v),'update',u);a=e.append(l,'resolve',resolution(p,outcome=1));b=e.append(l,'resolve',resolution(p,outcome=0));sa=e.replay(a);sb=e.replay(b);self.assertEqual(a['plan'],b['plan']);self.assertEqual(sa['forecasts'],sb['forecasts']);self.assertEqual(e.evaluate(a)['rows'][0]['selected_version_sha256'],e.evaluate(b)['rows'][0]['selected_version_sha256'])
    def test_negative_distinct_times(self):
        p=plan(1);l=e.append(e.append(e.create(p),'forecast',forecast(p)),'resolve',resolution(p,outcome=0));row=e.evaluate(l)['questions'][0]['resolution_history'][0]['record'];self.assertIsNone(row['occurrence_at']);self.assertNotEqual(row['outcome_known_at'],row['recorded_at'])
    def test_report_replay_unicode_fence(self):
        p=plan(1);p['questions'][0]['reasoning']['disagreement']='  नमस्ते\n```json\n  ';q=e.request('create',p);r=e.read(q);md=e.markdown(r);fence=md.splitlines()[-1];data=md.split(fence+'json\n')[1].rsplit('\n'+fence,1)[0];self.assertEqual(__import__('json').loads(data),r);self.assertEqual(e.read(q),r)
    def test_report_mutation_isolated(self):
        q=e.request('reference',dict(id='bayes'));r=e.read(q);old=copy.deepcopy(r);r['result']['scope']='modified';r['limits'].clear();self.assertEqual(e.read(q),old)

for i,c in enumerate(FIX['losses']):
    def test(self,c=c):
        p=plan(1);l=e.append(e.append(e.create(p),'forecast',forecast(p,0,c['p'])),'resolve',resolution(p,0,c['y']));r=e.evaluate(l);row=r['rows'][0];self.assertEqual(row['binary_brier']['exact'],c['binary']);self.assertEqual(row['two_category_sum_of_squares']['exact'],c['two_category']);self.assertEqual(row['natural_log_loss']['status'],c['log_status']);self.assertEqual(row['natural_log_loss']['decimal'],c['log_decimal']);self.assertEqual(r['primary']['calibration'][c['calibration_bin']]['count'],1)
    setattr(SuperforecastingScoreTests,f'test_loss_{i}',test)

class SuperforecastingNumericBoundaryTests(unittest.TestCase):
    def test_extremely_small_positive_baseline(self):
        p=plan(1);p['questions'][0]['baseline']['probability']='1/'+str(10**59);l=e.append(e.append(e.create(p),'forecast',forecast(p,0,'1/2')),'resolve',resolution(p,0,0));r=e.evaluate(l)['primary']['baseline'];expected=1-e.Q(1,4)*10**118;self.assertEqual(r['relative_skill']['exact'],str(expected));self.assertEqual(e.Q(r['relative_skill']['decimal']),expected)
    def test_half_even_exact_display(self):
        self.assertEqual(e.number(e.Q(1,2*10**12))['decimal'],'0.000000000000');self.assertEqual(e.number(e.Q(3,2*10**12))['decimal'],'0.000000000002');self.assertEqual(e.number(-e.Q(1,2*10**12))['decimal'],'0.000000000000')
    def test_probability_and_ratio_rejections(self):
        for p in (True,False,1,.5,float('nan'),'NaN','Infinity','1e-3','-1/2','3/2','1/0'):
            with self.assertRaises(ValueError):e.probability(p)
        for L in (True,'NaN','-1','1/0'):
            with self.assertRaises(ValueError):e.posterior('1/5',L)
    def test_unknown_request_and_hash(self):
        q=e.request('create',plan());q['profile']['sha256']='0'*64
        with self.assertRaises(ValueError):e.read(q)
        q=e.request('create',plan());q['extra']=True
        with self.assertRaises(ValueError):e.read(q)

from unittest.mock import patch
class SuperforecastingIntegrityTests(unittest.TestCase):
    def test_all_independent_families(self):
        from scripts.verify_superforecasting import verify
        self.assertEqual(len(verify()['families']),23)
    def test_pinned_assets(self):
        q=e.request('create',plan());old=e.load_input
        for ending in ('profile_v1.json','sources.json','source_freeze_v1.json'):
            def altered(path,ending=ending):
                v=old(path)
                if str(path).endswith(ending):
                    if isinstance(v,list):v[0]['author']='tampered'
                    else:v['tampered']=True
                return v
            with patch.object(e,'load_input',altered):
                with self.assertRaises(ValueError):e.read(q)
    def test_internal_log_range(self):
        for p in (e.Q(-1,2),e.Q(3,2)):
            with self.assertRaises(ValueError):e.log_loss(p,1)

class SuperforecastingTimestampPrecisionTests(unittest.TestCase):
    def test_frozen_fractional_timestamp_boundaries(self):
        f=load_input(Path('tests/fixtures/superforecasting_timestamp_precision_v1.json'));r=e.evaluate(e.create(f['plan']));training=r['rows'][0]['reference_training']
        for key in ('member_event_start','member_observed_end'):self.assertEqual(training[key],f['expected'][key])
        self.assertEqual(r['rows'][0]['lead_seconds']['exact'],f['expected']['lead_seconds']);self.assertEqual(e.question(f['plan']['questions'][0])['lead_seconds']['exact'],f['expected']['lead_seconds'])
