import itertools, ul
from collections import defaultdict, deque

F = ul.input()
G = ul.grid(F)
G = {(r,c) for (r,c) in ul.gridpoints(G) if G[r][c] == "#"}
D = deque("NSWE")
P = {
    "N": [ul.offset_rc(x) for x in ["N","NW","NE"]],
    "S": [ul.offset_rc(x) for x in ["S","SW","SE"]],
    "W": [ul.offset_rc(x) for x in ["W","SW","NW"]],
    "E": [ul.offset_rc(x) for x in ["E","SE","NE"]],
}

def check(r,c,d):
    for p in P[d]:
        if (r+p[0], c+p[1]) in G: return False
    return True

def turn():
    proposals = defaultdict(list)
    for (r,c) in G:
        if not set((r+rr, c+cc) for (rr, cc) in ul.padj8() if (r+rr, c+cc) in G):
            continue
        for dir in D:
            if check(r, c, dir):
                d = ul.offset_rc(dir)
                proposals[r+d[0], c+d[1]].append((r,c))
                break
    n = 0
    for goto, elves in proposals.items():
        if len(elves) > 1: continue
        G.remove(elves[0])
        G.add(goto)
        n += 1
    D.rotate(-1)
    return n

for i in itertools.count():
    n = turn()
    if i == 9:
        rm, RM = ul.minmax(*{r for (r,c) in G})
        cm, CM = ul.minmax(*{c for (r,c) in G})
        print((RM-rm+1)*(CM-cm+1)-len(G))
    if not n: print(i+1); break
