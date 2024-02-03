import functools, math, re, string, sys, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

if len(sys.argv) > 1:
    F = open(sys.argv[1])
else:
    F = sys.stdin.readlines()
    if not F[-1].strip():
        del F[-1]

F = [l.strip() for l in F]
S = set([int(l) for l in F])

builtin = max(S) + 3
d1, d3 = 0, 0
S.add(builtin)
S.add(0)

i = 0
while i < builtin:
    if i + 1 in S:
        d1 += 1
        i = i +1
    elif i + 2 in S:
        i = i + 2
    elif i + 3 in S:
        d3 += 1
        i = i + 3
    else:
        assert False
print(d1*d3)

@functools.cache
def path(x):
    v = 0
    if x == 0:
        return 1
    if x-3 in S:
        v += path(x-3)
    if x-2 in S:
        v += path(x-2)
    if x-1 in S:
        v += path(x-1)
    return v

# S = 0
# V = set()
# Q = deque([builtin])
# while len(Q) > 0:
#     E = Q.pop()
#     if E in G:
#         for k in G[E].keys():
#             Q.append(k)
#             S += 1
# print(S)
print(path(builtin))
