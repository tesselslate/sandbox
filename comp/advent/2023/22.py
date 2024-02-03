import itertools, ul
from collections import defaultdict, deque

F = ul.input()

B = []
for l in F:
    a, b, c, x, y, z = ul.scan("%d,%d,%d~%d,%d,%d", l)
    x1, x2 = ul.minmax(a,x)
    y1, y2 = ul.minmax(b,y)
    z1, z2 = ul.minmax(c,z)
    B.append(((x1,y1,z1),(x2,y2,z2)))
B.sort(key=lambda x: x[0][2])
S = {(x,y,0): -1 for (x,y) in itertools.product(range(10), repeat=2)}

for i in range(len(B)):
    ((x1,y1,z1),(x2,y2,z2)) = B[i]
    while True:
        for (x,y) in itertools.product(range(x1,x2+1), range(y1,y2+1)):
            if (x,y,z1-1) in S: break
        else: z1 -= 1; z2 -= 1; continue
        break
    for (x, y, z) in itertools.product(range(x1,x2+1),range(y1,y2+1),range(z1,z2+1)):
        S[x, y, z] = i

G, R = defaultdict(set), defaultdict(set)
for (x, y, z), i in S.items():
    if (x, y, z-1) in S:
        v = S[x, y, z-1]
        if v != i: G[i].add(v); R[v].add(i)

S = 0
for k in G.keys():
    for dep in R[k]:
        if not G[dep]-{k}: break
    else: S += 1
print(S)

S = 0
for k in G.keys():
    Q, V = deque([k]), set([k])
    while len(Q):
        i = Q.popleft()
        for k in R[i]:
            if i in G[k] and not G[k]-V:
                Q.append(k)
                V.add(k)
    S += len(V)-1
print(S)
