"""Offline tropical natal charts. All longitudes are degrees east."""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, reset_tzpath
from dataclasses import dataclass, asdict
from typing import Protocol
import hashlib
import math
from pathlib import Path
from itertools import combinations
from skyfield.api import load, load_file
from skyfield.framelib import ecliptic_frame
from .houses import SYSTEMS,cusps,house_for,frame

SIGNS = 'Aries Taurus Gemini Cancer Leo Virgo Libra Scorpio Sagittarius Capricorn Aquarius Pisces'.split()
BODIES = {'Sun': 'sun', 'Moon': 'moon', 'Mercury': 'mercury', 'Venus': 'venus', 'Mars': 'mars barycenter',
          'Jupiter': 'jupiter barycenter', 'Saturn': 'saturn barycenter', 'Uranus': 'uranus barycenter',
          'Neptune': 'neptune barycenter', 'Pluto': 'pluto barycenter'}
DEFAULT_ORBS = {0: 8., 60: 4., 90: 6., 120: 6., 180: 8.}

def signed(angle):
    return (angle + 180) % 360 - 180

def placement(lon):
    lon %= 360
    return {'sign': SIGNS[int(lon // 30)], 'degree_in_sign': lon % 30}

def birth_utc(local, zone, fold=None):
    # Use pinned bundled IANA data rather than host-dependent OS data.
    reset_tzpath(())
    ZoneInfo.clear_cache()
    naive = datetime.fromisoformat(local)
    if naive.tzinfo is not None:
        raise ValueError('Supply a local datetime without an offset and an IANA zone')
    tz = ZoneInfo(zone)
    candidates = {}
    for f in (0, 1):
        aware = naive.replace(tzinfo=tz, fold=f)
        utc = aware.astimezone(timezone.utc)
        if utc.astimezone(tz).replace(tzinfo=None) == naive:
            candidates[f] = utc
    if not candidates:
        raise ValueError('Nonexistent local time during a timezone transition')
    if len(set(candidates.values())) > 1 and fold is None:
        raise ValueError('Ambiguous local time: specify fold 0 or 1')
    if fold not in (None, 0, 1):
        raise ValueError('fold must be 0 or 1')
    return candidates[0 if fold is None else fold]

class Ephemeris(Protocol):
    def positions(self, utc): ...

class SkyfieldEphemeris:
    def longitudes(self, name, dates):
        """Vectorized apparent longitude sampling for transit searches."""
        if any(not 1850 <= d.year <= 2149 for d in dates):
            raise ValueError('Supported dates: 1850 through 2149')
        t = self.ts.from_datetimes(dates)
        return self.kernel['earth'].at(t).observe(self.kernel[BODIES[name]]).apparent().frame_latlon(ecliptic_frame)[1].degrees

    def __init__(self, path):
        self.path = Path(path)
        if not self.path.is_file():
            raise ValueError('Local kernel missing. Run python scripts/fetch_ephemeris.py')
        self.digest = hashlib.sha256(self.path.read_bytes()).hexdigest()
        if self.digest != 'c1c7feeab882263fc493a9d5a5b2ddd71b54826cdf65d8d17a76126b260a49f2':
            raise ValueError('Kernel checksum differs from validated DE440s release')
        self.kernel = load_file(str(self.path))
        self.ts = load.timescale(builtin=True)

    def positions(self, utc):
        if not 1850 <= utc.year <= 2149:
            raise ValueError('This release supports 1850 through 2149 (DE440s)')
        t = self.ts.from_datetime(utc)
        return self.positions_at_tt(t.tt)

    def longitudes_at_tt(self,name,jds):
        t=self.ts.tt_jd(jds)
        return self.kernel['earth'].at(t).observe(self.kernel[BODIES[name]]).apparent().frame_latlon(ecliptic_frame)[1].degrees

    def positions_at_tt(self,jd):
        t=self.ts.tt_jd(jd)
        if not 1850<=int(t.tt_calendar()[0])<=2149:
            raise ValueError('Supported ephemeris years: 1850 through 2149')
        result = {}
        for name, target in BODIES.items():
            def longitude(time):
                return float(self.kernel['earth'].at(time).observe(self.kernel[target]).apparent()
                             .frame_latlon(ecliptic_frame)[1].degrees)
            lon = longitude(t)
            speed = signed(longitude(self.ts.tt_jd(t.tt + .005)) - longitude(self.ts.tt_jd(t.tt - .005))) / .01
            result[name] = {'longitude': lon % 360, 'speed_degrees_per_day': speed, 'retrograde': speed < 0}
        return t, result

@dataclass(frozen=True)
class Settings:
    tradition: str = 'modern psychological'
    application: str = 'natal'
    zodiac: str = 'tropical'
    houses: str = 'whole-sign'
    rulership: str = 'traditional'

def angles(t, latitude, longitude):
    theta = math.radians((float(t.gast)*15 + longitude) % 360)
    # True obliquity: mean obliquity plus nutation in obliquity (Skyfield IAU model).
    eps = math.radians(float(t._mean_obliquity_radians) * 180/math.pi + float(t._nutation_angles_radians[1])*180/math.pi)
    mc = math.degrees(math.atan2(math.sin(theta), math.cos(theta)*math.cos(eps))) % 360
    asc = (math.degrees(math.atan2(-math.cos(theta), math.sin(theta)*math.cos(eps)
                                  + math.tan(math.radians(latitude))*math.sin(eps))) + 180) % 360
    return asc, mc

def aspects(planets, orbs):
    if any(float(a) not in (0,60,90,120,180) or not math.isfinite(o) or not 0 <= o < 15 for a,o in orbs.items()):
        raise ValueError('Invalid major aspect or orb')
    result = []
    for (a,p), (b,q) in combinations(planets.items(), 2):
        separation = abs(signed(p['longitude']-q['longitude']))
        for angle, orb in orbs.items():
            deviation = abs(separation-float(angle))
            if deviation <= orb:
                result.append({'bodies': [a,b], 'angle': float(angle), 'separation': separation, 'orb': deviation})
    return result

def chart(ephemeris, local, zone, latitude, longitude, settings=Settings(), fold=None, orbs=None):
    if not all(math.isfinite(v) for v in (latitude,longitude)) or not -90 < latitude < 90 or not -180 <= longitude <= 180:
        raise ValueError('Invalid latitude/longitude')
    if settings.tradition not in ('Hellenistic','medieval/traditional','modern psychological') or settings.application != 'natal' or settings.zodiac != 'tropical' or settings.houses not in SYSTEMS or settings.rulership != 'traditional':
        raise ValueError('Unsupported configuration')
    utc = birth_utc(local,zone,fold)
    t, planets = ephemeris.positions(utc)
    asc, mc = angles(t,latitude,longitude)
    house_cusps = cusps(frame(t,longitude)[0],latitude,frame(t,longitude)[1],settings.houses)
    if settings.tradition != 'modern psychological':
        planets = {k:v for k,v in planets.items() if k not in ('Uranus','Neptune','Pluto')}
    for p in planets.values():
        p.update(placement(p['longitude']))
        p['house'] = house_for(p['longitude'],house_cusps)
    return {'technique_id':1,'settings':asdict(settings),'birth':{'local':local,'zone':zone,'utc':utc.isoformat(),'latitude':latitude,'longitude':longitude},
            'times':{'jd_ut1':float(t.ut1),'jd_tt':float(t.tt),'delta_t_seconds':float(t.delta_t),'dut1_seconds':float(t.dut1)},
            'angles':{'ascendant':asc,'midheaven':mc},'house_cusps':house_cusps,'planets':planets,
            'aspects':aspects(planets,DEFAULT_ORBS if orbs is None else orbs),
            'conventions':{'coordinates':'apparent geocentric true ecliptic/equinox of date; outer planets use system barycenters',
                           'time':'IANA tzdata 2025.2; Skyfield builtin leap seconds and modeled delta T',
                           'orbs':DEFAULT_ORBS if orbs is None else orbs},
            'reproducibility':{'skyfield':'1.54','kernel_sha256':ephemeris.digest},
            'limitations':['UT1 uses bundled delta-T model; historical time-zone records and birth times may be uncertain.',
                           'Quadrant systems reject the polar domain explicitly; assignments use ecliptic longitude sectors, not mundane latitude.']}
