import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
V = set()
R = {}
D = defaultdict(lambda: defaultdict(lambda: math.inf))

for l in F:
    v, r, xs = ul.scan("Valve %s has flow rate=%d; %s", l)
    V.add(v)
    R[v] = r
    for n in [x.strip(", ") for x in xs.split()[4:]]:
        D[v][n] = 1

for b, a, c in itertools.product(V, repeat=3):
    D[a][c] = min(D[a][c], D[a][b] + D[b][c])

@functools.cache
def pressure(current, opened, time):
    if time == 0: return 0

    max_score = 0
    for (next, dist) in D[current].items():
        if next in opened or not R[next]: continue
        if time-dist > 0:
            ntime = time-dist-1
            max_score = max(max_score, pressure(next, frozenset(opened | {next}), ntime) + ntime*R[next])
    return max_score
print(pressure("AA", frozenset(), 30))

P = defaultdict(int)
def gen_paths(current, opened, time, score):
    P[opened] = max(P[opened], score)
    if time == 26: return

    for (next, dist) in D[current].items():
        if next in opened or not R[next]: continue
        if time+dist < 26:
            ntime = time+dist+1
            gen_paths(next, frozenset(opened | {next}), ntime, score + (26-ntime)*R[next])
gen_paths("AA", frozenset(), 0, 0)
print(max(pressure("AA", p, 26) + s for (p, s) in P.items()))
