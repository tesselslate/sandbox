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

S = 0
c = [0 for _ in F]
for l in F:
    n, w, h = ul.scan("Card %d: %s| %s", l)
    w = set([int(w.strip()) for w in w.split()])
    h = set([int(h.strip()) for h in h.split()])
    v = len(w&h)
    if v:
        S += 2 ** (v-1)
        for i in range(n, n+v):
            c[i] += c[n-1] + 1
print(S)
print(sum(c) + len(c))
