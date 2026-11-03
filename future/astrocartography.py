"""Geocentric angularity, independent of longitude-only relocation house placement."""
from datetime import timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
import math
import json
from .natal import BODIES, birth_utc, signed, chart, Settings
from .knowledge import Rule

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT/'knowledge/astrocartography_conventions_v1.json').read_text())
PROFILE = DATA['profile']
RADIUS_KM = 6371.0088
RAD = math.pi/180
EPS = 1e-7  # radians: exclude grazing endpoints and undefined geographic poles


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def scale(a, k):
    return tuple(x*k for x in a)


def unit(lon, lat):
    l, p = lon*RAD, lat*RAD
    return (math.cos(p)*math.cos(l), math.cos(p)*math.sin(l), math.sin(p))


def geographic(v):
    return [signed(math.atan2(v[1], v[0])/RAD), math.atan2(v[2], math.hypot(v[0], v[1]))/RAD]


def asin(x):
    return math.asin(max(-1., min(1., x)))/RAD


def coordinates(e, utc, bodies=None):
    if not 1851 <= utc.year <= 2148:
        raise ValueError('Astrocartography supported years: 1851-2148')
    bodies = list(BODIES) if bodies is None else list(bodies)
    if not bodies or len(set(bodies)) != len(bodies) or any(b not in BODIES for b in bodies):
        raise ValueError('Select unique supported planets')
    t = e.ts.from_datetime(utc)
    result = {}
    for name in bodies:
        ra, dec, _ = e.kernel['earth'].at(t).observe(e.kernel[BODIES[name]]).apparent().radec(epoch='date')
        result[name] = dict(ra_degrees=float(ra.hours)*15, declination_degrees=float(dec.degrees),
                            mc_longitude=signed(float(ra.hours)*15-float(t.gast)*15))
    return t, result


def basis(body):
    m, d = body['mc_longitude']*RAD, body['declination_degrees']*RAD
    u = (math.cos(d)*math.cos(m), math.cos(d)*math.sin(m), math.sin(d))
    v = (-math.sin(m), math.cos(m), 0.)
    w = (-math.sin(d)*math.cos(m), -math.sin(d)*math.sin(m), math.cos(d))
    return u, v, w


def diagnostics(body, lat, lon):
    h = signed(lon-body['mc_longitude'])*RAD
    p, d = lat*RAD, body['declination_degrees']*RAD
    altitude = asin(math.sin(p)*math.sin(d)+math.cos(p)*math.cos(d)*math.cos(h))
    derivative = -math.cos(p)*math.cos(d)*math.sin(h)
    a, b = math.sin(p)*math.sin(d), abs(math.cos(p)*math.cos(d))
    status = ('polar-degenerate' if abs(lat)==90 else 'grazing' if abs(abs(a)-b)<1e-12
              else 'always-above' if a>b else 'always-below' if a < -b else 'rises-and-sets')
    return dict(hour_angle_degrees=h/RAD, geometric_altitude_degrees=altitude,
                altitude_sine_derivative_per_hour_angle_radian=derivative, horizon_status=status)


def horizon_longitudes(body, lat):
    """For sensitivity reporting only; grazing roots are not rising/setting."""
    if abs(lat)==90:return dict(status='polar-degenerate',ASC=None,DSC=None)
    c=-math.tan(lat*RAD)*math.tan(body['declination_degrees']*RAD)
    if abs(c)>=1:
        return dict(status=diagnostics(body,lat,0)['horizon_status'],ASC=None,DSC=None)
    h=math.acos(c)/RAD
    return dict(status='rises-and-sets',ASC=signed(body['mc_longitude']-h),DSC=signed(body['mc_longitude']+h))


