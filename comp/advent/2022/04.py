import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

S = 0
S2 = 0
for l in F:
    a, b, c, d = ul.scan("%d-%d,%d-%d", l)
    x = range(a,b+1)
    y = range(c,d+1)
    if set(x) <= set(y) or set(y) <= set(x):
        S += 1
    if set(x) & set(y):
        S2 += 1
print(S)
print(S2)
