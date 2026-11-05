import copy
import json
from pathlib import Path
import re
import tempfile
import unittest
from future import geomancy as g
from future.__main__ import load_registry

F=json.loads(Path('tests/fixtures/geomancy_reference_v1.json').read_text(encoding='utf-8'))
def request(**kw):
    return dict(schema_version=1,profile=g.PROFILE,task='shield',mode='manual',input_mode='patterns',mothers=F['charts'][0]['positions'][:4])|kw

class GeomancyTests(unittest.TestCase):
    def reject(self,**kw):
        with self.assertRaises(ValueError):g.read(request(**kw))
    def test_source(self):self.assertEqual(g.DATA['source']['snapshot_sha256'],F['source']['snapshot_sha256'])
    def test_catalog(self):
        self.assertEqual(len(g.FIGURES),16)
        for f in F['figures']:self.assertEqual(g.lookup(f['pattern'])['name'],f['name'])
    def test_traditional_difference(self):
        self.assertEqual(g.lookup('Puella')['pattern'],'1211');self.assertEqual(g.lookup('Puer')['pattern'],'1121')
    def test_alias(self):
        for f in F['figures']:
            for v in [f['id'],f['name'],*f['aliases']]:self.assertEqual(g.lookup(v.upper())['id'],f['id'])
    def test_alias_not_fuzzy(self):
        for v in [' Puella','Puell','Martin Puella','']:self.assertRaises(ValueError,g.lookup,v)
    def test_published_chart(self):self.assertEqual(g.chart(F['charts'][0]['positions'][:4]),F['charts'][0]['positions'])
    def test_other_fixtures(self):
        for f in F['charts'][1:]:self.assertEqual(g.chart(f['positions'][:4]),f['positions'])
    def test_dot_array(self):self.assertEqual(g.chart([[int(x) for x in p] for p in request()['mothers']]),g.chart(request()['mothers']))
    def test_count_mode(self):
        q=request();q.pop('mothers');q.update(input_mode='mark_counts',mark_counts=[2,3,2,3,3,2,2,3,3,3,2,3,2,3,2,2]);r=g.read(q)
        self.assertEqual(r['input_mothers'],request()['mothers']);self.assertEqual(r['original_mark_counts'],q['mark_counts']);self.assertEqual(len(r['mark_parity_trace']),16)
    def test_figure_ids(self):
        q=request();q.pop('mothers');q.update(input_mode='figure_ids',figure_ids=['Acquisitio','Carcer','Puer','Rubeus']);self.assertEqual(g.read(q)['input_mothers'],request()['mothers'])
    def test_line_trace(self):
        r=g.read(request());self.assertEqual(r['positions'][4]['line_trace'][0],dict(parent=1,parent_row=1,dot_count=2))
        for p in r['positions'][8:]:
            self.assertEqual(p['parents'],F['parents'][str(p['position'])])
            for t in p['line_trace']:self.assertEqual(t['result'],1 if t['sum']%2 else 2)
    def test_layout_independent(self):
        a=g.read(request());b=g.read(request(layout='left_to_right'));self.assertEqual(a['positions'],b['positions']);self.assertEqual(a['layout']['tiers_left_to_right'][0],[8,7,6,5,4,3,2,1]);self.assertEqual(b['layout']['tiers_left_to_right'][0],list(range(1,9)))
    def test_repeated_mothers(self):self.assertEqual(g.read(request(mothers=['2121']*4))['invariants']['position_count'],15)
    def test_judge_not_prediction(self):
        r=g.read(request());self.assertTrue(r['invariants']['judge_even_total_points']);self.assertIn('not a certified',r['qualification']);self.assertNotIn('forecast',r)
    def test_catalog_task(self):
        q=dict(schema_version=1,profile=g.PROFILE,task='figure_catalog',mode='manual');r=g.read(q);self.assertEqual(len(r['figure_catalog']),16);self.assertIsNone(r['judge']);self.assertEqual(r['positions'],[])
    def test_lookup_task(self):
        q=dict(schema_version=1,profile=g.PROFILE,task='figure_catalog',mode='manual',lookup=['Way','Puella','1121']);self.assertEqual([f['id'] for f in g.read(q)['figure_catalog']],['via','puella','puer'])
    def test_raw_unicode(self):
        s='  Café Café\r\n猫\t `````json  ';q=request(question=s,commentary=s,association=s);r=g.read(q);self.assertEqual(r['replay']['request'],q);self.assertEqual(r['user_text']['question'],s)
    def test_raw_hash_and_copy(self):
        q=request(question='x');r=g.read(q);q['mothers'][0]='1111';self.assertNotEqual(r['replay']['request'],q);self.assertNotEqual(g.read(request(question=' x'))['replay']['input_sha256'],r['replay']['input_sha256'])
    def test_markdown_replay(self):
        r=g.read(request(question='`````json\n猫'));s=g.markdown(r);m=re.search(r'(`{3,})json\n(.*?)\n\1',s.split('## Exact replay metadata')[1],re.S);self.assertEqual(g.read(json.loads(m[2])['request']),r)
    def test_profile_immutable(self):
        with self.assertRaises(TypeError):g.DATA['profile']='other'
        r=g.read(request());r['source']['edition']='other';self.assertNotEqual(g.DATA['source']['edition'],'other')
    def test_registry_idempotent(self):
        r=load_registry()
        try:g.register_knowledge(r);g.register_knowledge(r);self.assertEqual(r.db.execute("select count(*) from rules where id like 'geomancy.%'").fetchone()[0],17)
        finally:r.close()
    def test_bad_schema(self):self.reject(schema_version=True)
    def test_bad_profile(self):self.reject(profile='greer')
    def test_bad_convention(self):self.reject(figure_convention='universal')
    def test_bad_layout(self):self.reject(layout='clockwise')
    def test_bad_task(self):
        for task in ['house_chart','horary_judgment']:self.reject(task=task)
    def test_no_seed(self):self.reject(seed='x')
    def test_no_sixteenth(self):self.reject(super_judge=True)
    def test_bad_mode(self):self.reject(mode='seeded')
    def test_bad_patterns(self):
        for p in ['121','12121','1231',1211,[1,2,True,1],[1,2,1.0,1]]:self.reject(mothers=[p]*4)
    def test_bad_mother_count(self):self.reject(mothers=['1111']*3)
    def test_mixed_input(self):self.reject(mark_counts=[1]*16)
    def test_invalid_counts(self):
        q=request();q.pop('mothers');q.update(input_mode='mark_counts')
        for n in [0,-1,True,1.0,1000001,'3',None]:
            with self.assertRaises(ValueError):g.read(q|dict(mark_counts=[n]*16))
        with self.assertRaises(ValueError):g.read(q|dict(mark_counts=[1]*15))
    def test_bad_unknown_ids(self):
        q=request();q.pop('mothers');q.update(input_mode='figure_ids',figure_ids=['not-a-figure']*4)
        with self.assertRaises(ValueError):g.read(q)
    def test_bad_text(self):
        for s in ['x'*10001,'\0','\ud800',3]:self.reject(question=s)
    def test_catalog_mixed(self):self.reject(task='figure_catalog')
    def test_strict_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d,'q.json')
            for text in ['{"mode":"manual","mode":"manual"}','{"n":NaN}','{"n":Infinity}']:
                p.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):g.load_input(p)
    def test_invalid_root(self):
        for v in [None,[],1,'x']:
            with self.assertRaises(ValueError):g.read(v)

if __name__=='__main__':unittest.main()
