import util
from sys import argv

F = [l.strip() for l in open(argv[1])]
SIZE = 1000 if argv[1] == "inputs/06" else 10

P = []
for l in F:
    x, y = util.scan("%d, %d", l)
    P.append((x,y))
G = util.grid(SIZE, -1)
for i in range(SIZE):
    for j in range(SIZE):
        m = SIZE*4
        for idx, p in enumerate(P):
            v = util.manhattan(i, j, p[0], p[1])
            if v < m:
                m = v
                G[i][j] = idx
            elif v == m:
                G[i][j] = -1
E = set()
for i in range(SIZE):
    E.add(G[i][0])
    E.add(G[0][i])
    E.add(G[i][SIZE-1])
    E.add(G[SIZE-1][i])
R = [0 for _ in P]
for i in range(len(P)):
    if i in E:
        continue
    S = 0
    for x in range(SIZE):
        for y in range(SIZE):
            if G[x][y] == i:
                S += 1
    R[i] = S
print(max(R))

S = 0
for i in range(SIZE):
    for j in range(SIZE):
        D = 0
        for p in P:
            D += util.manhattan(i, j, p[0], p[1])
        if D < 10000:
            S += 1
print(S)
