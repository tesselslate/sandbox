import math, ul
from collections import defaultdict, deque

F = ul.input()
G = ul.grid(F)

B = defaultdict(set)
W = set()
for (r,c) in ul.gridpoints(G):
    match G[r][c]:
        case "#": W.add((r,c))
        case ".": pass
        case _: B[r,c].add("NSEW"["^v><".index(G[r][c])])

fs = lambda dd: frozenset((r,c) for (r,c) in dd)

BL = [fs(B)]
for i in range(math.lcm(len(G) - 2, len(G[0]) - 2)-1):
    NB = defaultdict(set)
    for (r,c), blizzards in B.items():
        for b in blizzards:
            rr, cc = ul.offset_rc(b)
            rr, cc = r+rr, c+cc
            if rr == 0: rr = len(G) - 2
            if rr == len(G) - 1: rr = 1
            if cc == 0: cc = len(G[0]) - 2
            if cc == len(G[0]) - 1: cc = 1
            NB[rr,cc].add(b)
    BL.append(fs(NB))
    B = NB

def bfs(start, goal):
    Q = deque([start])
    V = set()
    while len(Q):
        (r,c,t) = Q.popleft()
        if (r,c) == goal: return t
        for rr, cc in ul.padj4() + [(0,0)]:
            rr, cc = rr+r, cc+c

            if not ul.gridcheck(G, rr, cc): continue
            if (rr, cc) in W or (rr, cc) in BL[(t+1)%len(BL)]: continue

            if (rr,cc,t+1) in V: continue
            V.add((rr,cc,t+1))

            Q.append((rr,cc,t+1))

A = (0,1)
B = (len(G)-1,len(G[0])-2)
n = bfs((*A, 0), B)
print(n)

n = bfs((*B, n), A)
n = bfs((*A, n), B)
print(n)
