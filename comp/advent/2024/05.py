import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

P, U = ul.double_linefeed(ul.input())

R = set()
for l in P:
    a, b = l.split("|")
    R.add((int(a), int(b)))

def check(P):
    for a, b in itertools.pairwise(P):
        if (b,a) in R: return False
    return True

def sort(P):
    while not check(P):
        for (i, j) in itertools.product(range(len(P)), repeat=2):
            if (P[i], P[j]) in R:
                P[i], P[j] = P[j], P[i]

S = 0
S2 = 0
for u in U:
    p = ul.ints(u)
    if check(p):
        S += p[len(p)//2]
    else:
        sort(p)
        S2 += p[len(p)//2]
print(S)
print(S2)
