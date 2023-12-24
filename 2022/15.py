import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
F = [tuple(ul.scan("Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d", l)) for l in F]
dists = []

R = 2000000
N = R * 2
S = set()
for b in F:
    x1, y1, x2, y2 = b
    bdist = ul.manhat((x1, y1), (x2, y2))
    dists.append(bdist)
    rdist = bdist - abs(R - y1)
    S |= {*range(x1-rdist,x1+rdist)}
print(len(S))

def check(p):
    for bdist, b in zip(dists, F):
        x1, y1, *_ = b
        if ul.manhat((x1,y1),(p[0],p[1])) <= bdist: return False
    return True

def try_all():
    c = set()
    for bdist, b in zip(dists, F):
        x1, y1, *_ = b

        y = y1 + bdist + 1
        for n in range(bdist):
            for p in [(x1+n,y-n),(x1-n,y-n),(x1+n,y+n),(x1-n,y+n)]:
                if 0 <= p[0] <= N and 0 <= p[1] <= N: c.add(p)
    for p in c:
        if check(p): return p

p = try_all()
print(4000000*p[0]+p[1])