def line_geometry(body, angle, tolerance=.01):
    """Parametric great-circle semicircles; split at the actual antimeridian crossing."""
    if angle not in ('MC', 'IC', 'ASC', 'DSC'):
        raise ValueError('Unknown angular axis')
    if not math.isfinite(tolerance) or not .0001 <= tolerance <= .1:
        raise ValueError('Map tolerance must be .0001 through .1 degrees')
    u, v, w = basis(body)
    if angle in ('MC', 'IC'):
        lon = signed(body['mc_longitude']+(180 if angle=='IC' else 0))
        return [[[lon, -90+EPS/RAD], [lon, 90-EPS/RAD]]], dict(max_probe_residual_degrees=0., vertices=2)
    sign = -1 if angle=='ASC' else 1

    def point(t):
        return geographic(tuple(w[i]*math.cos(t)+sign*v[i]*math.sin(t) for i in range(3)))

    # Initial arcs <=5 degrees; refine the geographic-linear rendering, not the astronomy.
    samples = []
    maximum = 0.

    def refine(a, pa, b, pb, depth=0):
        nonlocal maximum
        dl = signed(pb[0]-pa[0])
        residual = max(abs(asin(dot(u, unit(pa[0]+f*dl, pa[1]+f*(pb[1]-pa[1]))))) for f in (.25,.5,.75))
        if residual > tolerance*.8:
            if depth >= 24:
                raise ValueError('Requested map tolerance could not be resolved')
            mid=(a+b)/2; pm=point(mid)
            refine(a,pa,mid,pm,depth+1); refine(mid,pm,b,pb,depth+1)
        else:
            maximum=max(maximum,residual);samples.append((a,pa))

    ts = [EPS+(math.pi-2*EPS)*i/36 for i in range(37)]
    for a,b in zip(ts,ts[1:]):
        refine(a,point(a),b,point(b))
    samples.append((ts[-1],point(ts[-1])))
    segments = [[samples[0][1]]]
    for (a,pa),(b,pb) in zip(samples,samples[1:]):
        if abs(pb[0]-pa[0]) > 180:
            # Longitude is monotonic on each nondegenerate branch. Bisect unwrapped longitude.
            target=180 if pa[0]>0 else -180
            direction=signed(pb[0]-pa[0])
            lo,hi=a,b
            for _ in range(60):
                mid=(lo+hi)/2
                delta=signed(point(mid)[0]-pa[0])
                if (delta < target-pa[0]) == (direction>0):lo=mid
                else:hi=mid
            crossing=point((lo+hi)/2)[1]
            segments[-1].append([target,crossing]);segments.append([[-target,crossing]])
        segments[-1].append(pb)
    return segments, dict(max_probe_residual_degrees=maximum,vertices=sum(map(len,segments)),
                          probe_fractions=[.25,.5,.75],max_initial_arc_degrees=5,
                          excluded_endpoint_radians=EPS)


def nearest(body, angle, lat, lon):
    """Analytic closest point on a spherical semicircle closure, including endpoints."""
    q=unit(lon,lat);u,v,w=basis(body)
    if angle in ('MC','IC'):
        normal=v;half=unit(body['mc_longitude'],0);ends=(0.,0.,1.)
        sign=1 if angle=='MC' else -1; endpoint_kind='polar-endpoint'
    else:
        normal=u;half=v;ends=w;sign=-1 if angle=='ASC' else 1;endpoint_kind='grazing-endpoint'
    projected=tuple(q[i]-dot(q,normal)*normal[i] for i in range(3))
    norm=math.sqrt(dot(projected,projected))
    candidates=[(ends,endpoint_kind),(scale(ends,-1),endpoint_kind)]
    if norm>1e-14:
        foot=scale(projected,1/norm)
        if sign*dot(foot,half)>1e-12:candidates.append((foot,'branch-interior'))
    p,kind=max(candidates,key=lambda c:dot(q,c[0]))
    # atan2 remains stable near zero distance, unlike acos(dot).
    cross=(q[1]*p[2]-q[2]*p[1],q[2]*p[0]-q[0]*p[2],q[0]*p[1]-q[1]*p[0])
    radians=math.atan2(math.sqrt(dot(cross,cross)),dot(q,p))
    return dict(distance_km=radians*RADIUS_KM,central_angle_degrees=radians/RAD,
                nearest_coordinate=geographic(p),nearest_kind=kind,
                method='shortest spherical semicircle-closure distance; mean Earth radius 6371.0088km')


