import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
dirs = "LDRU"

def sim(N):
    knots = [(0,0) for _ in range(N)]
    v = set((0,0))

    def proc(h, t):
        return (t[0] - ul.sign(t[0]-h[0]), t[1] - ul.sign(t[1]-h[1]))

    for l in F:
        d, n = ul.scan("%s %d", l)
        (r, c) = knots[0]
        (rr, cc) = ul.padj4()[dirs.index(d)]
        for _ in range(n):
            r += rr
            c += cc
            knots[0] = (r, c)
            for i in range(1, N):
                while abs(knots[i][0] - knots[i-1][0]) > 1 or abs(knots[i][1] - knots[i-1][1]) > 1:
                    knots[i] = proc(knots[i-1], knots[i])
                    if i == N-1: v.add(knots[i])
    return len(v)
print(sim(2))
print(sim(10))
