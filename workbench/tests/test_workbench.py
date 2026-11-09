"""Independent boundary/lifecycle tests. Native sample hashes predate this UI."""
import copy, json, tempfile, unittest, uuid
from pathlib import Path
from datetime import datetime,timezone,timedelta
from fastapi.testclient import TestClient
from future.lab.common import ROOT,digest
from workbench.api import create_app

class WorkbenchTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='future-workbench-test-');self.stamp='2030-01-01T00:00:00Z'
        self.app=create_app(self.temp.name,clock=lambda:self.stamp);self.client=TestClient(self.app,base_url='http://127.0.0.1')
        self.sample=json.loads((ROOT/'data/future-lab-invocation-examples.json').read_text(encoding='utf-8'))['entries']
    def tearDown(self):self.client.close();self.temp.cleanup()
    def post(self,path,body,key=None):return self.client.post('/api'+path,json=body,headers={'Idempotency-Key':key or str(uuid.uuid4())})
    def ok(self,r):self.assertEqual(r.status_code,200,r.text[:2000]);return r.json()
    def participant(self,retain=False,scope=None):return self.ok(self.post('/participants',dict(consent=True,scopes=scope or ['explore','blind','prospective'],techniques=[4,51],retain_frozen=retain)))
    def case(self,p):return self.ok(self.post('/cases',dict(participant_id=p['id'],title='Voluntary test case')))
    def session(self,case=None,mode='explore',key=None):return self.ok(self.post('/sessions',dict(request=self.sample['4']['request'],case_id=case['id'] if case else None,mode=mode,origin='sample',hidden_answer='concealed-answer-xyz'),key))
    def forecast(self):return dict(question='Will the independent log contain event X in the observation window?',probability='3/5',cutoff='2030-01-02T00:00:00Z',window_end='2030-01-03T00:00:00Z',positive_rule='Logged event in window',negative_rule='Complete log with no event',source_ref='local:independent-log',evidence='Self-authored protocol, written before observation',reason='Judgment before the event',clarity_confirmed=True)
    def test_catalogue_and_six_exclusions(self):
        r=self.ok(self.client.get('/api/registry'));self.assertEqual(len(r['entries']),54);self.assertEqual(len(r['phases']),6)
        for i in r['excluded_ids']:self.assertEqual(self.client.get('/api/techniques/'+str(i)).status_code,422)
    def test_all54_native_hashes(self):
        for id,e in self.sample.items():
            with self.subTest(technique=id):
                v=self.ok(self.post('/sessions',dict(request=e['request'],origin='sample')))
                self.assertIsNone(v['result']['native_error']);self.assertEqual(v['result']['native_output_sha256'],e['native_output_sha256'])
    def test_native_error_and_unsupported(self):
        q=copy.deepcopy(self.sample['4']['request']);q['arguments'][0]='invalid'
        r=self.ok(self.post('/validate',q));self.assertEqual(r['status'],'native_rejected');self.assertTrue(r['invocation']['native_error'])
        q['operation']='invented';self.assertEqual(self.post('/validate',q).status_code,422)
    def test_idempotent_session_and_conflict(self):
        key=str(uuid.uuid4());a=self.session(key=key);self.assertEqual(a,self.session(key=key));self.assertEqual(len(self.ok(self.client.get('/api/records'))),1)
        self.assertEqual(self.post('/sessions',dict(request=self.sample['4']['request']),key).status_code,422)
    def test_consent_required_and_enforced(self):
        self.assertEqual(self.post('/participants',dict(consent=False)).status_code,422)
        c=self.case(self.participant(scope=['explore']));self.assertEqual(self.post('/sessions',dict(request=self.sample['4']['request'],case_id=c['id'],mode='blind',hidden_answer='secret')).status_code,422)
    def test_blind_lock_reveal_immutable(self):
        c=self.case(self.participant());v=self.session(c,'blind');id=v['id']
        self.assertNotIn('concealed-answer-xyz',json.dumps(v));self.assertNotIn('concealed-answer-xyz',self.client.get('/api/records').text);self.assertNotIn('concealed-answer-xyz',self.client.get('/api/export').text)
        self.assertEqual(self.post(f'/sessions/{id}/reveal',{}).status_code,422)
        locked=self.ok(self.post(f'/sessions/{id}/lock',dict(interpretation='Frozen interpretation')));self.assertEqual(locked['locked']['input_sha256'],digest(v['request']))
        self.assertEqual(self.post(f'/sessions/{id}/lock',dict(interpretation='Replacement')).status_code,422)
        r=self.ok(self.post(f'/sessions/{id}/reveal',{}));self.assertEqual(r['answer'],'concealed-answer-xyz')
        f=self.ok(self.post(f'/sessions/{id}/feedback',dict(assessor='independent-assessor',agreement=4,notes='Descriptive')));self.assertIn('not predictive',f['feedback'][0]['meaning'])
    def test_delete_cascades_and_erases_secrets(self):
        p=self.participant();c=self.case(p);self.session(c,'blind')
        self.assertEqual(self.client.get('/api/records/'+p['id']+'/deletion').json()['records'],3)
        r=self.client.delete('/api/records/'+p['id'],headers={'Idempotency-Key':str(uuid.uuid4())});self.ok(r)
        self.assertEqual(self.ok(self.client.get('/api/records')),[])
        with self.app.state.store.connect() as db:self.assertEqual(db.execute('SELECT COUNT(*) FROM secrets').fetchone()[0],0)
    def test_separately_consented_frozen_retention(self):
        p=self.participant(True);c=self.case(p);s=self.session(c,'blind');self.ok(self.post(f"/sessions/{s['id']}/lock",dict(interpretation='Retain frozen')))
        self.assertTrue(self.ok(self.client.get('/api/records/'+c['id']+'/deletion'))['separately_consented_frozen_retention'])
        r=self.ok(self.client.delete('/api/records/'+p['id'],headers={'Idempotency-Key':str(uuid.uuid4())}));self.assertEqual(r['retained_frozen'],1)
        rows=self.ok(self.client.get('/api/records'));self.assertEqual([v['kind'] for v in rows],['archive']);self.assertIsNone(rows[0]['parent'])
    def test_prospective_pending_resolve_exact_score(self):
        s=self.ok(self.post('/studies',self.forecast()));self.assertEqual(s['report']['coverage']['matched'],0);self.assertIsNone(s['report']['model']['brier']['exact'])
        q=dict(target_id='q1',status='resolved',value='1',known_at='2030-01-03T00:00:00Z',reason='Independent complete log',evidence='Outcome log records event',assessor='independent')
        self.assertEqual(self.post(f"/studies/{s['id']}/outcome",q).status_code,422)
        self.stamp='2030-01-04T00:00:00Z';r=self.ok(self.post(f"/studies/{s['id']}/outcome",q));self.assertEqual(r['report']['model']['brier']['exact'],'4/25');self.assertEqual(r['report']['baseline']['brier']['exact'],'1/4')
        self.assertEqual(self.post(f"/studies/{s['id']}/outcome",q).status_code,422)
    def test_missing_disputed_correction_scoring(self):
        s=self.ok(self.post('/studies',self.forecast()));self.stamp='2030-01-04T00:00:00Z'
        for status in ['disputed','correction','void']:
            r=self.ok(self.post(f"/studies/{s['id']}/outcome",dict(target_id='q1',status=status,reason='Independent dispute',evidence='Independent statement')))
        self.assertEqual(len(r['dispositions']),3);self.assertEqual(self.ok(self.client.get('/api/dashboard'))['eligible_scored'],0)
        s=self.ok(self.post('/studies',dict(self.forecast(),cutoff='2030-01-05T00:00:00Z',window_end='2030-01-06T00:00:00Z')));self.stamp='2030-01-07T00:00:00Z'
        r=self.ok(self.post(f"/studies/{s['id']}/outcome",dict(target_id='q1',status='missing',reason='Log absent',evidence='Independent missing declaration')));self.assertEqual(r['report']['coverage']['missing_outcomes'],1)
    def test_backdating_rejected(self):
        q=self.forecast();q['cutoff']='2029-01-01T00:00:00Z';self.assertEqual(self.post('/studies',q).status_code,422)
    def test_import_export_integrity_and_duplicates(self):
        self.session();e=self.ok(self.client.get('/api/export'));self.assertEqual(self.ok(self.post('/import',e))['imported'],0)
        bad=copy.deepcopy(e);bad['payload']['records'][0]['request']['operation']='altered';self.assertEqual(self.post('/import',bad).status_code,422)
        bad['sha256']=digest(bad['payload']);self.assertEqual(self.post('/import',bad).status_code,422)
    def test_local_boundary_strict_json(self):
        self.assertEqual(self.client.get('/api/records',headers={'Origin':'https://foreign.example'}).status_code,403)
        self.assertEqual(self.client.get('/api/records',headers={'Sec-Fetch-Site':'cross-site'}).status_code,403)
        self.assertEqual(self.client.get('/api/records',headers={'Host':'evil.example'}).status_code,400)
        for payload in ['{"a":1,"a":2}','{"a":NaN}']:
            self.assertEqual(self.client.post('/api/validate',content=payload).status_code,422)
        q=copy.deepcopy(self.sample['1']['request']);q['arguments']+=['--kernel','C:/private/file'];self.assertEqual(self.post('/validate',q).status_code,422)
        for alias in ['--ker','--k','--kernel=C:/private/file']:
            q=copy.deepcopy(self.sample['1']['request']);q['arguments']+=[alias,'C:/private/file'] if '=' not in alias else [alias];self.assertEqual(self.post('/validate',q).status_code,422)
        for malformed in [[],None,'C:/private/file']:
            self.assertEqual(self.post('/sessions',dict(request=malformed)).status_code,422)
    def test_empty_dashboard_and_filters(self):
        r=self.ok(self.client.get('/api/dashboard'));self.assertEqual(r['sessions'],0);self.assertEqual(r['eligible_scored'],0)
        self.session();r=self.ok(self.client.get('/api/dashboard?technique=51'));self.assertEqual(r['sessions'],0)
    def test_comparison_no_universal_scores(self):
        a=self.session();b=self.session();r=self.ok(self.post('/compare',dict(ids=[a['id'],b['id']],quantitative=False)));self.assertEqual(r['mode'],'descriptive')
        self.assertEqual(self.post('/compare',dict(ids=[a['id'],b['id']],quantitative=True)).status_code,422)
    def test_exports_all_formats(self):
        self.session()
        for f in ['json','csv','markdown']:self.assertEqual(self.client.get('/api/export?format='+f).status_code,200)
    def test_unlinked_run_deletion(self):
        s=self.session();r=self.client.delete('/api/records/'+s['id'],headers={'Idempotency-Key':str(uuid.uuid4())});self.assertEqual(self.ok(r)['deleted'],1);self.assertEqual(self.ok(self.client.get('/api/records')),[])
    def test_exact_text_export_import_into_fresh_workspace(self):
        self.ok(self.post('/sessions',dict(request=self.sample['1']['request'],origin='sample')))
        text=self.client.get('/api/export').text
        with tempfile.TemporaryDirectory(prefix='future-workbench-import-') as directory:
            with TestClient(create_app(directory),base_url='http://127.0.0.1') as other:
                r=other.post('/api/import',content=text,headers={'Content-Type':'application/json','Idempotency-Key':str(uuid.uuid4())});self.assertEqual(r.status_code,200,r.text);self.assertEqual(r.json()['imported'],1)
                self.assertEqual(other.get('/api/export').json()['payload'],json.loads(text)['payload'])
    def test_advanced_compatible_study_and_matched_comparison(self):
        s=self.ok(self.post('/studies',self.forecast()));p=copy.deepcopy(s['ledger']['plan']);p['id']='second-protocol'
        other=self.ok(self.post('/studies',dict(plan=p)));self.stamp='2030-01-04T00:00:00Z'
        for v in [s,other]:self.ok(self.post(f"/studies/{v['id']}/outcome",dict(target_id='q1',status='resolved',value='0',known_at='2030-01-03T00:00:00Z',reason='Complete independent log',evidence='No event in complete observation log')))
        r=self.ok(self.post('/compare',dict(ids=[s['id'],other['id']],quantitative=True)));self.assertEqual(r['matched_count'],1);self.assertEqual(r['models'][0]['scores']['brier']['exact'],'9/25')
if __name__=='__main__':unittest.main()