def register_knowledge(registry):
    for s in DATA['sources']:registry.add_source(s)
    rules=[Rule('acg.geometry',1,7,'angular lines',PROFILE,'acg-usno-geometry-v1',
        'Local hour angle; Altitude equations','Solve H=0/180 or geometric altitude=0 with branch derivative.',
        'spherical_angularity',DATA['conventions'],'verified','computational',['astrocartography-swiss-v1'])]
    for key,text in DATA['planet_components'].items():
        rules.append(Rule('acg.symbol.'+key,1,7,'compositional symbolism','modern psychological',
            'acg-symbol-'+key.lower()+'-v1','Opening planetary symbolism paragraphs',text,
            'symbolic_component',{'planet':key},'proposed','traditional',[]))
    for key,text in DATA['axis_components'].items():
        rules.append(Rule('acg.axis.'+key,1,7,'compositional symbolism','modern psychological',
            'acg-axis-topics-v1','Houses 1,4,7,10; angular-house analogy',text,
            'symbolic_component',{'angle':key},'proposed','traditional',[]))
    for rule in rules:registry.add_rule(rule)


def interpretation(planet, angle):
    return dict(coverage='compositional',tradition='modern psychological',
        text=f"Reflect on {DATA['planet_components'][planet]} in relation to {DATA['axis_components'][angle]}.",
        rule_ids=['acg.symbol.'+planet,'acg.axis.'+angle],
        sources=[s for s in DATA['sources'] if s['id'] in ('acg-symbol-'+planet.lower()+'-v1','acg-axis-topics-v1')],
        direct_book_coverage='unsupported',limitation=DATA['interpretation_policy'])


def relocated(e, utc, destination, houses):
    lat,lon=destination['latitude'],destination['longitude']
    validate_location(lat,lon)
    zone=ZoneInfo(destination['zone'])
    result=dict(destination=dict(destination),utc=utc.isoformat(),local_display=utc.astimezone(zone).isoformat(),
                frame='relocated',houses=houses)
    if abs(lat)>=60:
        return dict(result,status='unsupported',reason='Relocation charts validated only for |latitude|<60; no substitution.')
    c=chart(e,utc.replace(tzinfo=None).isoformat(),'UTC',lat,lon,Settings(houses=houses))
    c['epoch']=c.pop('birth');c['settings']['application']='relocation';c['technique_id']=7
    return dict(result,status='supported',chart=c)


def validate_location(lat,lon):
    if not all(isinstance(x,(int,float)) and math.isfinite(x) for x in (lat,lon)) or not -90<=lat<=90 or not -180<=lon<=180:
        raise ValueError('Finite latitude [-90,90] and east longitude [-180,180] required')


