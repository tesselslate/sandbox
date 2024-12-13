import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.double_linefeed(ul.input())

def solve(ax, ay, bx, by, px, py):
    # solve the system by elimination:
    # a*ax + b*bx = px
    # a*ay + b*by = py

    # coeff * (a*ay + b*by) = coeff * py
    # a*ax and a*ay cancel out when the equations are added
    coeff = -ax/ay

    lhs_coeff = bx + coeff * by
    rhs = px + coeff * py

    b = rhs / lhs_coeff
    a = (px-b*bx) / ax

    # check if the solution works (a and b are both integers)
    a, b = round(a), round(b)

    if ax*a + bx*b == px and ay*a + by*b == py:
        return a * 3 + b
    else:
        return 0

D = 10000000000000

S1, S2 = 0, 0
for ll in F:
    ax, ay = ul.ints(ll[0])
    bx, by = ul.ints(ll[1])
    px, py = ul.ints(ll[2])

    S1 += solve(ax, ay, bx, by, px, py)
    S2 += solve(ax, ay, bx, by, px + D, py + D)

print(S1)
print(S2)
