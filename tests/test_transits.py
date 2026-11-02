import unittest,json
from pathlib import Path
from datetime import datetime,timedelta,timezone
from future.transits import phase,roots,forecast
from future.natal import SkyfieldEphemeris,chart,Settings,signed

class TransitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.e=SkyfieldEphemeris('data/de440s.bsp')
    def test_phase(self):
        self.assertEqual(phase(-1,1),'applying')
        self.assertEqual(phase(-1,-1),'separating')
        self.assertEqual(phase(1,-1),'applying')
        self.assertEqual(phase(0,-1),'exact')
        self.assertEqual(phase(1,0),'stationary')
    def test_repeated_and_window_roots(self):
        start=datetime(2026,1,1,tzinfo=timezone.utc)
        times=[start+timedelta(hours=3*i) for i in range(30*8+1)]
        def value(t):
            x=(t-start).total_seconds()/86400
            return (225+(x-5)*(x-10)*(x-15)*.001)%360
        found=roots(times,[value(t) for t in times],225,value)
        self.assertEqual([round((t-start).total_seconds()/86400) for t in found],[5,10,15])
        def linear(t): return (t-start).total_seconds()/86400
        self.assertEqual(roots(times,[linear(t) for t in times],0,linear),[start])
        self.assertEqual(roots(times,[linear(t) for t in times],30,linear),[])
        # Opposite longitude jump must not be interpreted as a conjunction.
        self.assertEqual(roots(times,[170+linear(t) for t in times],0,lambda t:170+linear(t)),[])
    def test_independent_retrograde_passes_and_positions(self):
        f=json.loads(Path('tests/fixtures/transit_reference.json').read_text())
        start=datetime.fromisoformat(f['start'])
        times=[start+timedelta(hours=3*i) for i in range(30*8+1)]
        evaluate=lambda t:float(self.e.longitudes('Mercury',[t])[0])
        found=roots(times,self.e.longitudes('Mercury',times),f['target'],evaluate)
        self.assertEqual(len(found),len(f['roots']))
        self.assertGreaterEqual(len(found),2)
        for actual,expected in zip(found,f['roots']):
            self.assertLess(abs((actual-datetime.fromisoformat(expected['utc'])).total_seconds()),120)
            speed=signed(evaluate(actual+timedelta(minutes=1))-evaluate(actual-timedelta(minutes=1)))
            self.assertEqual(speed<0,expected['retrograde'])
        for p in f['positions']:
            self.assertLess(abs(signed(evaluate(datetime.fromisoformat(p['utc']))-p['longitude'])),.01)
    def test_near_station_crossings(self):
        start=datetime(2026,1,1,tzinfo=timezone.utc)
        times=[start+timedelta(hours=3*i) for i in range(9)]
        def value(t):
            x=(t-start).total_seconds()/86400
            return 225+(x-.45)**2-.0001
        found=roots(times,[value(t) for t in times],225,value)
        self.assertEqual(len(found),2)
        for t,expected in zip(found,(.44,.46)):
            self.assertLess(abs((t-start).total_seconds()/86400-expected),.00001)
    def test_output_provenance_and_validation(self):
        from future.__main__ import load_registry
        from future.western import load_context,interpreter
        natal=chart(self.e,'1990-07-15T14:30','Asia/Kolkata',28.6139,77.209,Settings(tradition='medieval/traditional'))
        r=load_registry()
        try:
            context=load_context(r,'medieval/traditional')
            self.assertFalse(any(c['author']=='Nicholas Campion' for c in context))
            report=forecast(self.e,natal,datetime(2026,11,2,tzinfo=timezone.utc),30,
                            bodies=['Mercury'],interpreter=interpreter(context,natal))
            self.assertTrue(report['exact_events'])
            dates=[e['exact_utc'] for e in report['exact_events']]
            self.assertEqual(dates,sorted(dates))
            for e in report['exact_events']:
                self.assertLess(e['angular_residual_degrees'],.00001)
                self.assertTrue(e['interpretations']['components'])
                self.assertTrue(all(c['source'] and c['locator'] for c in e['interpretations']['components']))
            for days in (0,31,-1):
                with self.assertRaises(ValueError): forecast(self.e,natal,datetime.now(timezone.utc),days)
            with self.assertRaises(ValueError): forecast(self.e,natal,datetime(2026,1,1))
        finally:r.close()

if __name__=='__main__': unittest.main()
