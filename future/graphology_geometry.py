"""Independent Euclidean teaching geometry; no graphological interpretation."""
import math


def _object(value,keys,path):
    if not isinstance(value,dict) or set(value)-set(keys):raise ValueError('Invalid '+path+' fields')


def _number(value,positive=False):
    if isinstance(value,bool) or not isinstance(value,(int,float)):raise ValueError('Finite numerical measurement required')
    try:valid=math.isfinite(value) and abs(value)<=1e12
    except OverflowError:valid=False
    if not valid or (positive and value<=0):raise ValueError('Measurement outside finite supported range; positive denominator required')
    return value


def _vector(points):
    if not isinstance(points,list) or len(points)!=2:raise ValueError('Two endpoints required')
    for p in points:
        if not isinstance(p,list) or len(p)!=2:raise ValueError('Each endpoint requires x,y')
        for n in p:_number(n)
    v=[points[1][i]-points[0][i] for i in (0,1)]
    if v==[0,0]:raise ValueError('Zero-length vector')
    return v


def measure(value):
    _object(value,['coordinate_system','units','baseline','upstroke','spacing','proportions'],'geometry')
    if value.get('coordinate_system')!='cartesian_y_up' or value.get('units') not in ('mm','arbitrary'):
        raise ValueError('Explicit Cartesian x-right/y-up coordinates and common mm/arbitrary units required')
    if not set(value)&{'baseline','spacing','proportions'}:raise ValueError('Supply baseline or normalized dimensions')
    out=dict(coordinate_system='cartesian_y_up',input_units=value['units'],angle_units='degrees',ratios={},
        baseline_angle=None,slant_from_baseline_normal=None,interpretation_applied=False,
        dimension_conventions='x_height:baseline to lowercase body top;ascender_height:baseline to ascender top;descender_depth:positive depth below baseline;gaps:nonnegative edge-to-edge distances in common units.',
        angle_conventions='Baseline degrees counterclockwise from page horizontal;slant degrees clockwise from upward baseline normal;angles rounded to12 decimal places. No source category thresholds inferred.')
    if 'baseline' in value:
        b=_vector(value['baseline'])
        if b[0]<=0:raise ValueError('Baseline must run from left to right with positive x displacement')
        out['baseline_angle']=round(math.degrees(math.atan2(b[1],b[0])),12)
        if 'upstroke' in value:
            u=_vector(value['upstroke']);normal=b[0]*u[1]-b[1]*u[0];along=b[0]*u[0]+b[1]*u[1]
            if normal<=0:raise ValueError('Upstroke base-to-tip must point above the baseline')
            out['slant_from_baseline_normal']=round(math.degrees(math.atan2(along,normal)),12)
    elif 'upstroke' in value:raise ValueError('Upstroke requires an explicit baseline')
    for field,dimensions in [('spacing',['word_gap','letter_gap','line_gap']),('proportions',['ascender_height','descender_depth'])]:
        if field not in value:continue
        row=value[field];_object(row,['x_height',*dimensions],field)
        denominator=_number(row.get('x_height'),positive=True)
        if not set(row)&set(dimensions):raise ValueError('Supply at least one normalized dimension')
        for key in dimensions:
            if key in row:
                n=_number(row[key])
                if n<0:raise ValueError('Gaps/heights/depths must be nonnegative; overlap classification not implemented')
                ratio=n/denominator
                if not math.isfinite(ratio):raise ValueError('Nonfinite normalized ratio')
                out['ratios'][key+'_over_x_height']=ratio
    return out
