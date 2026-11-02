"""Original spherical constructions. Swiss Ephemeris is not imported here."""
import math

SYSTEMS=('whole-sign','equal','porphyry','placidus','regiomontanus','campanus')

class HouseGeometryError(ValueError): pass

def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def axes(armc,latitude,obliquity):
    th,ph,ep=map(math.radians,(armc,latitude,obliquity))
    mc=math.degrees(math.atan2(math.sin(th),math.cos(th)*math.cos(ep)))%360
    asc=(math.degrees(math.atan2(-math.cos(th),math.sin(th)*math.cos(ep)+math.tan(ph)*math.sin(ep)))+180)%360
    return asc,mc

def cusps(armc,latitude,obliquity,system):
    if system not in SYSTEMS: raise ValueError('Unknown house system')
    if not all(math.isfinite(v) for v in (armc,latitude,obliquity)) or not -90<latitude<90 or not 0<obliquity<90:
        raise HouseGeometryError('Invalid spherical house inputs')
    asc,mc=axes(armc,latitude,obliquity)
    if system in ('whole-sign','equal'):
        start=math.floor(asc/30)*30 if system=='whole-sign' else asc
        return [(start+i*30)%360 for i in range(12)]
    if abs(latitude)>=90-obliquity:
        reason='circumpolar semi-arcs undefined' if system=='placidus' else 'polar orientation outside validated domain'
        raise HouseGeometryError(f'{system}: {reason}; no fallback is used')
    result={1:asc,10:mc,4:(mc+180)%360,7:(asc+180)%360}
    if system=='porphyry':
        for start,end in ((10,1),(1,4),(4,7),(7,10)):
            arc=(result[end]-result[start])%360
            for i in (1,2):result[(start+i-1)%12+1]=(result[start]+i*arc/3)%360
    elif system in ('regiomontanus','campanus'):
        th,ph,ep=map(math.radians,(armc,latitude,obliquity))
        north=(-math.sin(ph)*math.cos(th),-math.sin(ph)*math.sin(th),math.cos(ph))
        east=(-math.sin(th),math.cos(th),0.)
        zenith=(math.cos(ph)*math.cos(th),math.cos(ph)*math.sin(th),math.sin(ph))
        for house,offset in ((11,30),(12,60),(2,120),(3,150)):
            h=math.radians(offset)
            q=(math.cos(th+h),math.sin(th+h),0.) if system=='regiomontanus' else tuple(
                zenith[j]*math.cos(h)+east[j]*math.sin(h) for j in range(3))
            normal=cross(north,q)
            a=normal[0];b=normal[1]*math.cos(ep)+normal[2]*math.sin(ep)
            if math.hypot(a,b)<1e-12:raise HouseGeometryError('Degenerate house circle')
            lon=math.atan2(-a,b)
            point=(math.cos(lon),math.sin(lon)*math.cos(ep),math.sin(lon)*math.sin(ep))
            if sum(x*y for x,y in zip(point,q))<0:lon+=math.pi
            result[house]=math.degrees(lon)%360
            result[(house+5)%12+1]=(result[house]+180)%360
    else:
        ph,ep=map(math.radians,(latitude,obliquity))
        # Solve for right ascension along each semi-arc, not equal longitude.
        for house,lo,hi,factor,night in ((11,0,90,1/3,False),(12,0,90,2/3,False),
                                         (2,90,180,2/3,True),(3,90,180,1/3,True)):
            # At large declinations the eastern semi-arc can exceed 90 degrees.
            # Bracket the entire eastern half-sphere, not an equatorial quadrant.
            lo,hi=0.,180.
            def equation(offset):
                alpha=math.radians(armc+offset)
                lon=math.atan2(math.sin(alpha),math.cos(alpha)*math.cos(ep))
                dec=math.asin(math.sin(ep)*math.sin(lon))
                argument=-math.tan(ph)*math.tan(dec)
                if abs(argument)>=1:raise HouseGeometryError('Placidus semi-arc undefined')
                semi=math.degrees(math.acos(argument))
                desired=180-factor*(180-semi) if night else factor*semi
                return offset-desired
            for _ in range(60):
                mid=(lo+hi)/2
                if equation(mid)>0:hi=mid
                else:lo=mid
            alpha=math.radians(armc+(lo+hi)/2)
            result[house]=math.degrees(math.atan2(math.sin(alpha),math.cos(alpha)*math.cos(ep)))%360
            result[(house+5)%12+1]=(result[house]+180)%360
    output=[result[i] for i in range(1,13)]
    widths=[(output[(i+1)%12]-output[i])%360 for i in range(12)]
    if min(widths)<1e-8 or abs(sum(widths)-360)>1e-7:
        raise HouseGeometryError(f'{system}: degenerate or inverted cusp sequence')
    return output

def house_for(longitude,house_cusps):
    """Longitude sectors [cusp, next cusp); no latitude-based mundane placement."""
    for i,a in enumerate(house_cusps):
        width=(house_cusps[(i+1)%12]-a)%360
        if (longitude-a)%360<width:return i+1
    raise HouseGeometryError('House cusps do not partition longitude')

def frame(t,longitude):
    return ((float(t.gast)*15+longitude)%360,
            math.degrees(float(t._mean_obliquity_radians)+float(t._nutation_angles_radians[1])))
