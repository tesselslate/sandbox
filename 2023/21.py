import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F)

sr, sc = 0, 0
for (r,c) in ul.gridpoints(G):
    if G[r][c] == "S": sr, sc = r, c; break

def occupied(sr, sc, N):
    V = defaultdict(set)
    V[0].add((sr,sc))
    Q = deque([(sr,sc,0)])
    while len(Q):
        (r,c,d) = Q.popleft()
        for rr, cc in ul.padj4():
            rr, cc = rr+r, cc+c
            if G[rr%len(G)][cc%len(G)] == "#": continue
            if (rr,cc) in V[d]: continue
            V[d].add((rr,cc))
            if d < N: Q.append((rr,cc,d+1))
    return V[N-1]
print(len(occupied(65, 65, 64)))

def n_points(P, r, c):
    sr, sc = r * 131, c * 131
    er, ec = sr + 131, sc + 131
    return len(set((r,c) for (r,c) in itertools.product(range(sr, er), range(sc, ec)) if (r,c) in P))

p = occupied(65, 65, 589)

# 589
x = """
0 0    0    0    0    0    0    0    0    0    0
0 0    0    0    928  5526 951  0    0    0    0
0 0    0    928  6412 7367 6443 951  0    0    0
0 0    928  6412 7367 7329 7367 6443 951  0    0
0 928  6412 7367 7329 7367 7329 7367 6443 951  0
0 5537 7367 7329 7367 7329 7367 7329 7367 5530 0
0 941  6454 7367 7329 7367 7329 7367 6416 949  0
0 0    941  6454 7367 7329 7367 6416 949  0    0
0 0    0    941  6454 7367 6416 949  0    0    0
0 0    0    0    941  5541 949  0    0    0    0
0 0    0    0    0    0    0    0    0    0    0
"""
# nums = Counter(int(x) for x in re.findall(r'\d+', x))
# print(nums)

center1     = n_points(p, 0, 0)
center2     = n_points(p, 0, 1)
l_corner    = n_points(p, 0, -4)
r_corner    = n_points(p, 0, 4)
b_corner    = n_points(p, 4, 0)
t_corner    = n_points(p, -4, 0)
o_tl_edge   = n_points(p, -4, -1)
i_tl_edge   = n_points(p, -3, -1)
o_tr_edge   = n_points(p, -4, 1)
i_tr_edge   = n_points(p, -3, 1)
o_bl_edge   = n_points(p, 4, -1)
i_bl_edge   = n_points(p, 3, -1)
o_br_edge   = n_points(p, 4, 1)
i_br_edge   = n_points(p, 3, 1)

N = 202300
N2 = N-1

# n = Counter([l_corner, r_corner, b_corner, t_corner])
# n[center1] = sum(range(1, N2))*2 - N2
# n[center2] = sum(range(1, N))*2 - N
# for x in [o_tl_edge,o_tr_edge,o_bl_edge,o_br_edge]: n[x] = N
# for x in [i_tl_edge,i_tr_edge,i_bl_edge,i_br_edge]: n[x] = N2
# print(n)

# 1*center2
# 2*center2, 1*center1
# 3*center2, 2*center1
# ...
# 202300*center2, 202299*center1
# ...
# 3*center2, 2*center1

corners = sum([l_corner, r_corner, b_corner, t_corner])
edges = sum(N * a + N2 * b for (a,b) in zip([o_tl_edge, o_tr_edge, o_bl_edge, o_br_edge], [i_tl_edge, i_tr_edge, i_bl_edge, i_br_edge]))
center1 = (sum(range(1, N2))*2 + N2) * center1
center2 = (sum(range(1, N))*2 + N) * center2
print(corners + edges + center1 + center2)

# 599879935521506 too low
# 599879937125674 too low
# 601435117179596 too low
