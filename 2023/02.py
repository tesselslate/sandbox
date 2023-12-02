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

R = 12
G = 13
B = 14
for i, l in enumerate(F):
    n, b = ul.scan("Game %d: %s", l)
    good = True
    for game in b.split(";"):
        for w in game.split(","):
            w = w.strip().split()
            x = int(w[0])
            t = w[1]
            if t == "blue" and x > B:
                good = False
            if t == "red" and x > R:
                good = False
            if t == "green" and x > G:
                good = False
    if good:
        S += i+1
print(S)

S = 0
for i, l in enumerate(F):
    n, b = ul.scan("Game %d: %s", l)
    good = True
    mr,mg,mb=0,0,0
    for game in b.split(";"):
        for w in game.split(","):
            w = w.strip().split()
            x = int(w[0])
            t = w[1]
            if t == "blue" and x > mb:
                mb = x
            if t == "red" and x > mr:
                mr = x
            if t == "green" and x > mg:
                mg = x
    if good:
        S += mr*mg*mb
print(S)
