import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

P = []
for l in F:
    a, b, c, x, y, z = ul.scan("%d,%d,%d~%d,%d,%d", l)
    x1, x2 = ul.minmax(a,x)
    y1, y2 = ul.minmax(b,y)
    z1, z2 = ul.minmax(c,z)
    P.append(((x1,y1,z1),(x2,y2,z2)))

def collide(a,b):
    x = a[0][0] <= b[1][0] and a[1][0] >= b[0][0]
    y = a[0][1] <= b[1][1] and a[1][1] >= b[0][1]
    z = a[0][2] <= b[1][2] and a[1][2] >= b[0][2]
    return x and y and z

G = [[[0 for _ in range(373)] for _ in range(10)] for _ in range(10)]
def sim(P):
    while True:
        moved = False
        for i in range(len(P)):
            a = P[i]
            ((x1,y1,z1),(x2,y2,z2)) = P[i]
            for b in P: assert not collide(a,b) if a != b else True
            ok = True
            z1 -= 1
            z2 -= 1
            a = ((x1,y1,z1),(x2,y2,z2))
            for j in range(len(P)):
                if i == j: continue
                b = P[j]
                if z1 <= 0 or collide(a,b): ok = False; break
            if ok:
                P[i] = a
                moved = True
        if not moved: return P

from copy import deepcopy
P2 = deepcopy(P)
P = sim(P)
S = defaultdict(set)
R = defaultdict(set)
for i in range(len(P)):
    ((x1,y1,z1),(x2,y2,z2)) = P[i]
    a = ((x1,y1,z1-1),(x2,y2,z2-1))
    for j in range(len(P)):
        if i != j and collide(a, P[j]): S[i].add(j); R[j].add(i)

N = 0
for i in range(len(P)):
    for v in S.values():
        if not v-{i}: break
    else: N += 1
print(N)

N = 0
for i in range(len(P)):
    Q = deque([i])
    V = set([i])
    while len(Q):
        i = Q.popleft()
        for k in R[i]:
            if i in S[k] and not S[k]-V:
                Q.append(k)
                V.add(k)
    print(i,N,len(V)-1)
    N += len(V)-1
print(N)
