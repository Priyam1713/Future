"""Measure production outputs against frozen independent Swiss reference fixtures."""
import json
import math
from pathlib import Path
from datetime import datetime
from future.natal import SkyfieldEphemeris,signed
from future.astrocartography import coordinates,line_geometry,diagnostics,relocated


def run():
    fixture=json.loads(Path('tests/fixtures/astrocartography_swiss.json').read_text())
    e=SkyfieldEphemeris('data/de440s.bsp')
    maxima=dict(ra_degrees=0.,declination_degrees=0.,gast_degrees=0.,meridian_degrees=0.,
                reference_horizon_root_altitude_degrees=0.,mapped_vertex_independent_altitude_degrees=0.,
                rendered_probe_independent_altitude_degrees=0.,relocated_cusp_degrees=0.,relocated_angle_degrees=0.)
    count=dict(epochs=0,planet_positions=0,horizon_roots=0,circumpolar_cases=0,map_vertices=0,rendered_probes=0,relocated_charts=0)
    systems=dict(P='placidus',R='regiomontanus',C='campanus',O='porphyry',E='equal',W='whole-sign')
    def record(key,value):maxima[key]=max(maxima[key],abs(value))
    try:
        for case in fixture['cases']:
            count['epochs']+=1;utc=datetime.fromisoformat(case['utc'])
            t,positions=coordinates(e,utc)
            record('gast_degrees',signed(float(t.gast)*15-case['gast_degrees']))
            for name,b in positions.items():
                count['planet_positions']+=1;r=case['planets'][name]
                record('ra_degrees',signed(b['ra_degrees']-r['ra']))
                record('declination_degrees',b['declination_degrees']-r['dec'])
                for angle in ('MC','IC','ASC','DSC'):
                    segments,_=line_geometry(b,angle)
                    for segment in segments:
                        if angle in ('MC','IC'):
                            record('meridian_degrees',signed(case['gast_degrees']+segment[0][0]-r['ra']-(180 if angle=='IC' else 0)))
                            continue
                        def altitude(lon,lat):
                            h=math.radians(case['gast_degrees']+lon-r['ra']);p=math.radians(lat);d=math.radians(r['dec'])
                            return math.degrees(math.asin(max(-1,min(1,math.sin(p)*math.sin(d)+math.cos(p)*math.cos(d)*math.cos(h)))))
                        for lon,lat in segment:
                            count['map_vertices']+=1;record('mapped_vertex_independent_altitude_degrees',altitude(lon,lat))
                        for a,bpoint in zip(segment,segment[1:]):
                            for f in (.1,.2,.4,.6,.8,.9):
                                count['rendered_probes']+=1
                                record('rendered_probe_independent_altitude_degrees',altitude(a[0]+f*(bpoint[0]-a[0]),a[1]+f*(bpoint[1]-a[1])))
            for row in case['horizon_roots']:
                if not row['roots']:count['circumpolar_cases']+=1
                for root in row['roots']:
                    count['horizon_roots']+=1
                    record('reference_horizon_root_altitude_degrees',diagnostics(positions[row['planet']],row['latitude'],root['longitude'])['geometric_altitude_degrees'])
            for ref in case['sites']:
                count['relocated_charts']+=1
                c=relocated(e,utc,dict(name='reference',zone='UTC',latitude=ref['latitude'],longitude=ref['longitude']),systems[ref['system']])['chart']
                for key in ('ascendant','midheaven'):record('relocated_angle_degrees',signed(c['angles'][key]-ref[key]))
                for a,b in zip(c['house_cusps'],ref['cusps']):record('relocated_cusp_degrees',signed(a-b))
        bounds=dict(ra_degrees=.001,declination_degrees=.001,gast_degrees=.012,meridian_degrees=.012,
                    reference_horizon_root_altitude_degrees=.012,mapped_vertex_independent_altitude_degrees=.012,
                    rendered_probe_independent_altitude_degrees=.021,relocated_cusp_degrees=.02,relocated_angle_degrees=.012)
        assert all(maxima[k]<bounds[k] for k in maxima),(maxima,bounds)
        result=dict(oracle=fixture['oracle'],fixture_id=fixture['id'],profile='geocentric-apparent-geometric-v1',counts=count,
            maximum_measured_errors=maxima,acceptance_bounds=bounds,passed=True,
            limits=['Four modern epochs, not exhaustive date-range validation.',
                   'Swiss and Skyfield use separately modeled UT1; coordinate/time-model differences are included.',
                   'Map rendering error is separate from exact-vertex astronomical error.',
                   'Numerical agreement does not validate locational symbolism.'])
        Path('data/astrocartography-verification.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2))
    finally:e.kernel.close()

if __name__=='__main__':run()
