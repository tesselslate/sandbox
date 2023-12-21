import itertools, math, ul
from copy import deepcopy
from collections import Counter, defaultdict

F = ul.input()
F = ul.double_linefeed(F)

T = {}
for ll in F:
    n, = ul.scan("Tile %d:", ll[0])
    T[n] = ul.grid(ll[1:])

B = {}
R = defaultdict(Counter)
M = defaultdict(lambda: math.inf)
for n, g in T.items():
    borders = [ul.gcol(g, 0), ul.gcol(g, -1), g[0], g[-1]]
    borders += [reversed(x) for x in borders]
    B[n] = ["".join(x) for x in borders]
matches = Counter()
for k, v in B.items():
    for k2 in B.keys():
        if k == k2: continue
        for v2 in B[k2]:
            if v2 in v:
                matches[k] += 1
                R[k][k2] += 1
                M[k, k2] = 1
for k in matches: matches[k] //= 2
corners = [k for k, v in matches.items() if v == 2]
print(math.prod(corners))

adj = lambda k: list(R[k].keys())

for b, a, c in itertools.product(R.keys(), repeat=3):
    M[a, c] = min(M[a, c], M[a, b] + M[b, c])

# pick a corner, fill edges, fill grid
sz = math.isqrt(len(T))
G = [[-1 for _ in range(sz)] for _ in range(sz)]
G[0][0] = corners[0]
G[0][1] = adj(corners[0])[0]
G[1][0] = adj(corners[0])[1]
used = set([G[0][0], G[0][1], G[1][0]])

rg = [k for k in corners if M[G[0][1], k] == 10 and matches[k] == 2]
cg = [k for k in corners if M[G[1][0], k] == 10 and matches[k] == 2]
assert len(rg) == len(cg) == 1
rg, cg = rg[0], cg[0]
G[0][-1] = rg
G[-1][0] = cg
for i in range(2,sz-1):
    for k in R.keys():
        if M[rg, k] == sz-i-1 and M[G[0][0], k] == i:
            G[0][i] = k
            used.add(k)
            break
    for k in R.keys():
        if M[cg, k] == sz-i-1 and M[G[0][0], k] == i:
            G[i][0] = k
            used.add(k)
            break

while True:
    found = False
    for (r,c) in ul.gridpoints(G):
        if G[r][c] > 0: continue
        adj = []
        for (rr, cc) in ul.padj4():
            rr, cc = rr+r, cc+c
            if not ul.gridcheck(G,rr,cc): continue
            if G[rr][cc] > 0: adj.append(G[rr][cc])
        if len(adj) == 2:
            adj = set.intersection(*[set(R[k].keys()) for k in adj]) - used
            assert len(adj) == 1
            nk = list(adj)[0]
            G[r][c] = nk
            found = True
            used.add(nk)
    if not found:
        break

# we have the grid, apply transformations to each pair of adjacent tiles until
# they work
# ag is to left of bg (horiz)
# ag is above bg (vert)
def matches(ag, bg, horiz):
    if horiz: return ul.gcol(ag, -1) == ul.gcol(bg, 0)
    else: return ag[-1] == bg[0]

def transforms(grid):
    out = []
    for i in range(4):
        g = deepcopy(grid)
        for _ in range(i): g = [list(reversed(x)) for x in ul.transpose(g)]
        out.append(g)

        g = deepcopy(grid)
        g = list(reversed(g))
        for _ in range(i): g = [list(reversed(x)) for x in ul.transpose(g)]
        out.append(g)

        g = deepcopy(grid)
        for r in range(len(g)): g[r] = list(reversed(g[r]))
        for _ in range(i): g = [list(reversed(x)) for x in ul.transpose(g)]
        out.append(g)
    return out

def pg(g):
    for r in g:
        print("".join(r))

TT = {}
for (r,c) in ul.gridpoints(G):
    TT[G[r][c]] = transforms(T[G[r][c]])

for (r,c) in ul.gridpoints(G):
    ok = TT[G[r][c]]

    left = TT[G[r][c-1]] if c > 0 else []
    right = TT[G[r][c+1]] if c < len(G[0])-1 else []
    down = TT[G[r+1][c]] if r < len(G)-1 else []
    up = TT[G[r-1][c]] if r > 0 else []

    okl, okr, okd, oku = set(), set(), set(), set()
    for a, b in itertools.product(left, ok):
        if matches(a, b, True): okl.add("\n".join("".join(r) for r in b))
    for a, b in itertools.product(right, ok):
        if matches(b, a, True): okr.add("\n".join("".join(r) for r in b))
    for a, b in itertools.product(down, ok):
        if matches(b, a, False): okd.add("\n".join("".join(r) for r in b))
    for a, b in itertools.product(up, ok):
        if matches(a, b, False): oku.add("\n".join("".join(r) for r in b))
    fin = set.intersection(*[oks for (oks, transformations) in zip([okl,okr,okd,oku], [left,right,down,up]) if transformations])
    assert len(fin) == 1
    T[G[r][c]] = ul.grid(list(fin)[0].split("\n"))

NT = {}
gsz = 0
for k, v in T.items():
    g = v
    del g[0], g[-1]
    for r in range(len(g)): g[r] = g[r][1:-1]
    NT[k] = g
    gsz = len(g)

nsz = sz * gsz
GG = [['.' for _ in range(nsz)] for _ in range(nsz)]
for (r,c) in ul.gridpoints(G):
    g = NT[G[r][c]]
    for (rr,cc) in ul.gridpoints(g):
        GG[r*gsz+rr][c*gsz+cc] = g[rr][cc]

S = 0
pat = [
        "..................#.",
        "#....##....##....###",
        ".#..#..#..#..#..#..."]

GG = ["".join(r) for r in GG]

def checkpat(r, c):
    xs = set()
    for rr in range(3):
        for i, (a, b) in enumerate(zip(GG[r+rr][c:], pat[rr])):
            if b == "#":
                if a == ".": return False, None
                xs.add((r+rr,i+c))

    return True, xs

for GG in transforms(GG):
    hs = set((r,c) for (r,c) in ul.gridpoints(GG) if GG[r][c] == "#")
    xs = set()
    for r in range(len(GG) - 2):
        for c in range(len(GG) - 19):
            ok, new = checkpat(r,c)
            if ok: xs |= new
    if len(xs):
        print(len(hs-xs))
        break
