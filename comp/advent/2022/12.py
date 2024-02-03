import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F)

def elev(x):
    match x:
        case "S": return -1
        case "E": return 26
        case _: return string.ascii_lowercase.index(x)

sr, sc = 0,0
er, ec = 0,0
st = []
for (r,c) in ul.gridpoints(G):
    if G[r][c] == "S": sr, sc = r, c
    if G[r][c] == "E": er, ec = r, c
    if G[r][c] == "a": st.append((r,c))

def path(sr, sc):
    Q = deque([(sr,sc,0)])
    V = {}
    while len(Q):
        E = Q.popleft()
        (r,c,dist) = E
        if (r,c) in V: continue
        V[(r,c)] = dist

        e = elev(G[r][c])
        for (rr,cc) in ul.padj4():
            rr, cc = rr+r,cc+c
            if ul.gridcheck(G,rr,cc) and elev(G[rr][cc]) <= e + 1:
                Q.append((rr,cc,dist+1))
    return V[(er,ec)] if (er,ec) in V else math.inf

print(path(sr,sc))
print(min([path(r,c) for (r,c) in st + [(sr,sc)]]))
