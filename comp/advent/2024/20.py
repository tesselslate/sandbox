import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F)

start = None
for (r,c) in ul.gridpoints(G):
    if G[r][c] == "S":
        start = (r,c)
        break

Q = deque([(start, 0)])
V = defaultdict(lambda: math.inf, {start: 0})
while len(Q):
    pos, time = Q.popleft()
    r, c = pos

    for (rr, cc) in ul.padj4():
        nr, nc = r+rr, c+cc

        if G[nr][nc] != "#" and (nr, nc) not in V:
            V[nr, nc] = time + 1
            Q.append(((nr, nc), time + 1))

def cheats(clen):
    cadj = {}
    for (r, c) in itertools.product(range(-clen, clen+1), repeat=2):
        if abs(r) + abs(c) <= clen:
            cadj[r, c] = abs(r) + abs(c)

    S = 0
    for pos, time in V.items():
        r, c = pos
        for (dr, dc), dt in cadj.items():
            nr, nc = r+dr, c+dc
            if (nr, nc) in V and V[nr, nc] - time - dt >= 100:
                S += 1

    return S

print(cheats(2))
print(cheats(20))
