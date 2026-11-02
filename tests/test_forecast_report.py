import unittest,json
from copy import deepcopy
from datetime import datetime,timezone,timedelta
from future.natal import SkyfieldEphemeris,chart,Settings
from future.transits import forecast,roots,orb_intervals
from future.western import load_context,interpreter,conditions_match
from future.forecast_report import present,markdown
from future.__main__ import load_registry

class ForecastReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.e=SkyfieldEphemeris('data/de440s.bsp')
    def test_direct_composed_unsupported_and_conditions(self):
        registry=load_registry()
        try:
            n=chart(self.e,'1990-07-15T14:30','Asia/Kolkata',28.6139,77.209)
            records=load_context(registry,'modern psychological')
            select=interpreter(records,n)
            direct=select('Mercury','Pluto',0)
            self.assertEqual(direct['coverage'],'documented')
            self.assertIn('research',direct['direct'][0]['text'])
            self.assertTrue(all(r['source'] and r['locator'] and r['version'] for r in direct['direct']))
            self.assertEqual(select('Pluto','Mercury',0)['coverage'],'compositional')
            self.assertEqual(interpreter([],n)('Mercury','Pluto',0)['coverage'],'unsupported')
            traditional=interpreter(load_context(registry,'medieval/traditional'),n)
            self.assertFalse(traditional('Mercury','Pluto',0)['direct'])
            conditioned=deepcopy(next(r for r in records if r['kind']=='transit'))
            conditioned['conditions']={'phase':'applying','retrograde':True,'natal_house':[3,4]}
            f=interpreter([conditioned],n)
            args=(conditioned['transiting'],conditioned['natal_target'],conditioned['aspects'][0])
            self.assertFalse(f(*args)['direct'])
            self.assertTrue(f(*args,{'phase':'applying','retrograde':True,'natal_house':3})['direct'])
            self.assertFalse(f(*args,{'phase':'exact','retrograde':True,'natal_house':3})['direct'])
            self.assertFalse(conditions_match({'unimplemented':1},{'unimplemented':1}))
        finally: registry.close()
    def test_report_partition_and_multiple_dates_locations(self):
        for local,zone,lat,lon,start in [
            ('1990-07-15T14:30','Asia/Kolkata',28.6139,77.209,'2026-11-02T00:00:00+00:00'),
            ('2000-08-01T12:00','Europe/London',51.5,0,'2024-04-08T00:00:00+00:00')]:
            n=chart(self.e,local,zone,lat,lon)
            r=load_registry()
            try:
                select=interpreter(load_context(r,'modern psychological'),n)
                report=forecast(self.e,n,datetime.fromisoformat(start),3,bodies=['Moon'],interpreter=select)
                before=deepcopy(report['exact_events']); present(report)
                self.assertEqual(before,report['exact_events'])
                ids=[e['id'] for e in report['exact_events']]
                self.assertEqual(len(ids),len(set(ids)))
                theme_ids=[i for g in report['presentation']['themes'] for i in g['event_ids']]
                self.assertCountEqual(ids,theme_ids)
                self.assertEqual(ids,report['presentation']['upcoming_event_ids'])
                for c in report['configurations']:
                    self.assertGreaterEqual(c['hours_in_window'],0)
                    self.assertLessEqual(c['hours_in_window'],72)
                self.assertIn('Coverage gaps',markdown(report))
            finally:r.close()
    def test_tangent_station_and_clipped_duration(self):
        start=datetime(2026,1,1,tzinfo=timezone.utc)
        times=[start+timedelta(hours=3*i) for i in range(9)]
        value=lambda t:225+((t-start).total_seconds()/86400-.45)**2
        found=roots(times,[value(t) for t in times],225,value)
        self.assertEqual(len(found),1)
        self.assertLess(abs((found[0]-start).total_seconds()/86400-.45),.00001)
        spans=orb_intervals(times,[225]*len(times),225,1,lambda t:225)
        self.assertEqual(spans[0]['hours_in_window'],24)
        self.assertTrue(spans[0]['start_clipped'] and spans[0]['end_clipped'])
        self.assertEqual(orb_intervals(times,[225]*len(times),225,0,lambda t:225),[])
    def test_real_retrograde_grouping_preserves_contacts(self):
        n=chart(self.e,'1990-07-15T14:30','Asia/Kolkata',28.6139,77.209)
        r=load_registry()
        try:
            report=present(forecast(self.e,n,datetime(2026,11,2,tzinfo=timezone.utc),30,
                    bodies=['Mercury'],interpreter=interpreter(load_context(r,'modern psychological'),n)))
            self.assertTrue(report['presentation']['repeated_patterns'])
            events={e['id']:e for e in report['exact_events']}
            seen=[]
            for group in report['presentation']['repeated_patterns']:
                self.assertEqual(len(group['event_ids']),len(set(group['event_ids'])))
                self.assertTrue(any(events[i]['retrograde'] for i in group['event_ids']))
                self.assertTrue(any(not events[i]['retrograde'] for i in group['event_ids']))
                seen+=group['event_ids']
            self.assertEqual(len(seen),len(set(seen)))
        finally:r.close()

if __name__=='__main__':unittest.main()
