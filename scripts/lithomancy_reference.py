"""Independent expanded dot-product oracle; no production/profile imports."""

def squared(p,a):
    if p is None or a is None:return None
    x,y=p;u,v=a
    return x*x+y*y+u*u+v*v-2*x*u-2*y*v


def ranking(points,anchor):
    distances={k:squared(p,anchor) for k,p in points.items()}
    values=sorted(set(d for d in distances.values() if d is not None))
    return distances,[[k for k in sorted(distances) if distances[k]==d] for d in values]
