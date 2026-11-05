"""Independent bit-matrix oracle. No production imports, catalogs or helpers."""

def encode(p):
    return int(''.join('1' if x == '1' else '0' for x in p),2)


def decode(n):
    return ''.join('1' if n & (8 >> j) else '2' for j in range(4))


def reference(mothers):
    a,b,c,d = [encode(p) for p in mothers]
    daughters = []
    for shift in (3,2,1,0):
        daughters.append((((a>>shift)&1)<<3)|(((b>>shift)&1)<<2)|(((c>>shift)&1)<<1)|((d>>shift)&1))
    e,f,g,h = daughters
    n1,n2,n3,n4 = a^b,c^d,e^f,g^h
    w1,w2 = n1^n2,n3^n4
    return [decode(x) for x in [a,b,c,d,e,f,g,h,n1,n2,n3,n4,w1,w2,w1^w2]]
