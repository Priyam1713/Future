from datetime import datetime, timedelta, date
import json
from pathlib import Path
import unittest
from future.natal import SkyfieldEphemeris
from future.chinese import chart,solar_terms,day_hour,day_index,animal_year,CONVENTIONS,register_knowledge
from future.__main__ import load_registry

ROOT=Path(__file__).resolve().parents[1]

class ChineseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=SkyfieldEphemeris(ROOT/'data/de440s.bsp')
        cls.p=json.loads((ROOT/'tests/fixtures/chinese_published.json').read_text(encoding='utf-8'))
        cls.ref=json.loads((ROOT/'tests/fixtures/chinese_reference.json').read_text(encoding='utf-8'))

    @classmethod
    def tearDownClass(cls):
        solar_terms.cache_clear();cls.e.kernel.close()

    def test_independent_hko_all_terms_and_solver_precision(self):
        for r in self.p['hko_terms']:
            expected=datetime.fromisoformat(r['hkt']+'+08:00')
            found=next(t for t in solar_terms(self.e,expected.year) if t['longitude']==r['longitude'])
            dt=datetime.fromisoformat(found['utc'])
            self.assertLess(abs((dt-expected).total_seconds()),self.p['tolerance_seconds'])
            self.assertLessEqual(found['bracket_seconds'],.005)
            from future.natal import signed
            self.assertLess(abs(signed(float(self.e.longitudes('Sun',[dt])[0])-r['longitude'])),1e-6)

    def test_published_charts_and_independent_diverse_calendars(self):
        for r in self.p['published_charts']+self.ref['cases']:
            with self.subTest(local=r['local'],profile=r['profile'],zone=r['zone']):
                n=chart(self.e,r['local'],r['zone'],r['latitude'],r['longitude'],r.get('fold'),r['profile'])
                self.assertEqual([p['pair'] for p in n['pillars'].values()],r['pillars'])
                self.assertEqual(sum(n['elements']['visible_stem_counts'].values()),4)
                self.assertEqual(sum(n['elements']['branch_phase_counts'].values()),4)
                for p in n['pillars'].values():self.assertEqual(p['stem']['index']%2,p['branch']['index']%2)

    def test_exact_jie_and_zhongqi_boundaries(self):
        for year,lon in [(2014,315),(2026,315),(2026,345),(2026,0)]:
            t=next(t for t in solar_terms(self.e,year) if t['longitude']==lon)
            dt=datetime.fromisoformat(t['utc'])
            def run(d):return chart(self.e,d.replace(tzinfo=None).isoformat(),'UTC',0,0)
            before=run(dt-timedelta(seconds=1));at=run(dt);after=run(dt+timedelta(seconds=1))
            for p in ('year','month'):self.assertEqual(at['pillars'][p],after['pillars'][p])
            self.assertEqual(before['pillars']['year']!=at['pillars']['year'],lon==315)
            self.assertEqual(before['pillars']['month']!=at['pillars']['month'],lon%30==15)
            if lon%30==15:self.assertEqual(at['solar_month']['start_inclusive']['utc'],t['utc'])
            self.assertTrue(at['boundary_sensitivity']['within_120_seconds_of_jie'] if lon%30==15 else True)

    def test_day_epoch_zi_midnight_and_hour_boundaries(self):
        from future.chinese import pillar
        for r in self.p['day_references']:
            i=day_index(date.fromisoformat(r['date']))
            self.assertEqual(pillar(i%10,i%12)['pair'],r['pair'])
        # Published split-Zi late-hour fixture has day Geng-Zi, hour Wu-Zi.
        late=datetime(1988,2,15,23,30)
        d,h,*_=day_hour(late,'civil-split-zi');self.assertEqual((d['pair'],h['pair']),('庚子','戊子'))
        d,h,*_=day_hour(late,'civil-zi23');self.assertEqual((d['pair'],h['pair']),('辛丑','戊子'))
        d0,h0,*_=day_hour(late.replace(hour=0,day=16),'civil-zi23')
        self.assertEqual((d['pair'],h['pair']),(d0['pair'],h0['pair']))
        for hour in range(24):
            clock=datetime(2026,8,18,hour)
            for profile in CONVENTIONS['profiles']:
                _,h,*_=day_hour(clock,profile)
                self.assertEqual(h['branch']['index'],((hour+1)//2)%12)
        before=day_hour(datetime(2026,8,18,22,59,59),'civil-zi23')[0]
        at=day_hour(datetime(2026,8,18,23),'civil-zi23')[0]
        self.assertEqual(before['pair'],'甲子');self.assertEqual(at['pair'],'乙丑')

    def test_dst_scope_provenance_and_reproducibility(self):
        for local in ['2026-03-08T02:30','2026-11-01T01:30']:
            with self.assertRaises(ValueError):chart(self.e,local,'America/New_York',40,-74)
        civil=chart(self.e,'2000-02-29T23:30','Australia/Sydney',-33.9,151.2)
        standard=chart(self.e,'2000-02-29T23:30','Australia/Sydney',-33.9,151.2,profile='standard-zi23')
        self.assertEqual(civil['clock']['dst_seconds'],3600)
        self.assertNotEqual(civil['pillars']['day'],standard['pillars']['day'])
        self.assertEqual(civil['solar_month'],standard['solar_month'])
        self.assertEqual(civil,chart(self.e,'2000-02-29T23:30','Australia/Sydney',-33.9,151.2))
        for local,profile in [('1800-01-01T12:00','civil-zi23'),('2101-01-01T12:00','civil-zi23'),('2026-01-01T12:00','solar')]:
            with self.assertRaises(ValueError):chart(self.e,local,'UTC',0,0,profile=profile)
        with self.assertRaises(ValueError):chart(self.e,'2026-01-01T12:00','UTC',float('nan'),0)
        r=load_registry()
        try:
            register_knowledge(r);register_knowledge(r)
            for rule in CONVENTIONS['rules']:
                self.assertTrue(rule['locator'] and rule['exceptions'])
                self.assertIsNotNone(r.db.execute('SELECT id FROM sources WHERE id=?',(rule['source_id'],)).fetchone())
        finally:r.close()

    def test_lunar_festival_separate_from_solar_year(self):
        n=chart(self.e,'2026-02-10T12:00','Asia/Hong_Kong',22.3,114.2)
        self.assertEqual(n['pillars']['year']['branch']['animal'],'Horse')
        self.assertEqual(n['lunar_year_animal']['animal'],'Snake')
        self.assertEqual(animal_year(date(2034,2,18))['animal'],'Ox')
        self.assertEqual(animal_year(date(2034,2,19))['animal'],'Tiger')
        records=json.loads((ROOT/'knowledge/chinese_new_years.json').read_text(encoding='utf-8'))['records']
        self.assertEqual([r['year'] for r in records],list(range(1901,2101)))
        for r in records:
            boundary=date.fromisoformat(r['cny'])
            self.assertEqual(r['cny'],self.ref['cny_dates'][str(r['year'])])
            self.assertEqual(animal_year(boundary)['lunar_year'],r['year'])
            self.assertEqual(animal_year(boundary-timedelta(days=1))['lunar_year'],r['year']-1)
            self.assertEqual(len(r['sha256']),64)

if __name__=='__main__':unittest.main()
