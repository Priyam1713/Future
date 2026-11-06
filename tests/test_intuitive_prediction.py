import copy,json,unittest
from pathlib import Path
from fractions import Fraction as Q
from future import intuitive_prediction as p

F=json.loads(Path('tests/fixtures/intuitive_prediction_reference_v1.json').read_text(encoding='utf-8'))
def tm(day,hour=0):return f'2026-11-{day:02d}T{hour:02d}:00:00Z'
def dec(**kw):
    d=copy.deepcopy(F['decision']);d.update(kw);return d
def ttb(**kw):
    v=dict(profile=p.PROFILES['take-the-best'],recognition=['recognized','recognized'],cues=copy.deepcopy(F['search_stop']['cues']));v.update(kw);return dec(**v)
def study(plan=None,forecasts=None,resolutions=None):
    l=p.create(copy.deepcopy(plan or F['plan']))
    for f in copy.deepcopy(F['forecasts'] if forecasts is None else forecasts):l=p.append(l,'forecast',f)
    for r in copy.deepcopy(F['resolutions'] if resolutions is None else resolutions):l=p.append(l,'resolve',r)
    return l
def baseline_plan():
    v=copy.deepcopy(F['plan']);v['events']=v['events'][:2];v['slots']=v['slots'][:2]
    v['baseline']=dict(probability='0.25',frozen_at=tm(8),domain=v['domain'],horizon=v['horizon'],event_definition=v['event_definition'],
        training_start=tm(1),training_end=tm(7),training_outcomes=[dict(event_id='train'+str(i),outcome=y) for i,y in enumerate([0,0,0,1])],evidence=copy.deepcopy(F['evidence']))
    return v
def baseline_study():
    forecasts=copy.deepcopy(F['forecasts'][:2]);resolutions=copy.deepcopy(F['resolutions'][:2])
    for v,q in zip(forecasts,['0.1','0.9']):v['probability']=q
    for v,y in zip(resolutions,[0,1]):v['outcome']=y
    return study(baseline_plan(),forecasts,resolutions)

