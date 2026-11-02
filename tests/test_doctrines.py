import unittest,json
from pathlib import Path
from skyfield.api import wgs84
from future.natal import SkyfieldEphemeris,chart,Settings
from future.doctrines import *

class DoctrineTests(unittest.TestCase):
    def test_documented_reception_example(self):
        config=DoctrineSettings('lilly-ptolemaic','lilly','lilly-ca113','fixed-day-fortune','dignity-occupancy')
        d=dignity(205,False,config)
        self.assertEqual([d[k] for k in ('domicile','exaltation','triplicity','bound','face')],['Venus','Saturn','Mercury','Mars','Jupiter'])
        p={n:{'longitude':lon,'retrograde':False,'speed_degrees_per_day':1} for n,lon in [('Sun',205),('Saturn',10),('Venus',40),('Mercury',90),('Moon',120),('Jupiter',150),('Mars',180)]}
        conditions,edges=condition_report(p,10,False,config)
        self.assertTrue(any(e['host']=='Saturn' and e['guest']=='Sun' and e['mutual'] for e in edges))
    def test_boundaries_and_distinct_tables(self):
        a=DoctrineSettings();b=DoctrineSettings(bounds='lilly-ptolemaic')
        self.assertEqual(dignity(13,True,a)['bound'],'Mercury')
        self.assertEqual(dignity(13,True,b)['bound'],'Venus')
        self.assertEqual(dignity(6-1e-8,True,a)['bound'],'Jupiter')
        self.assertEqual(dignity(6,True,a)['bound'],'Venus')
        self.assertEqual(dignity(360,True,a),dignity(0,True,a))
        self.assertEqual(dignity(210,False,a)['triplicity'],'Mars')
        self.assertEqual(dignity(210,False,a)['participating'],'Moon')
        for table in TABLES['bounds'].values():
            self.assertEqual(len(table['rows']),12)
            for row in table['rows']:
                self.assertEqual(row[-1][1],30)
                self.assertEqual(sorted(set(end for p,end in row)),[end for p,end in row])
    def test_solar_examples_and_lots(self):
        self.assertEqual(solar_condition(45+25/60,45.5,'lilly-ca113')['state'],'cazimi')
        self.assertEqual(solar_condition(17/60,0,'lilly-ca113')['state'],'cazimi')
        self.assertEqual(solar_condition(17/60+.0001,0,'lilly-ca113')['state'],'combust')
        self.assertEqual(solar_condition(359,1,'lilly-ca113')['state'],'under_beams')
        self.assertEqual(solar_condition(359,1,'hellenistic-beams')['state'],'under_beams')
        day=lots(10,350,20,True);night=lots(10,350,20,False)
        self.assertEqual((day['Fortune'],day['Spirit']),(40,340))
        self.assertEqual((night['Fortune'],night['Spirit']),(340,40))
        self.assertEqual(lots(10,350,20,False,'fixed-day-fortune')['Fortune'],40)
    def test_independent_sect_altitudes(self):
        e=SkyfieldEphemeris('data/de440s.bsp');self.addCleanup(e.kernel.close)
        for f in json.loads(Path('tests/fixtures/sect_reference.json').read_text())['cases']:
            t=e.ts.ut1_jd(f['jd_ut1'])
            alt=float((e.kernel['earth']+wgs84.latlon(f['latitude'],f['longitude'])).at(t).observe(e.kernel['sun']).apparent().altaz()[0].degrees)
            self.assertLess(abs(alt-f['sun_true_altitude']),.02)
            self.assertEqual('day' if alt>=0 else 'night',f['sect'])
    def test_profiles_do_not_silently_merge(self):
        e=SkyfieldEphemeris('data/de440s.bsp');self.addCleanup(e.kernel.close)
        n=chart(e,'1990-07-15T14:30','Asia/Kolkata',28.6139,77.209,Settings(tradition='Hellenistic'))
        a=analyze(e,n)
        self.assertEqual(a['settings']['bounds'],'egyptian')
        self.assertEqual(a['sect']['type'],'day')
        self.assertEqual(len(a['planets']),7)
        with self.assertRaises(ValueError):analyze(e,n,DoctrineSettings(triplicity='lilly'))

if __name__=='__main__':unittest.main()
