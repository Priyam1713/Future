import unittest,json
from pathlib import Path
from datetime import datetime,timedelta,timezone
from future.releasing import release,periods,from_natal,register_knowledge,KNOWLEDGE
from future.natal import SkyfieldEphemeris,chart,Settings

UTC=timezone.utc

class ReleasingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f=json.loads(Path('tests/fixtures/releasing_reference.json').read_text())
        cls.birth=datetime(2000,1,1,tzinfo=UTC)
    def test_published_valens_gemini_sequence_and_truncation(self):
        f=self.f['published_examples'][0]
        rows=list(periods(2,self.birth,self.birth+timedelta(days=7200),2))
        self.assertEqual([r[0] for r in rows],f['child_signs'])
        self.assertEqual([(r[2]-r[1]).total_seconds()/86400/30 for r in rows],f['child_months'])
        self.assertEqual((rows[12][1]-self.birth).days,f['bond_elapsed_days'])
        self.assertEqual([i for i,r in enumerate(rows) if r[4]],[12])
        self.assertGreater(rows[-1][3],rows[-1][2])
    def test_published_diana_absolute_bond_date(self):
        f=self.f['published_examples'][1];birth=datetime.fromisoformat(f['birth_utc'])
        rows=list(periods(f['fortune_sign'],birth,birth+timedelta(days=80*360),1))
        virgo=rows[1];self.assertEqual(virgo[0],5)
        self.assertEqual(virgo[1].date().isoformat(),f['l1_following_start_date'])
        bond=next(r for r in periods(virgo[0],virgo[1],virgo[2],2) if r[4])
        self.assertEqual(bond[0],11);self.assertEqual(bond[1].date().isoformat(),f['bond_date'])
    def test_lower_level_published_units_and_single_bond(self):
        f=self.f['lower_level_table']
        for level,sign,hours in [(3,0,900),(4,0,75),(4,1,40),(4,4,95),(4,9,135),(4,10,150)]:
            first=next(periods(sign,self.birth,self.birth+timedelta(days=1000),level))
            self.assertEqual((first[3]-first[1]).total_seconds()/3600,hours)
        for level,hours in [(3,12660),(4,1055)]:
            # Aquarius parent lasts 30 units, so has room for a full child circuit.
            parent_duration=timedelta(days=900 if level==3 else 75)
            rows=list(periods(10,self.birth,self.birth+parent_duration,level))
            bonds=[r for r in rows if r[4]]
            self.assertEqual(len(bonds),1);self.assertEqual(bonds[0][0],4)
            self.assertEqual((bonds[0][1]-self.birth).total_seconds()/3600,hours)
            # Long parents return to their initial sign without a second jump.
            self.assertEqual(sum(r[0]==10 for r in rows),2)
    def test_nested_coverage_boundaries_and_no_lost_periods(self):
        start=self.birth+timedelta(days=7000);end=start+timedelta(days=366)
        r=release(self.birth,10,65,start,end)
        by_id={p['id']:p for p in r['periods']}
        self.assertEqual(len(by_id),len(r['periods']))
        for level in range(1,5):
            rows=sorted([p for p in r['periods'] if p['level']==level],key=lambda p:p['visible_start_utc'])
            self.assertEqual(rows[0]['visible_start_utc'],start.isoformat())
            self.assertEqual(rows[-1]['visible_end_exclusive_utc'],end.isoformat())
            for a,b in zip(rows,rows[1:]):self.assertEqual(a['visible_end_exclusive_utc'],b['visible_start_utc'])
            for p in rows:
                if level>1:
                    parent=by_id[p['parent_id']]
                    self.assertGreaterEqual(p['start_inclusive_utc'],parent['start_inclusive_utc'])
                    self.assertLessEqual(p['end_exclusive_utc'],parent['end_exclusive_utc'])
        # Exact boundary belongs solely to the next period, including a leap-year epoch.
        boundary=self.birth+timedelta(days=20*360)
        r=release(self.birth,10,65,boundary,boundary+timedelta(seconds=1),levels=1)
        self.assertEqual(len(r['periods']),1);self.assertEqual(r['periods'][0]['sign'],'Cancer')
    def test_same_sign_spirit_adjustment_and_fortune_reference(self):
        args=(self.birth,359.99,330,self.birth,self.birth+timedelta(days=1))
        s=release(*args,lot='Spirit');f=release(*args,lot='Fortune')
        self.assertEqual(s['starting_sign'],'Aries');self.assertTrue(s['spirit_shifted_one_sign'])
        self.assertEqual(f['starting_sign'],'Pisces');self.assertFalse(f['spirit_shifted_one_sign'])
        self.assertEqual(s['lots']['fortune_reference_sign'],'Pisces')
        self.assertIsNone(f['periods'][0]['symbolic_peak'])
        for spirit,place,peak in [(90,4,True),(30,2,False),(210,8,False),(270,10,True)]:
            x=release(self.birth,0,spirit,self.birth,self.birth+timedelta(seconds=1),levels=1)
            self.assertEqual(x['periods'][0]['fortune_whole_sign_place'],place)
            self.assertEqual(x['periods'][0]['symbolic_peak'],peak)
        self.assertEqual(release(*args),release(*args))
    def test_registry_input_and_tradition_isolation(self):
        from future.__main__ import load_registry
        r=load_registry()
        try:
            register_knowledge(r);register_knowledge(r)
            self.assertEqual(r.db.execute("select count(*) from rules where id like 'zr.%'").fetchone()[0],6)
        finally:r.close()
        args=(self.birth,0,60,self.birth,self.birth+timedelta(days=1))
        for kwargs in ({'profile':'valens-riley-iv10-calendar'},{'lot':'Eros'},{'levels':5},{'levels':True}):
            with self.assertRaises(ValueError):release(*args,**kwargs)
        for fortune in (-1,360,float('nan'),True):
            with self.assertRaises(ValueError):release(self.birth,fortune,0,self.birth,self.birth+timedelta(days=1))
        with self.assertRaises(ValueError):release(self.birth.replace(tzinfo=None),0,0,self.birth,self.birth+timedelta(days=1))
        with self.assertRaises(ValueError):release(self.birth,0,0,self.birth,self.birth+timedelta(days=2000))
        with self.assertRaises(ValueError):release(self.birth,0,0,self.birth-timedelta(days=1),self.birth)
        with self.assertRaises(ValueError):from_natal(None,{'settings':{'tradition':'modern psychological'}},self.birth,self.birth+timedelta(days=1))
    def test_july_example_and_published_diana_lot(self):
        e=SkyfieldEphemeris('data/de440s.bsp')
        try:
            n=chart(e,'1990-07-15T14:30','Asia/Kolkata',28.6139,77.209,Settings(tradition='Hellenistic'))
            r=from_natal(e,n,datetime(2026,11,2,tzinfo=UTC),datetime(2026,12,2,tzinfo=UTC))
            self.assertEqual({p['level'] for p in r['periods']},{1,2,3,4})
            self.assertTrue(r['lot_calculation']['kernel_sha256'])
            d=chart(e,'1961-07-01T19:45','Europe/London',52+50/60,.5,Settings(tradition='Hellenistic'))
            r=from_natal(e,d,datetime(1997,7,21,tzinfo=UTC),datetime(1997,7,24,tzinfo=UTC),lot='Fortune')
            self.assertEqual(int(r['lots']['Fortune']//30),4)
            bond=[p for p in r['periods'] if p['level']==2 and p['loosing_of_bond']]
            self.assertEqual(len(bond),1);self.assertTrue(bond[0]['start_inclusive_utc'].startswith('1997-07-22'))
        finally:e.kernel.close()
    def test_independent_starting_lots(self):
        f=json.loads(Path('tests/fixtures/releasing_lot_reference.json').read_text())
        e=SkyfieldEphemeris('data/de440s.bsp')
        try:
            for case in f['cases']:
                n=chart(e,case['local'],case['zone'],case['latitude'],case['longitude'],Settings(tradition='Hellenistic'))
                birth=datetime.fromisoformat(n['birth']['utc'])
                r=from_natal(e,n,birth,birth+timedelta(days=1))
                for lot in ('Fortune','Spirit'):
                    self.assertLess(abs((r['lots'][lot]-case[lot]+180)%360-180),f['tolerance_degrees'])
                self.assertEqual(r['lot_calculation']['sect']['type'],'day' if case['sun_altitude_degrees']>=0 else 'night')
        finally:e.kernel.close()
