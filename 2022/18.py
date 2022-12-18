import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]

I = []
for l in F:
    x,y,z = util.scan("%d,%d,%d", l)
    I.append((x+1,y+1,z+1))

SIZE = 30
G = util.grid3d(SIZE, 0)
for i in I:
    G[i[0]][i[1]][i[2]] = 1

Q = collections.deque([(0,0,0)])
while len(Q) > 0:
    E = Q.pop()
    d = [
        (E[0]+1,E[1],E[2]),
        (E[0]-1,E[1],E[2]),
        (E[0],E[1]+1,E[2]),
        (E[0],E[1]-1,E[2]),
        (E[0],E[1],E[2]+1),
        (E[0],E[1],E[2]-1),
    ]
    for dir in d:
        if dir[0] >= 0 and dir[1] >= 0 and dir[2] >= 0 and dir[0] < SIZE - 1 and dir[1] < SIZE - 1 and dir[2] < SIZE - 1:
            if G[dir[0]][dir[1]][dir[2]] == 0:
                Q.append(dir)
                G[dir[0]][dir[1]][dir[2]] = 2

S = 0
S2 = 0
for x in range(SIZE):
    for y in range(SIZE):
        for z in range(SIZE):
            if G[x][y][z] != 1:
                continue
            if x > 0:
                S += 1 if G[x-1][y][z] != 1 else 0
                S2 += 1 if G[x-1][y][z] == 2 else 0
            if y > 0:
                S += 1 if G[x][y-1][z] != 1 else 0
                S2 += 1 if G[x][y-1][z] == 2 else 0
            if z > 0:
                S += 1 if G[x][y][z-1] != 1 else 0
                S2 += 1 if G[x][y][z-1] == 2 else 0
            if x < SIZE - 1:
                S += 1 if G[x+1][y][z] != 1 else 0
                S2 += 1 if G[x+1][y][z] == 2 else 0
            if y < SIZE - 1:
                S += 1 if G[x][y+1][z] != 1 else 0
                S2 += 1 if G[x][y+1][z] == 2 else 0
            if z < SIZE - 1:
                S += 1 if G[x][y][z+1] != 1 else 0
                S2 += 1 if G[x][y][z+1] == 2 else 0
print(S)
print(S2)
