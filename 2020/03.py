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
g = ul.grid(F)

i,j,k,x,y= 0,0,0,0,0

c = 0
for r in range(len(g)):
    if g[r][c] == "#":
        i += 1
    c = (c + 3) % len(g[0])
c = 0
for r in range(len(g)):
    if g[r][c] == "#":
        j += 1
    c = (c + 1) % len(g[0])
c = 0
for r in range(len(g)):
    if g[r][c] == "#":
        k += 1
    c = (c + 5) % len(g[0])
c = 0
for r in range(len(g)):
    if g[r][c] == "#":
        x += 1
    c = (c + 7) % len(g[0])
c = 0
for r in range(0, len(g), 2):
    if g[r][c] == "#":
        y += 1
    c = (c + 1) % len(g[0])
c = 0
print(i*j*k*x*y)