def generate(e, local, zone, latitude, longitude, *, destinations=(), query=None, fold=None,
             bodies=None, houses='placidus', tolerance=.01, uncertainty_minutes=0, profile=PROFILE):
    from .houses import SYSTEMS
    if profile!=PROFILE:raise ValueError('Unsupported coordinate profile')
    if houses not in SYSTEMS:raise ValueError('Unsupported house system')
    validate_location(latitude,longitude)
    if not math.isfinite(uncertainty_minutes) or not 0<=uncertainty_minutes<=60:
        raise ValueError('Uncertainty minutes must be 0 through 60')
    utc=birth_utc(local,zone,fold)
    t,positions=coordinates(e,utc,bodies)
    features=[];near=[]
    if query is not None:
        if len(query)!=2:raise ValueError('Query needs latitude and longitude')
        validate_location(*query)
    for name,body in positions.items():
        for angle in ('MC','IC','ASC','DSC'):
            segments,diagnostic=line_geometry(body,angle,tolerance)
            reading=interpretation(name,angle)
            features.append(dict(type='Feature',id=f'{name}.{angle}',
                properties=dict(planet=name,angle=angle,profile=profile,**body,
                    ephemeris_target=BODIES[name],
                    calculation_sources=['acg-usno-geometry-v1','acg-skyfield-coordinates-v1'],
                    rule_id='acg.geometry',diagnostics=diagnostic,interpretation=reading),
                geometry=dict(type='MultiLineString',coordinates=segments)))
            if query is not None:
                near.append(dict(planet=name,angle=angle,**nearest(body,angle,*query),
                                 angularity=diagnostics(body,*query),interpretation=reading))
    sensitivity=[]
    for minutes in (-uncertainty_minutes,uncertainty_minutes) if uncertainty_minutes else ():
        _,offset=coordinates(e,utc+timedelta(minutes=minutes),positions)
        sensitivity.append(dict(offset_minutes=minutes,utc=(utc+timedelta(minutes=minutes)).isoformat(),
            planets={name:dict(**b,mc_shift_degrees=signed(b['mc_longitude']-positions[name]['mc_longitude'])) for name,b in offset.items()},
            query_diagnostics={name:diagnostics(b,*query) for name,b in offset.items()} if query is not None else {},
            at_latitude=query[0] if query is not None else latitude,
            horizon_longitudes={name:horizon_longitudes(b,query[0] if query is not None else latitude) for name,b in offset.items()}))
    release=ROOT/'knowledge/astrocartography_core_v1.json'
    return dict(technique_id=7,profile=profile,release_status=json.loads(release.read_text())['status'] if release.exists() else 'Developing',
        birth=dict(local=local,zone=zone,fold=fold,latitude=latitude,longitude=longitude,utc=utc.isoformat()),
        times=dict(jd_tt=float(t.tt),jd_ut1=float(t.ut1),gast_degrees=float(t.gast)*15,delta_t_seconds=float(t.delta_t),dut1_seconds=float(t.dut1)),
        conventions=DATA['conventions'],reproducibility=dict(kernel_sha256=e.digest,skyfield='1.54',profile_version=1),
        ephemeris_targets={name:BODIES[name] for name in positions},
        equatorial_positions=positions,geojson=dict(type='FeatureCollection',features=features,
            profile=profile,utc=utc.isoformat(),map_tolerance_degrees=tolerance,
            conventions=DATA['conventions'],calculation_sources=DATA['sources'][:2],
            kernel_sha256=e.digest,ephemeris_targets={name:BODIES[name] for name in positions}),
        natal_frame=relocated(e,utc,dict(name='Birth location',latitude=latitude,longitude=longitude,zone=zone),houses)|{'frame':'natal'},
        relocated_frames=[relocated(e,utc,d,houses) for d in destinations],
        query=dict(latitude=query[0],longitude=query[1],lines=sorted(near,key=lambda x:x['distance_km'])) if query is not None else None,
        birth_time_sensitivity=sensitivity,sources=DATA['sources'],
        limitations=['Spatial correctness does not establish predictive validity.',
            'Existing DE440s targets use Mars through Pluto system barycenters; exact target mapping is supplied.',
            'Geocentric horizon differs from observed rise/set, especially for the Moon.',
            'Grazing endpoints and poles are excluded from mapped branches; distances include their closure.',
            'Interpolation probes bound tested residuals, not a formal continuous error proof.',
            'Longitude-only chart ASC/DSC and houses need not coincide with actual-body angular lines.',
            'No original Lewis/Davis procedural or direct interpretive coverage; no parans/local-space.'])


def markdown(r):
    out=['# Astrocartography',f"{r['release_status']} · {r['profile']}",
         f"Birth instant: {r['birth']['utc']}; {len(r['geojson']['features'])} angular lines.",
         'MC/IC are upper/lower meridians; ASC/DSC use the geocentric geometric center horizon.',
         '\n## Selected point']
    if r['query']:
        out.append('Distance sorts geometry only; no favorable-location ranking. All line details remain in JSON.')
        for row in r['query']['lines'][:8]:
            out.extend([f"- {row['planet']} {row['angle']}: {row['distance_km']:.1f} km ({row['nearest_kind']}).",
                '  Compositional: '+row['interpretation']['text'],
                '  Sources: '+', '.join(f"[{s['author']}]({s['url']}) — {s['locator']}" for s in row['interpretation']['sources'])])
    out.append('\n## Chart frames')
    for frame in [r['natal_frame']]+r['relocated_frames']:
        out.append(f"- {frame['frame']}: {frame['destination']['name']}, {frame['status']}; UTC {frame['utc']}, {frame['houses']}.")
        if frame['status']=='supported':
            out.append('  Angles: '+json.dumps(frame['chart']['angles']))
            out.extend(['','| Planet | Tropical longitude | Sign | House |','|---|---:|---|---:|'])
            for name,p in frame['chart']['planets'].items():
                out.append(f"| {name} | {p['longitude']:.5f}° | {p['sign']} | {p['house']} |")
    out.extend(['\n## Limits']+['- '+s for s in r['limitations']])
    return '\n'.join(out)+'\n'
