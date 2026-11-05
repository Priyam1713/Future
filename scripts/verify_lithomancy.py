import hashlib,itertools,json
from pathlib import Path
from scripts.lithomancy_reference import squared,ranking

def verify():
    from future import lithomancy as l
    fpath=Path('tests/fixtures/lithomancy_reference_v1.json')
    f=json.loads(fpath.read_text(encoding='utf-8'));s=json.loads(Path('knowledge/lithomancy_source_freeze_v1.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(fpath.read_bytes()).hexdigest()==s['fixture_sha256']
    assert f['authored_before_engine'] and l.DATA['source']==l.freeze(f['source'])
    assert len(l.ROLES)==12 and set(l.ROLES)=={r['role_id'] for r in f['roles']}
    for r in f['roles']:assert l.thaw(l.ROLES[r['role_id']])==r
    assert l.thaw(l.DATA['source_policy'])==f['source_policy']
    assert l.thaw(l.DATA['spatial_contract'])==f['spatial_contract']
    def p(x):return dict(zip(('x','y'),x)) if x is not None else None
    def check(points,anchor,frame=l.FRAMES[0]):
        distances,groups=ranking(points,anchor);r=l.geometry({k:p(x) for k,x in points.items()},p(anchor),frame)
        assert {v['id']:v['distance_squared'] for v in r['distances']}==distances
        assert [g['ids'] for g in r['ordered_distance_groups']]==groups
        assert r['nearest_known']==(groups[0] if groups else [])
        assert r['farthest_known']==(groups[-1] if groups else [])
        return r
    for c in f['geometry_cases']:
        assert ranking(c['positions'],c['anchor'])==(c['distance_squared'],c['groups'])
        r=check(c['positions'],c['anchor'])
        for row in r['distances']:
            if 'directions' in c:assert row['direction']==c['directions'][row['id']]
    grid=list(itertools.product(range(-3,4),repeat=2));anchors=list(itertools.product(range(-2,3),repeat=2))
    points={f'p{i:02d}':v for i,v in enumerate(grid)};pairs=0
    for anchor in anchors:
        check(points,anchor)
        for v in grid:
            d=l.distance_squared(p(v),p(anchor));assert d==squared(v,anchor)==l.distance_squared(p(anchor),p(v));pairs+=1
    transforms=[lambda x,y:(x+19,y-23),lambda x,y:(3*x,3*y),lambda x,y:(-x,y),lambda x,y:(y,-x),lambda x,y:(-x,-y)]
    transformed=0
    for c in f['geometry_cases'][:2]:
        for i,t in enumerate(transforms):
            pts={k:t(*v) for k,v in c['positions'].items()};a=t(*c['anchor']);r=check(pts,a)
            assert [g['ids'] for g in r['ordered_distance_groups']]==c['groups']
            factor=9 if i==1 else 1
            assert {v['id']:v['distance_squared'] for v in r['distances']}=={k:d*factor for k,d in c['distance_squared'].items()};transformed+=1
    check({'a':None,'b':(0,0)},(1,1));check({'a':(1,2)},None)
    direction_checks=0
    for x,y in itertools.product((-1,0,1),repeat=2):
        up=l.directions(p((x,y)),p((0,0)),l.FRAMES[0]);down=l.directions(p((x,-y)),p((0,0)),l.FRAMES[1]);assert up==down;direction_checks+=1
    out=dict(passed=True,profile=l.PROFILE,profile_sha256=l.PROFILE_HASH,source_sha256=f['source']['snapshot_sha256'],fixture_sha256=s['fixture_sha256'],
        verified_roles=12,source_policy_checks=9,authored_geometry_cases=4,bounded_grid_anchor_rankings=len(anchors),bounded_grid_distance_pairs=pairs,
        transform_cases=transformed,viewpoint_checks=direction_checks,unknown_cases=2,
        reference='Independent expanded dot-product arithmetic and ranking in scripts/lithomancy_reference.py; no production imports or shared helpers.',
        invariants=['Exact squared distance and ranking','Symmetry','Tie retention including coincidence','Translation and rotation/reflection invariance','Positive uniform-scale ordering','Frame-dependent descriptive directions only','Unknown data never assigned coordinates'],empirical_validation=False)
    Path('data/lithomancy-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(f'12 Lithomancy source roles; {pairs} independent distance pairs;25 grid rankings;4 authored cases;10 transforms;9 viewpoint checks;2 unknown cases passed')
    return out
if __name__=='__main__':verify()
