import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

from z3 import *

F = ul.double_linefeed(ul.input())

a = Int("a")
b = Int("b")

def solve(ax, ay, bx, by, px, py, d):
    opt = Optimize()
    opt.minimize(3*a + b)
    opt.add(a * ax + b * bx == px + d)
    opt.add(a * ay + b * by == py + d)
    if opt.check() == sat:
        model = opt.model()
        return model[a].as_long() * 3 + model[b].as_long()
    else:
        return 0

S1, S2 = 0, 0
for ll in F:
    ax, ay = ul.ints(ll[0])
    bx, by = ul.ints(ll[1])
    px, py = ul.ints(ll[2])

    S1 += solve(ax, ay, bx, by, px, py, 0)
    S2 += solve(ax, ay, bx, by, px, py, 10000000000000)

print(S1)
print(S2)
