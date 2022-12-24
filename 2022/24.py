import collections
from sys import argv

F = [l.strip() for l in open(argv[1])]
G = {}

for r in range(len(F)):
    for c in range(len(F[r])):
        if not (r,c) in G:
            G[(r,c)] = []
        v = F[r][c]
        if v != "#" and v != ".":
            G[(r,c)].append(v)


def tick_blizzards(G):
    NG = {}
    dirs = {
            "<": (0, -1),
            ">": (0, 1),
            "v": (1, 0),
            "^": (-1, 0)
    }
    for key in G.keys():
        val = G[key]
        for blizzard in val:
            d = dirs[blizzard]
            v = [d[0] + key[0], d[1] + key[1]]
            if v[0] == 0:
                v[0] = len(F) - 2
            elif v[0] == len(F) - 1:
                v[0] = 1
            if v[1] == 0:
                v[1] = len(F[0]) - 2
            elif v[1] == len(F[0]) - 1:
                v[1] = 1
            v = tuple(v)
            if not v in NG:
                NG[v] = []
            NG[v].append(blizzard)
    return NG

BT = []
MAXSTEPS = 2000
for i in range(MAXSTEPS):
    G = tick_blizzards(G)
    BT.append(G)

def bfs(start, goal):
    Q = collections.deque([start])
    V = set()
    while Q:
        E = Q.popleft()
        if E[0] == goal:
            return E[1]
        if E[1] > MAXSTEPS - 1:
            continue
        dirs = [
            (0, -1),
            (0, 1),
            (1, 0),
            (-1, 0),
            (0, 0),
        ]

        G = BT[E[1]]
        for d in dirs:
            p = E[0]
            np = (p[0] + d[0], p[1] + d[1])
            if np in G or np[0] > len(F) - 1 or F[np[0]][np[1]] == "#":
                continue
            if (np,E[1]+1) in V:
                continue
            V.add((np,E[1]+1))
            Q.append((np,E[1]+1))

v = bfs(((0,1),0), (len(F)-1,len(F[0])-2))
v = bfs(((len(F)-1,len(F[0])-2), v), (0,1))
v = bfs(((0,1),v), (len(F)-1,len(F[0])-2))
print(v)
