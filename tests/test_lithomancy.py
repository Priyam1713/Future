import copy,json,re,tempfile,unittest
from pathlib import Path
from future import lithomancy as l
from future.__main__ import load_registry

F=json.loads(Path('tests/fixtures/lithomancy_reference_v1.json').read_text(encoding='utf-8'))
def stone(id,role,x=0,y=0,**kw):return dict(id=id,role_id=role,position=dict(x=x,y=y))|kw
def request(**kw):
    return dict(schema_version=1,profile=l.PROFILE,task='manual_spatial_reading',mode='manual',reading_id='test',frame=l.FRAMES[0],coverage='subset',origin='hypothetical',
        stones=[stone('self','lodestone'),stone('onyx','onyx',3,4),stone('tiger','tigers_eye',1,0),stone('coin','five_pence_coin',-1,0),stone('glass','sea_glass',0,-2)],anchor=dict(kind='personal_stone',stone_id='self'))|kw

class LithomancyTests(unittest.TestCase):
    def reject(self,**kw):
        with self.assertRaises(ValueError):l.read(request(**kw))
    def test_source_identity(self):self.assertEqual(l.thaw(l.DATA['source']),F['source'])
    def test_all_roles(self):
        self.assertEqual(len(l.ROLES),12)
        for r in F['roles']:self.assertEqual(l.thaw(l.ROLES[r['role_id']]),r)
    def test_example_not_universal(self):
        r=l.read(request());self.assertIn('not universal',r['set_coverage']['kind']);self.assertFalse(r['set_coverage']['generated_missing_objects'])
    def test_association_present(self):
        r=l.read(request());self.assertEqual(r['source_priority']['nearest_known'][0]['source_association']['association'],l.ROLES['five_pence_coin']['association'])
    def test_exact_distance(self):self.assertEqual(l.distance_squared(dict(x=3,y=4),dict(x=0,y=0)),25)
    def test_limit_distance(self):self.assertEqual(l.distance_squared(dict(x=-1000000,y=-1000000),dict(x=1000000,y=1000000)),8000000000000)
    def test_nearest_tie(self):
        r=l.read(request());self.assertEqual(r['spatial']['nearest_known'],['coin','tiger']);self.assertEqual(r['source_priority']['status'],'applicable')
    def test_farthest_not_discarded(self):
        r=l.read(request());self.assertEqual(r['spatial']['farthest_known'],['onyx']);self.assertIn('distant',r['source_policy']['exceptions'].lower())
    def test_personal_anchor_excluded(self):self.assertNotIn('self',[r['id'] for r in l.read(request())['spatial']['distances']])
    def test_reader_anchor(self):
        r=l.read(request(anchor=dict(kind='reader',position=dict(x=0,y=0))));self.assertEqual(r['spatial']['nearest_known'],['self']);self.assertEqual(len(r['spatial']['distances']),5)
    def test_explicit_other_personal(self):
        r=l.read(request(anchor=dict(kind='personal_stone',stone_id='coin')));self.assertEqual(r['anchor']['excluded_instance_id'],'coin');self.assertEqual(r['placements'][3]['source_role']['role_id'],'five_pence_coin')
    def test_no_anchor(self):
        q=request();q.pop('anchor');r=l.read(q);self.assertEqual(r['source_priority']['status'],'insufficient_evidence');self.assertEqual(r['spatial']['nearest_known'],[])
    def test_unknown_anchor(self):
        q=request();q['stones'][0]['position']=None;r=l.read(q);self.assertFalse(r['spatial']['anchor_position_known']);self.assertEqual(r['source_priority']['scope'],'unavailable')
    def test_unknown_reader(self):self.assertEqual(l.read(request(anchor=dict(kind='reader',position=None)))['source_priority']['status'],'insufficient_evidence')
    def test_unknown_stone(self):
        q=request();q['stones'][1].pop('position');r=l.read(q);self.assertEqual(r['spatial']['unknown_positions'],['onyx']);self.assertEqual(r['source_priority']['status'],'partial_evidence');self.assertEqual(r['source_priority']['scope'],'known_positions_only')
    def test_only_anchor(self):
        r=l.read(request(stones=[stone('self','lodestone')]));self.assertEqual(r['source_priority']['status'],'insufficient_evidence')
    def test_coincident_centers(self):
        q=request();q['stones'][1]['position']=dict(x=0,y=0);r=l.read(q);self.assertEqual(r['spatial']['nearest_known'],['onyx']);self.assertIn(['self','onyx'],r['coincident_centers'])
    def test_display_frame(self):
        a=l.read(request());b=l.read(request(frame=l.FRAMES[1]));self.assertEqual(a['spatial']['ordered_distance_groups'],b['spatial']['ordered_distance_groups']);self.assertEqual(a['spatial']['distances'][0]['direction'],['right','above']);self.assertEqual(b['spatial']['distances'][0]['direction'],['right','below'])
    def test_source_meaning_frame_invariant(self):
        a=l.read(request());b=l.read(request(frame=l.FRAMES[1]));self.assertEqual(a['source_priority']['nearest_known'],b['source_priority']['nearest_known']);self.assertIsNone(a['editorial_synthesis']['combined_fortune'])
    def test_uncertainty(self):self.assertEqual(l.read(request(uncertainty=True))['source_priority']['status'],'uncertain_evidence')
    def test_groups_user_only(self):
        r=l.read(request(groups=[dict(id='g',members=['coin','tiger'],association='mine')]));self.assertIn('unsupported',r['declared_groups'][0]['interpretation']);self.assertEqual(r['declared_groups'][0]['declaration']['association'],'mine')
    def test_qualitative_conflict(self):
        r=l.read(request(relations=[dict(**{'from':'onyx','to':'self'},relation='left')]));self.assertEqual(r['source_priority']['status'],'conflicting_evidence');self.assertEqual(r['placements'][1]['declaration']['position'],dict(x=3,y=4))
    def test_qualitative_consistent(self):self.assertEqual(l.read(request(relations=[dict(**{'from':'onyx','to':'self'},relation='above')]))['declared_relation_checks'][0]['status'],'consistent')
    def test_near_unquantified(self):self.assertEqual(l.read(request(relations=[dict(**{'from':'onyx','to':'self'},relation='near')]))['declared_relation_checks'][0]['status'],'unquantified_user_declaration')
    def test_full_set(self):
        q=request(coverage='full_example',stones=[stone('s'+str(i),r['role_id'],i,2*i) for i,r in enumerate(F['roles'])],anchor=dict(kind='personal_stone',stone_id='s0'));self.assertEqual(l.read(q)['set_coverage']['missing_roles'],[])
    def test_raw_unicode(self):
        text='  Café Café\r\n猫\t `````json  ';q=request(question=text,commentary=text);q['stones'][1]['association']=text;r=l.read(q);self.assertEqual(r['replay']['request'],q);self.assertEqual(r['placements'][1]['declaration']['association'],text)
    def test_replay_and_digest(self):
        r=l.read(request(question='x'));self.assertEqual(l.read(r['replay']['request']),r);self.assertNotEqual(r['replay']['input_sha256'],l.read(request(question=' x'))['replay']['input_sha256'])
    def test_markdown_replay(self):
        r=l.read(request(question='`````json\n猫'));text=l.markdown(r);m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);self.assertEqual(l.read(json.loads(m[2])['request']),r)
    def test_immutable(self):
        with self.assertRaises(TypeError):l.DATA['profile']='x'
        q=request();r=l.read(q);q['stones'][1]['role_id']='x';self.assertEqual(r['placements'][1]['declaration']['role_id'],'onyx')
    def test_registry(self):
        r=load_registry()
        try:l.register_knowledge(r);l.register_knowledge(r);self.assertEqual(r.db.execute("select count(*) from rules where id like 'lithomancy.%'").fetchone()[0],14)
        finally:r.close()
    def test_full_missing(self):self.reject(coverage='full_example')
    def test_duplicate_id(self):
        q=request();q['stones'][1]['id']='self';self.reject(stones=q['stones'])
    def test_duplicate_role(self):
        q=request();q['stones'][1]['role_id']='lodestone';self.reject(stones=q['stones'])
    def test_unknown_role(self):
        for role in ['Sun','wimmer.life',None,{}]:self.reject(stones=[stone('self',role)])
    def test_bad_coordinates(self):
        for n in [True,False,0.1,'1',None,1000001,-1000001]:self.reject(stones=[stone('self','lodestone',n,0)])
    def test_partial_position(self):self.reject(stones=[dict(id='self',role_id='lodestone',position=dict(x=0))])
    def test_contradictory_anchor(self):self.reject(anchor=dict(kind='personal_stone',stone_id='self',position=dict(x=0,y=0)))
    def test_missing_anchor_reference(self):self.reject(anchor=dict(kind='personal_stone',stone_id='missing'))
    def test_bad_group(self):self.reject(groups=[dict(id='x',members=['self','missing'])])
    def test_duplicate_group(self):self.reject(groups=[dict(id='x',members=['self','onyx'])]*2)
    def test_bad_relation(self):self.reject(relations=[dict(**{'from':'self','to':'missing'},relation='left')])
    def test_unsupported(self):
        for field,value in [('seed','x'),('circle_radius',3),('cluster_radius',2),('viewpoint','north'),('arrow_bearing',90)]:self.reject(**{field:value})
    def test_wrong_frame_mode_schema(self):
        for key,value in [('frame','cup-handle'),('mode','seeded'),('schema_version',True),('profile','wimmer'),('reading_id',''),('coverage','auto')]:self.reject(**{key:value})
    def test_invalid_text(self):
        for value in ['x'*10001,'\0','\ud800',3]:self.reject(question=value)
    def test_no_inference(self):
        q=request(commentary='all stones are at0,0');q['stones'][1]['position']=None;self.assertIsNone(l.read(q)['placements'][1]['declaration']['position'])
    def test_json_strict(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d,'q.json')
            for text in ['{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}']:
                p.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):l.load_input(p)

if __name__=='__main__':unittest.main()
