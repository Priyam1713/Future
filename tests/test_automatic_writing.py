import copy
import json
from pathlib import Path
import tempfile
import unittest
from future import automatic_writing as a
from future.__main__ import load_registry

REF = json.loads(Path('tests/fixtures/automatic_writing_reference.json').read_text(encoding='utf-8'))


def event(kind, i=0, **payload):
    return dict(id='e'+str(i), type=kind, **payload)


def base(events=None, state='prepared', **kwargs):
    return dict(schema_version=1, profile=a.PROFILE, task='guided_writing', mode='manual',
                session_id='example', state=state, events=events or []) | kwargs


def log(kinds):
    result=[];order=0;parent='first_draft';rev=0
    for i,kind in enumerate(kinds):
        e=event(kind,i)
        if kind=='append':
            order+=1;e['segment']=dict(id='s'+str(order),order=order,text='one',authorship='user')
        if kind=='revise':
            rev+=1;e['revision']=dict(id='r'+str(rev),parent=parent,text='Edited.',authorship='user');parent='r'+str(rev)
        result.append(e)
    return result


class AutomaticWritingTests(unittest.TestCase):
    def test_01_independent_source_facts(self):
        self.assertEqual(a.DATA['source']['id'],REF['source_id'])
        self.assertEqual([(r['id'].split('.')[-1],r['statement']) for r in a.DATA['rules']],[(r['id'],r['meaning']) for r in REF['rules']])
        self.assertIn('underlying',a.DATA['source']['edition'].lower())
        self.assertIn('not authenticated',a.DATA['source']['edition'])

    def test_02_independent_metric_vectors(self):
        for row in REF['metrics']:
            events=log(['begin']+['append']*len(row['segments'])+['stop'])
            for e,text in zip(events[1:],row['segments']):e['segment']['text']=text
            r=a.read(base(events,'stopped'))
            self.assertEqual(r['first_draft']['text'],row['draft'])
            self.assertEqual([r['metrics'][k] for k in ('unicode_code_points','words','lines')],[row['code_points'],row['words'],row['lines']])

    def test_03_pre_engine_valid_transitions(self):
        for row in REF['transitions']:self.assertEqual(a.read(base(log(row['events']),row['state']))['session']['state'],row['state'])

    def test_04_pre_engine_invalid_transitions(self):
        for kinds in REF['invalid']:
            with self.assertRaises(ValueError):a.read(base(log(kinds)))

    def test_05_all_declared_states(self):
        for state,kinds in [('prepared',[]),('writing',['begin']),('paused',['begin','pause']),('resumed',['begin','pause','resume']),('stopped',['stop']),('under_review',['stop','review']),('completed',['stop','complete'])]:
            self.assertEqual(a.read(base(log(kinds),state))['session']['state'],state)

    def test_06_exact_concatenation(self):
        e=log(['begin','append','append','stop']);e[2]['segment']['text']='two'
        self.assertEqual(a.read(base(e,'stopped'))['first_draft']['text'],'onetwo')

    def test_07_independent_revision_chain(self):
        e=log(['begin','append','append','stop','review','revise','revise','complete']);e[2]['segment']['text']='two'
        for item,row in zip(e[5:7],REF['revisions']['rows']):item['revision']=row|dict(authorship='user')
        r=a.read(base(e,'completed'));self.assertEqual(r['first_draft']['text'],'onetwo')
        self.assertEqual([x['record']['text'] for x in r['revisions']],['One two.','One, two.'])
        self.assertEqual(r['revisions'][0]['parent_sha256'],r['first_draft']['content_sha256'])

    def test_08_parent_must_exist_and_be_latest(self):
        for parent in ('unknown','first_draft'):
            e=log(['stop','review','revise','revise']);e[-1]['revision']['parent']=parent
            with self.assertRaises(ValueError):a.read(base(e,'under_review'))

    def test_09_duplicate_identifiers(self):
        for what in ('event','segment','revision'):
            e=log(['begin','append','append','stop','review','revise','revise'])
            if what=='event':e[1]['id']=e[0]['id']
            elif what=='segment':e[2]['segment']['id']=e[1]['segment']['id']
            else:e[-1]['revision']['id']=e[-2]['revision']['id']
            with self.assertRaises(ValueError):a.read(base(e,'under_review'))

    def test_10_orders_not_sorted(self):
        for order in (1,0,True,1.5):
            e=log(['begin','append','append']);e[2]['segment']['order']=order
            with self.assertRaises(ValueError):a.read(base(e,'writing'))

    def test_11_review_policy(self):
        with self.assertRaises(ValueError):a.read(base(log(['stop','review']),'under_review',review_policy='no_review'))
        with self.assertRaises(ValueError):a.read(base(log(['stop','complete']),'completed',review_policy='required'))
        self.assertEqual(a.read(base(log(['stop','review','complete']),'completed',review_policy='required'))['session']['state'],'completed')

    def test_12_immutable_isolation(self):
        q=base(log(['begin','append','stop','review','revise']),'under_review');snapshot=copy.deepcopy(q);r=a.read(q)
        q['events'][1]['segment']['text']='changed';self.assertEqual(r['first_draft']['text'],'one')
        r['replay']['request']['events'][1]['segment']['text']='again'
        self.assertEqual(r['original_segments'][0]['record']['text'],'one')
        self.assertEqual(a.read(snapshot)['first_draft']['text'],'one')

    def test_13_optional_text_and_omissions(self):
        q=base(intention=None,comments='',associations=['  ','猫'],constraints=['My choice'])
        r=a.read(q);self.assertEqual(r['session']['user_record'],{k:q[k] for k in ('intention','comments','associations','constraints')})
        self.assertNotIn('start_time',r['session']['user_record'])

    def test_14_duration_offset_vector(self):
        row=REF['duration'];self.assertEqual(a.interval(row['start'],row['stop'])['seconds'],10)
        self.assertEqual(a.interval('2026-11-04T10:00:00Z','2026-11-04T10:00:10.000001Z')['microseconds'],10000001)
        e=log(['begin','stop']);e[0]['timestamp']=row['start'];e[1]['timestamp']=row['stop']
        self.assertEqual(a.read(base(e,'stopped'))['metrics']['duration']['seconds'],10)

    def test_15_unavailable_timing(self):
        for x,y in [(None,None),('2026-11-04','2026-11-05'),('2026-11-04T10:00:00','2026-11-04T10:00:10Z')]:
            self.assertIsNone(a.interval(x,y)['seconds'])
        self.assertIsNone(a.read(base())['metrics']['declared_segment_seconds'])

    def test_16_timestamp_order(self):
        e=log(['begin','stop']);e[0]['timestamp']='2026-11-04T10:00:10Z';e[1]['timestamp']='2026-11-04T10:00:00Z'
        with self.assertRaises(ValueError):a.read(base(e,'stopped'))
        with self.assertRaises(ValueError):a.interval(e[0]['timestamp'],e[1]['timestamp'])

    def test_17_segment_timestamps(self):
        e=log(['begin','append']);e[1]['timestamp']='2026-11-04T10:00:00Z';e[1]['segment']['timestamp']='2026-11-04T10:00:01Z'
        with self.assertRaises(ValueError):a.read(base(e,'writing'))
        e[1].pop('timestamp');self.assertEqual(a.read(base(e,'writing'))['original_segments'][0]['record']['timestamp'],'2026-11-04T10:00:01Z')

    def test_18_segment_intervals(self):
        e=log(['begin','append','append']);e[1]['segment']['elapsed_seconds']=3;e[2]['segment']['elapsed_seconds']=7
        self.assertEqual(a.read(base(e,'writing'))['metrics']['declared_segment_seconds'],10)
        for bad in (-1,True,1.5,604801):
            e[1]['segment']['elapsed_seconds']=bad
            with self.assertRaises(ValueError):a.read(base(e,'writing'))

    def test_19_invalid_timestamps(self):
        for bad in ('now','2026-02-30','2026-11-04T10:00:00+99:00'):
            with self.assertRaises(ValueError):a.read(base(start_time=bad))

    def test_20_payload_separation(self):
        for bad in [event('begin',segment={}),event('revise'),event('append',revision={})]:
            with self.assertRaises(ValueError):a.read(base([bad],'writing'))

    def test_21_authorship_is_explicit(self):
        for kind in ('segment','revision'):
            e=log(['begin','append','stop','review','revise']);row=e[1]['segment'] if kind=='segment' else e[-1]['revision'];row['authorship']='spirit'
            with self.assertRaises(ValueError):a.read(base(e,'under_review'))

    def test_22_no_unrequested_inference(self):
        e=log(['begin','append']);e[1]['segment']['text']='A spirit predicts I am anxious.'
        r=a.read(base(e,'writing'));self.assertEqual(r['first_draft']['text'],e[1]['segment']['text'])
        self.assertIn('unsupported',r['evidence_layers']);self.assertFalse(r['replay']['generated_text'])

    def test_23_strict_schema(self):
        for q in (base(seed=0),base(profile='Moses'),base(mode='llm'),base(schema_version=True),base(state=[]),base(session_id='../file')):
            with self.assertRaises(ValueError):a.read(q)

    def test_24_raw_text_validation(self):
        for bad in ('\ud800','a\x00b',None,'x'*20001):
            e=log(['begin','append']);e[1]['segment']['text']=bad
            with self.assertRaises(ValueError):a.read(base(e,'writing'))

    def test_25_report_json_markdown_replay(self):
        q=base(log(['begin','append','stop']),'stopped');r=a.read(q);md=a.markdown(r)
        replay=json.loads(md.split('## Exact replay metadata')[1].split('```json\n')[1].split('\n```')[0])
        self.assertEqual(a.read(replay['request']),json.loads(json.dumps(r)))
        self.assertEqual(a.read(q),a.read(q))

    def test_26_fences_and_literal_unicode(self):
        e=log(['begin','append']);text='```\r\n猫 Café🐍\n';e[1]['segment']['text']=text
        md=a.markdown(a.read(base(e,'writing')))
        encoded=md.split('## Original first draft')[1].split('````json\n')[1].split('\n````')[0]
        self.assertEqual(json.loads(encoded),text)

    def test_27_profile_frozen_and_hash_portable(self):
        with self.assertRaises(TypeError):a.DATA['version']=2
        self.assertEqual(a.digest({'猫':1,'a':2}),a.digest({'a':2,'猫':1}))
        self.assertEqual(a.PROFILE_HASH,a.digest(a.thaw(a.DATA)))

    def test_28_registry_scope(self):
        r=load_registry()
        try:
            a.read(base(),r)
            rows=r.db.execute('SELECT record FROM rules WHERE id LIKE ?',('automatic.breton.%',)).fetchall()
            self.assertEqual(len(rows),7)
            self.assertTrue(all(json.loads(x[0])['status']=='proposed' for x in rows))
        finally:r.close()

    def test_29_strict_file_loader(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d,'q.json');p.write_text('{"a":1,"a":2}',encoding='utf-8')
            with self.assertRaises(ValueError):a.load_input(p)

    def test_30_bounds_and_empty_discontinued(self):
        self.assertEqual(a.read(base(log(['stop']),'stopped'))['first_draft']['text'],'')
        e=log(['stop','review']+['revise']*33)
        with self.assertRaises(ValueError):a.read(base(e,'under_review'))
        with self.assertRaises(ValueError):a.read(base(events=[event('begin',i) for i in range(513)]))


if __name__=='__main__':unittest.main()
