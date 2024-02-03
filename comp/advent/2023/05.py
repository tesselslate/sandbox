import math, ul
from collections import deque

F = ul.input()
F = ul.double_linefeed(F)

seeds = [int(x) for x in F[0][0].split()[1:]]
funcs = {}
mapping = {}

for ls in F[1:]:
    k1, k2 = ul.scan("%s-to-%s map:", ls[0])
    mapping[k1] = k2
    funcs[k1] = []
    for l in ls[1:]:
        # dst src sz
        funcs[k1].append(tuple(int(x) for x in l.split()))

def apply(k, x):
    for (dst, src, sz) in funcs[k]:
        if src <= x < src + sz:
            return x - src + dst
    return x

M = math.inf
for seed in seeds:
    k = "seed"
    while k != "location":
        seed = apply(k, seed)
        k = mapping[k]
    if seed < M:
        M = seed
print(M)

def ranges(k, rs):
    nr = []
    Q = deque(rs)
    for (dst, src, sz) in funcs[k]:
        NQ = deque()
        while len(Q):
            (s, e) = Q.popleft()
            d = dst-src

            i = ul.range_intersect((s, e), (src, src+sz))
            if i:
                if s < src: NQ.append((s,src))
                if e > src + sz: NQ.append((src+sz,e))
                nr.append((i[0]+d,i[1]+d))
            else:
                NQ.append((s,e))
                continue
        Q = NQ
    return nr + list(NQ)

M = math.inf
for r in ul.batched(seeds, 2):
    k = "seed"
    r = [(r[0],r[0]+r[1])]
    while k != "location":
        r = ranges(k, r)
        k = mapping[k]
    v = min(r, key=lambda x: x[0])[0]
    if v < M:
        M = v
print(M)
