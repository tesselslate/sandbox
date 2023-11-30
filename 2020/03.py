import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]
G = []

for l in F:
    a = []
    for c in l:
        a += [c]
    G += [a]

x = 0
S = 0
for i in range(0, len(F)):
    if G[i][x] == "#":
        S += 1
    x = (x + 3) % len(F[0])
print(S)

a,b,c,d,e=0,0,0,0,0
x=0
for i in range(0, len(F)):
    if G[i][x] == "#":
        a += 1
    x = (x + 1) % len(F[0])
x=0
for i in range(0, len(F)):
    if G[i][x] == "#":
        b += 1
    x = (x + 3) % len(F[0])
x=0
for i in range(0, len(F)):
    if G[i][x] == "#":
        c += 1
    x = (x + 5) % len(F[0])
x=0
for i in range(0, len(F)):
    if G[i][x] == "#":
        d += 1
    x = (x + 7) % len(F[0])
x=0
for i in range(0, len(F), 2):
    if G[i][x] == "#":
        e += 1
    x = (x + 1) % len(F[0])
print(a*b*c*d*e)
