import json
import unittest
from pathlib import Path
from fastapi.testclient import TestClient
from future.natal import SkyfieldEphemeris, Settings, chart
from future.core_readings import placements
from future.knowledge import Registry
from fate.api import create_app
from fate.western import WesternInput, WesternService, search_places

ROOT=Path(__file__).resolve().parents[2]
Q=dict(local='1990-07-15T14:30:00',zone='Europe/London',latitude=51.50853,longitude=-0.12574,houses='whole-sign',fold=None)


class WesternTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine=SkyfieldEphemeris(ROOT/'data/de440s.bsp')

    @classmethod
    def tearDownClass(cls):
        cls.engine.kernel.close()

    def setUp(self):
        self.prompts=[]
        def provider(prompt):
            self.prompts.append(prompt)
            parts=json.loads(prompt.split('DATA: ')[1])
            return dict(themes=[dict(id=p['id'],reflection=p['text']) for p in parts]),dict(provider='test',model='fixture')
        self.client=TestClient(create_app(provider=provider,signing_key=b'western-fixture'))
        self.client.__enter__()

    def tearDown(self):
        self.client.__exit__(None,None,None)

    def test_native_parity_full_chart_and_existing_composition(self):
        r=self.client.post('/api/western',json=Q)
        self.assertEqual(r.status_code,200)
        expected=chart(self.engine,Q['local'],Q['zone'],Q['latitude'],Q['longitude'])
        registry=Registry()
        try:expected['reading']=placements(expected,registry)
        finally:registry.close()
        self.assertEqual(r.json()['result'],json.loads(json.dumps(expected)))
        self.assertEqual(expected['birth']['utc'],'1990-07-15T13:30:00+00:00')
        self.assertEqual(expected['planets']['Sun']['sign'],'Cancer')
        self.assertEqual(r.headers['cache-control'],'no-store')

    def test_different_real_input_changes_chart_not_calculation(self):
        a=self.client.post('/api/western',json=Q).json()['result']
        b=self.client.post('/api/western',json={**Q,'local':'1990-07-15T18:30:00','latitude':-33.8688,'longitude':151.2093,'zone':'Australia/Sydney'}).json()['result']
        self.assertNotEqual(a['angles'],b['angles'])
        self.assertNotEqual(a['planets']['Moon']['longitude'],b['planets']['Moon']['longitude'])
        self.assertEqual(len(b['planets']),10)

    def test_dst_gap_rejected_and_repeated_time_needs_choice(self):
        for local,fragment in [('2024-03-10T02:30:00','Nonexistent'),('2024-11-03T01:30:00','Ambiguous')]:
            r=self.client.post('/api/western',json={**Q,'local':local,'zone':'America/New_York'})
            self.assertEqual(r.status_code,422);self.assertIn(fragment,r.json()['detail'])
        a=self.client.post('/api/western',json={**Q,'local':'2024-11-03T01:30:00','zone':'America/New_York','fold':0}).json()['result']
        b=self.client.post('/api/western',json={**Q,'local':'2024-11-03T01:30:00','zone':'America/New_York','fold':1}).json()['result']
        self.assertEqual(a['birth']['utc'],'2024-11-03T05:30:00+00:00')
        self.assertEqual(b['birth']['utc'],'2024-11-03T06:30:00+00:00')

    def test_no_offset_or_unknown_zone_or_missing_time(self):
        for q in [{**Q,'local':'1990-07-15T14:30:00+01:00'},{**Q,'zone':'Mars/Here'},{**Q,'local':'1990-07-15'},{k:v for k,v in Q.items() if k!='local'}]:
            self.assertEqual(self.client.post('/api/western',json=q).status_code,422)

    def test_strict_bounds_extra_fields_and_boolean_fold(self):
        for key,value in [('latitude',90),('latitude',-90),('longitude',181),('fold',True),('fold','0'),('houses','sidereal'),('name','Private')]:
            self.assertEqual(self.client.post('/api/western',json={**Q,key:value}).status_code,422,(key,value))

    def test_polar_quadrants_rejected_without_fallback(self):
        q={**Q,'latitude':75,'houses':'placidus'}
        r=self.client.post('/api/western',json=q)
        self.assertEqual(r.status_code,422)
        r=self.client.post('/api/western',json={**q,'houses':'whole-sign'})
        self.assertEqual(r.status_code,200);self.assertEqual(r.json()['result']['settings']['houses'],'whole-sign')

    def test_supported_house_systems_preserve_native_geometry(self):
        for system in ['equal','porphyry','placidus','regiomontanus','campanus']:
            r=self.client.post('/api/western',json={**Q,'houses':system}).json()['result']
            n=chart(self.engine,Q['local'],Q['zone'],Q['latitude'],Q['longitude'],Settings(houses=system))
            self.assertEqual(r['house_cusps'],n['house_cusps'])
            self.assertEqual(r['aspects'],n['aspects'])

    def test_ephemeris_bounds_real_dates_and_historical_offsets(self):
        for local in ['1849-12-30T14:00:00','2150-01-02T14:00:00','2000-02-30T14:00:00']:
            self.assertEqual(self.client.post('/api/western',json={**Q,'local':local}).status_code,422)
        r=self.client.post('/api/western',json={**Q,'local':'1900-01-01T12:00:00','zone':'Asia/Kolkata'}).json()['result']
        self.assertEqual(r['birth']['utc'],'1900-01-01T06:38:50+00:00')

    def test_places_are_real_disambiguated_points_not_inferred_defaults(self):
        hits=search_places('London GB')
        london=next(r for r in hits if r['id']==2643743)
        self.assertEqual(london['zone'],'Europe/London')
        self.assertEqual(london['latitude'],51.50853)
        self.assertEqual(search_places(''),[])
        r=self.client.post('/api/western/places',json={'query':'Mumbai IN'})
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json()['places'][0]['zone'],'Asia/Kolkata')
        self.assertEqual(self.client.post('/api/western/places',json={'query':'London','latitude':2}).status_code,422)

    def test_consent_receipt_and_private_input_exclusion(self):
        env=self.client.post('/api/western',json=Q).json()
        self.assertEqual(self.prompts,[])
        for consent in [False,'true',1,None]:
            r=self.client.post('/api/western/explain',json={'draw':Q,'receipt':env['receipt'],'cloud_consent':consent})
            self.assertEqual(r.status_code,422)
        self.assertEqual(self.client.post('/api/western/explain',json={'draw':{**Q,'longitude':10},'receipt':env['receipt'],'cloud_consent':True}).status_code,403)
        r=self.client.post('/api/western/explain',json={'draw':Q,'receipt':env['receipt'],'cloud_consent':True})
        self.assertEqual(r.status_code,200)
        prompt=self.prompts[0]
        for private in [Q['local'],Q['zone'],str(Q['latitude']),str(Q['longitude']),'receipt','birth']:
            self.assertNotIn(private,prompt)
        self.assertEqual(r.json()['coverage'],'experimental_ai_commentary')

    def test_provider_mismatch_never_replaces_native(self):
        with TestClient(create_app(provider=lambda prompt:({'themes':[]},{}))) as c:
            env=c.post('/api/western',json=Q).json()
            r=c.post('/api/western/explain',json={'draw':Q,'receipt':env['receipt'],'cloud_consent':True})
            self.assertEqual(r.status_code,422)
            self.assertEqual(c.post('/api/western',json=Q).json()['result'],env['result'])

    def test_frozen_western_reference_matches_existing_source_records(self):
        from future.core_readings import DATA
        rs=json.loads((ROOT/'knowledge/western_rules.json').read_text())+DATA['records']
        expected=[r for r in rs if r['tradition']=='modern psychological' and r['kind'] in ('planet','planet_symbol','sign','house','aspect')]
        archive=json.loads((ROOT/'fate/web/src/astrology/reference-v1.json').read_text())
        self.assertEqual(archive['records'],expected)
        self.assertEqual(len(expected),32)


if __name__=='__main__':unittest.main()