class IntuitivePredictionTests(unittest.TestCase):
    def test_recognition_positive(self):self.assertEqual(p.decision(dec())['selected'],'A')
    def test_recognition_negative(self):self.assertEqual(p.decision(dec(ecological_direction='negative'))['selected'],'B')
    def test_recognition_lower(self):self.assertEqual(p.decision(dec(criterion_direction='lower'))['selected'],'B')
    def test_recognition_negative_lower(self):self.assertEqual(p.decision(dec(ecological_direction='negative',criterion_direction='lower'))['selected'],'A')
    def test_recognition_unknown_direction(self):self.assertEqual(p.decision(dec(ecological_direction='unknown'))['reason'],'unknown_ecological_direction')
    def test_recognition_both(self):self.assertIsNone(p.decision(dec(recognition=['recognized']*2))['selected'])
    def test_recognition_neither(self):self.assertIsNone(p.decision(dec(recognition=['unrecognized']*2))['selected'])
    def test_recognition_unknown(self):self.assertIsNone(p.decision(dec(recognition=['recognized','unknown']))['selected'])
    def test_ttb_precedence(self):
        d=ttb();d['recognition']=['unrecognized','recognized'];r=p.decision(d)
        self.assertEqual(r['selected'],'B');self.assertEqual(r['inspected'],[])
    def test_ttb_neither(self):
        d=ttb();d['recognition']=['unrecognized']*2;self.assertIsNone(p.decision(d)['selected'])
    def test_ttb_negative_not_imported(self):
        with self.assertRaises(ValueError):p.decision(ttb(ecological_direction='negative'))
    def test_source_examples(self):
        for x in F['source_worked']:
            r=p.decision(ttb(alternatives=x['alternatives'],cues=x['cues']))
            self.assertEqual(r['selected'],x['selected']);self.assertEqual([c['cue']['cue_id'] for c in r['inspected']],x['inspected'])
    def test_early_stop(self):
        r=p.decision(ttb());self.assertEqual(r['selected'],'B');self.assertEqual(r['not_inspected'],['c3']);self.assertEqual(len(r['inspected']),2)
    def test_nine_pairs(self):
        for x,y,expected in F['cue_pairs']:
            c=copy.deepcopy(F['search_stop']['cues'][0]);c['values']=[x,y]
            self.assertEqual(p.decision(ttb(cues=[c]))['selected'],expected)
    def test_exhausted(self):self.assertEqual(p.decision(ttb(cues=[]))['reason'],'exhausted_cues_editorial_abstention')
    def test_tie_abstain(self):
        c=copy.deepcopy(F['search_stop']['cues'][:2]);c[1]['validity']=c[0]['validity']
        self.assertEqual(p.decision(ttb(cues=c))['reason'],'ambiguous_validity_tie')
    def test_tie_frozen(self):
        c=copy.deepcopy(F['search_stop']['cues'][:2]);c[1]['validity']=c[0]['validity']
        self.assertEqual(p.decision(ttb(cues=c,tie_policy='frozen_order'))['selected'],'B')
    def test_invalid_rank(self):
        c=copy.deepcopy(F['search_stop']['cues']);c[1]['rank']=1
        with self.assertRaises(ValueError):p.decision(ttb(cues=c))
    def test_unsorted_validity(self):
        c=copy.deepcopy(F['search_stop']['cues']);c[1]['validity']='1'
        with self.assertRaises(ValueError):p.decision(ttb(cues=c))
    def test_invalid_orientation(self):
        c=copy.deepcopy(F['search_stop']['cues']);c[0]['orientation']='negative'
        with self.assertRaises(ValueError):p.decision(ttb(cues=c))
    def test_invalid_validity(self):
        c=copy.deepcopy(F['search_stop']['cues']);c[0]['validity']='0.4'
        with self.assertRaises(ValueError):p.decision(ttb(cues=c))
    def test_missing_provenance(self):
        c=copy.deepcopy(F['search_stop']['cues']);c[0]['provenance']=''
        with self.assertRaises(ValueError):p.decision(ttb(cues=c))
    def test_probability_boundaries(self):
        for q in ['0','1','0.5']:self.assertEqual(p.probability(q),Q(q))
    def test_exact_grid(self):
        for x in F['rational_grid']:self.assertEqual(str((p.probability(x['probability'])-x['outcome'])**2),x['loss'])
    def test_exact_brier(self):
        r=p.evaluate(study());self.assertEqual(r['brier']['exact'],'5/16');self.assertEqual(r['two_category_positive_quadratic']['exact'],'5/8')
        self.assertEqual([x['loss']['exact'] for x in r['forecasts']],F['brier']['losses'])
    def test_n0(self):
        r=p.evaluate(study(forecasts=[],resolutions=[]));self.assertIsNone(r['brier']);self.assertEqual(r['denominators']['planned'],4)
    def test_unresolved(self):
        r=p.evaluate(study(resolutions=[]));self.assertEqual(r['denominators']['unresolved'],4);self.assertIsNone(r['brier'])
    def test_disputed_void(self):
        rr=copy.deepcopy(F['resolutions']);rr[0].update(status='disputed',outcome=None);rr[1].update(status='void',outcome=None)
        r=p.evaluate(study(resolutions=rr));self.assertEqual(r['denominators']['disputed'],1);self.assertEqual(r['denominators']['void'],1);self.assertEqual(r['denominators']['resolved_and_scored'],2)
    def test_missing_evidence(self):
        rr=copy.deepcopy(F['resolutions']);rr[0]['evidence']=None;r=p.evaluate(study(resolutions=rr));self.assertEqual(r['denominators']['missing_resolution_evidence'],1)
    def test_unknown_occurrence(self):
        rr=copy.deepcopy(F['resolutions']);rr[0]['occurrence_at']=None;r=p.evaluate(study(resolutions=rr));self.assertIn('occurrence_time_unknown',r['forecasts'][0]['exclusion_reasons'])
    def test_equal_occurrence(self):
        rr=copy.deepcopy(F['resolutions']);rr[0]['occurrence_at']=tm(10)
        r=p.evaluate(study(resolutions=rr));self.assertIn('at_or_after_occurrence',r['forecasts'][0]['versions'][0]['exclusion_reasons'])
    def test_outside_window(self):
        rr=copy.deepcopy(F['resolutions']);rr[0]['occurrence_at']=tm(10,12);r=p.evaluate(study(resolutions=rr));self.assertIn('outside_event_window',r['forecasts'][0]['exclusion_reasons'])
    def test_equal_cutoff(self):
        ff=copy.deepcopy(F['forecasts']);ff[-1]['at']=tm(10,23);self.assertEqual(p.evaluate(study(forecasts=ff))['denominators']['resolved_and_scored'],4)
    def test_late(self):
        ff=copy.deepcopy(F['forecasts']);ff[-1]['at']=tm(11);r=p.evaluate(study(forecasts=ff));self.assertEqual(r['denominators']['late_versions'],1)
    def test_known(self):
        ff=copy.deepcopy(F['forecasts']);ff[-1]['outcome_known']=True;self.assertEqual(p.evaluate(study(forecasts=ff))['denominators']['resolved_and_scored'],3)
    def test_amend(self):
        l=study(resolutions=[]);v=copy.deepcopy(F['forecasts'][0]);v.update(at=tm(10,1),probability='0.9',parent_sha256=p.digest(v),reason='Prospective revision')
        l=p.append(l,'forecast',v)
        for r in F['resolutions']:l=p.append(l,'resolve',r)
        r=p.evaluate(l);self.assertEqual(r['denominators']['resolved_and_scored'],4);self.assertEqual(r['denominators']['amendments'],1);self.assertEqual(r['forecasts'][0]['loss']['exact'],'1/100')
    def test_late_amendment_keeps_original(self):
        l=study();v=copy.deepcopy(F['forecasts'][0]);v.update(at=tm(13),probability='1',parent_sha256=p.digest(v),reason='After event',outcome_known=True)
        r=p.evaluate(p.append(l,'forecast',v));self.assertEqual(r['forecasts'][0]['selected_version_sha256'],F['expected_original_sha256'][0]);self.assertEqual(r['brier']['exact'],'5/16')
    def test_wrong_parent(self):
        l=study(resolutions=[]);v=copy.deepcopy(F['forecasts'][0]);v['parent_sha256']='0'*64
        with self.assertRaises(ValueError):p.append(l,'forecast',v)
    def test_duplicate_slot(self):
        pl=copy.deepcopy(F['plan']);pl['slots'].append(copy.deepcopy(pl['slots'][0]))
        with self.assertRaises(ValueError):p.create(pl)
    def test_tamper(self):
        l=study();l['actions'][0]['payload']['notes']+='x'
        with self.assertRaises(ValueError):p.replay(l)
    def test_raw_unicode(self):
        ff=copy.deepcopy(F['forecasts']);ff[0]['notes']='e\u0301  \n';r=p.evaluate(study(forecasts=ff));self.assertEqual(r['forecasts'][0]['versions'][0]['record']['notes'],'e\u0301  \n')
    def test_calibration(self):
        ff=copy.deepcopy(F['forecasts']);ff[1]['probability']='0.8';r=p.evaluate(study(forecasts=ff));b=r['calibration'][8]
        self.assertEqual((b['count'],b['mean_probability']['exact'],b['observed_frequency']['exact']),(2,'4/5','1/2'));self.assertIsNone(r['calibration'][0]['observed_frequency'])
    def test_calibration_endpoints(self):
        ff=copy.deepcopy(F['forecasts']);ff[0]['probability']='1';ff[1]['probability']='0';r=p.evaluate(study(forecasts=ff));self.assertEqual(r['calibration'][9]['count'],1);self.assertEqual(r['calibration'][0]['count'],1)
    def test_baseline(self):
        r=p.evaluate(baseline_study());self.assertEqual(r['brier']['exact'],'1/100');self.assertEqual(r['baseline']['brier']['exact'],'5/16');self.assertEqual(r['baseline']['paired_absolute_improvement']['exact'],'121/400')
    def test_baseline_leak(self):
        pl=baseline_plan();pl['baseline']['training_outcomes'][0]['event_id']='e1'
        with self.assertRaises(ValueError):p.create(pl)
    def test_baseline_bad_prevalence(self):
        pl=baseline_plan();pl['baseline']['probability']='0.5'
        with self.assertRaises(ValueError):p.create(pl)
    def test_baseline_scope(self):
        pl=baseline_plan();pl['baseline']['domain']='other'
        with self.assertRaises(ValueError):p.create(pl)
    def test_baseline_time(self):
        pl=baseline_plan();pl['baseline']['training_end']=tm(9)
        with self.assertRaises(ValueError):p.create(pl)
    def test_confidence_separate(self):
        ff=copy.deepcopy(F['forecasts']);ff[0]['probability']='0';r=p.evaluate(study(forecasts=ff));self.assertEqual(r['forecasts'][0]['loss']['exact'],'1');self.assertEqual(r['forecasts'][0]['versions'][0]['record']['confidence'],'high')
    def test_environment_change(self):
        d=dec();d['context']['environment_changed']=True;self.assertIn('environment_changed:prior_validity_may_not_transfer',p.decision(d)['domain_review']['warnings'])
    def test_no_probability(self):self.assertFalse(p.decision(dec())['probability_generated'])
    def test_reference(self):
        v=dict(context=copy.deepcopy(F['decision']['context']),rpd={k:'Human declaration' for k in ['cues_noticed','situation','expectancies','anomalies','candidate_action','mental_simulation','revision_or_alternative','feedback_history']})
        self.assertFalse(p.reference(v)['action_selected_by_software'])
    def test_rights(self):
        rr=copy.deepcopy(F['resolutions']);rr[0]['evidence']['permission']=''
        with self.assertRaises(ValueError):study(resolutions=rr)
    def test_wrong_bytes(self):
        rr=copy.deepcopy(F['resolutions']);rr[0]['evidence']['sha256']='0'*64
        with self.assertRaises(ValueError):study(resolutions=rr)
    def test_consent(self):
        pl=copy.deepcopy(F['plan']);pl['privacy_consent']=False
        with self.assertRaises(ValueError):p.create(pl)
    def test_missing_zone(self):
        ff=copy.deepcopy(F['forecasts']);ff[0]['at']='2026-11-10T00:00:00'
        with self.assertRaises(ValueError):study(forecasts=ff)
    def test_group_dependence(self):
        pl=copy.deepcopy(F['plan']);pl['events'][1]['dependency_group']='g1';r=p.evaluate(study(pl));self.assertEqual(r['denominators']['scored_dependency_groups'],3)
    def test_decision_link(self):
        l=p.append(p.create(F['plan']),'decision',dec());v=copy.deepcopy(F['forecasts'][0]);v['decision_id']='d1';l=p.append(l,'forecast',v)
        self.assertEqual(p.evaluate(l)['forecasts'][0]['versions'][0]['record']['probability'],'0.8')
    def test_unknown_decision_link(self):
        ff=copy.deepcopy(F['forecasts']);ff[0]['decision_id']='missing'
        with self.assertRaises(ValueError):study(forecasts=ff)
    def test_resolution_replacement(self):
        l=study()
        with self.assertRaises(ValueError):p.append(l,'resolve',F['resolutions'][0])
    def test_markdown(self):
        q=dict(schema_version=1,task='report',ledger=study());r=p.read(q);raw=p.markdown(r);self.assertIn(json.dumps(r,ensure_ascii=False,indent=2),raw);self.assertEqual(r,p.read(q))

def rejected_probability(v):
    def test(self):
        with self.assertRaises(ValueError):p.probability(v)
    return test
for i,v in enumerate(['-0.1','1.1','NaN','Infinity','0e0','+0.1',' 0.1','00.1','.1','0.','0.'+'1'*101,True,False,None,0.8,1,{},[]]):
    setattr(IntuitivePredictionTests,'test_reject_probability_'+str(i),rejected_probability(v))

if __name__=='__main__':unittest.main()
