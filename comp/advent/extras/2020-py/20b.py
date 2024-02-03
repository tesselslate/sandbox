import functools, math, re, string, sys, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

if len(sys.argv) > 1:
    F = open(sys.argv[1])
else:
    F = sys.stdin.readlines()

F = [l.strip() for l in F]
while F[-1] == "":
    del F[-1]
F = ul.double_linefeed(F)
T = {}
for ll in F:
    n, = ul.scan("Tile %d:", ll[0])
    T[n] = ul.grid(ll[1:])

S = 0

def top(g):
    return g[0]

def bot(g):
    return g[-1]

def left(g):
    return [g[i][0] for i in range(len(g))]

def right(g):
    return [g[i][-1] for i in range(len(g))]

n_matches = Counter()
matches = defaultdict(Counter)
matches2 = defaultdict(dict)

borders = {}
for n, grid in T.items():
    b = [top(grid), bot(grid), left(grid), right(grid)]
    b += list(reversed(x) for x in b)
    borders[n] = ["".join(x) for x in b]

for k, v in borders.items():
    for k2 in borders.keys():
        if k == k2: continue
        for v2 in borders[k2]:
            for vv in v:
                if v2 == vv:
                    n_matches[k] += 1
                    matches[k][k2] += 1
                    matches2[k][k2] = True
for k in n_matches.keys():
    n_matches[k] /= 2 # handle reversed borders
print(math.prod(k for (k, v) in n_matches.items() if v == 2))

# this solution only works on even grids
assert math.isqrt(len(n_matches)) % 2 == 0

# part 2
# start by doing BFS from each tile to all others to find the minimum distance
# yes i need to learn floyd-warshall eventually
md = defaultdict(dict)
for k in matches.keys():
    Q = deque([(k,0)])
    V = set([k])
    while len(Q):
        E = Q.popleft()
        md[k][E[0]] = E[1]
        for adj in matches[E[0]].keys():
            if adj in V:
                continue
            V.add(adj)
            Q.append((adj,E[1]+1))
    assert len(md[k]) == len(n_matches)

# we will build the tile grid in concentric rings
# each element of grids will represent a ring, where inner tiles are filled with None
# we will solve for the whole grid by brute forcing all rotations at the end (4^6 on my input)
grids = []
def build_ring():
    ring_size = math.isqrt(len(n_matches))

    # find the 4 corners of this ring
    corners = [k for (k,v) in n_matches.items() if v == 2]
    assert len(corners) == 4

    # find the 2 midpoint tiles of each edge
    cm = {}
    for corner in corners:
        cm[corner] = {x for x in md[corner].keys() if md[corner][x] == (ring_size / 2 - 1)}
    midpoints = set.union(*cm.values())
    for corner in corners:
        M = math.inf
        nm = set()
        for midpoint in cm[corner]:
            for maybe_adj in midpoints:
                if md[midpoint][maybe_adj] == 1:
                    nm.add(midpoint)
        assert len(nm) == 2
        cm[corner] = nm
    midpoints = set.union(*cm.values())

    # cm now contains the midpoints adjacent to each corner
    # find the 2nd midpoint of each edge from each corner
    for corner in corners:
        [a, b] = cm[corner]
        x, y = None, None
        for m in midpoints:
            if md[a][m] == 1: x = m
            if md[b][m] == 1: y = m
        assert x and y
        cm[corner] = (a, b, x, y)

    # cm now contains the 2 midpoints on each edge the corner is on
    # (a, b, x, y) - A and X are a pair, B and Y are a pair
    # A and B are closest, X and Y are furthest
    #
    # cAX.
    # B...
    # Y...
    # ....

    # find which corners are adjacent to one another
    adj = {}
    for corner in corners:
        a = []
        _, _, x, y = cm[corner]
        for corner2 in corners:
            if corner2 == corner: continue
            if x in cm[corner2]: a.append(corner2)
            if y in cm[corner2]: a.append(corner2)
        assert len(a) == 2
        adj[corner] = tuple(a)

    # create a list of the adjacent corners
    cl = [corners[0]]
    while len(cl) < 4:
        c = cl[-1]
        for x in adj[c]:
            if x not in cl:
                cl.append(x)
                break
        else:
            assert False

    # now we know the order the 4 corners are in, but not their rotation
    # solve for the edges
    edges = []
    for (a, b) in itertools.chain(itertools.pairwise(cl), [(cl[-1], cl[0])]):
        edge = []
        for i in range(ring_size):
            for k in n_matches.keys():
                if md[a][k] == i and md[b][k] == ring_size - i - 1:
                    edge.append(k)
                    break
            else:
                assert False
        edges.append(edge)

    # create a grid from the edges and add it to the list of `grids`
    G = [[None for _ in range(ring_size)] for _ in range(ring_size)] 
    for i, x in enumerate(edges[0]):
        G[0][i] = x
    for i, x in enumerate(edges[1]):
        G[i][-1] = x
    for i, x in enumerate(edges[2]):
        G[-1][-i-1] = x
    for i, x in enumerate(edges[3]):
        G[-i-1][0] = x
    grids.append(G)

    # remove all of the tiles in this ring from consideration for next rings
    V = set.union(*[set(x) for x in edges])
    for x in V:
        del md[x]
        for k in md:
            del md[k][x]

        for k in matches[x].keys():
            if k not in V:
                n_matches[k] -= 1
                del matches[k][x]
        del matches[x]
        del n_matches[x]

    assert len(matches) == len(n_matches) == len(md)
    assert ring_size ** 2 > len(n_matches)

while len(n_matches) > 4:
    build_ring()

# at the last ring, we need to build the edges list manually (our midpoint detection etc no longer works)
assert len(n_matches) == 4
def build_last_ring():
    corners = list(n_matches.keys())
    cl = [corners[0]]
    while len(cl) < 4:
        c = cl[-1]
        for x in matches[c].keys():
            if x not in cl and md[c][x] == 1:
                cl.append(x)
                break
        else:
            assert False
    grid = [[cl[0], cl[1]], [cl[3], cl[2]]]
    grids.append(grid)
build_last_ring()

# create each rotation ahead of time
def make_rots(grid):
    rots = []

    def rotate90(grid):
        ng = [[None for _ in range(len(grid))] for _ in range(len(grid))]

        # this wastes time on the whole None center but i dont care
        for (r, c) in ul.gridpoints(grid):
            if grid[r][c] != None:
                ng[c][-1-r] = grid[r][c]
        return ng

    for i in range(4):
        ng = grid
        for j in range(i):
            ng = rotate90(ng)
        rots.append(ng)

    return rots
rots = [make_rots(x) for x in grids]

# brute force rotations to match
matches = matches2
grid_size = math.isqrt(len(matches))
good = None

for rl in itertools.product(range(4), repeat=grid_size // 2):
    G = [[None for _ in range(grid_size)] for _ in range(grid_size)]

    # create the grid
    for i in range(grid_size // 2):
        g = rots[i][rl[i]]
        for (r, c) in ul.gridpoints(g):
            G[r+i][c+i] = g[r][c]
    for (r, c) in ul.gridpoints(G):
        n = G[r][c]

    # test the grid
    for (r, c) in ul.gridpoints(G):
        n = G[r][c]
        adj = []
        for (rr, cc) in ul.padj4():
            rr += r
            cc += c
            if ul.gridcheck(G, rr, cc):
                adj.append(G[rr][cc])

        for x in adj:
            if x not in matches[n]:
                break
        else:
            continue
        break
    else:
        good = tuple(rl)
        print("found rotation sequence", good)
        break
else:
    print("no sequence")
    exit()
