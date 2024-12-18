import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
S = 0

O = {tuple(ul.ints(l)) for l in F[:1024]}

def pathfind(O):
    Q = deque([((0, 0), 0)])
    V = set()

    while len(Q):
        pos, cost = Q.popleft()
        x, y = pos

        if pos == (70, 70):
            return cost

        for (dx, dy) in ul.padj4():
            nx, ny = x+dx, y+dy

            if (nx,ny) not in O and (nx,ny) not in V and 0 <= nx <= 70 and 0 <= ny <= 70:
                V.add((nx,ny))
                Q.append(((nx,ny),cost+1))

print(pathfind(O))

for l in F[1024:]:
    O.add(tuple(ul.ints(l)))

    if pathfind(O) == None:
        print(l)
        exit()
