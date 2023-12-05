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
F = ul.double_linefeed(F)

seeds = [int(x) for x in F[0][0].split()[1:]]
maps, rmaps = {}, {}
fmap, rmap = {}, {}

for l in F[1:]:
    k1, k2 = ul.scan("%s-to-%s map:", l[0])
    maps[k1] = []
    rmaps[k2] = []
    fmap[k1] = k2
    rmap[k2] = k1
    for l in l[1:]:
        xs = [int(x) for x in l.split()]
        maps[k1].append(xs)
        rmaps[k2].append([xs[1], xs[0], xs[2]])

M = 999999999999999
for s in seeds:
    S = s
    p = "seed"
    while p != "location":
        for xs in maps[p]:
            if xs[1] <= S <= xs[1]+xs[2]:
                S = S - xs[1] + xs[0]
                break
        p = fmap[p]
    if S < M:
        M = S
print(M)

for i in itertools.count():
    S = i
    p = "location"
    while p != "seed":
        for xs in rmaps[p]:
            if xs[1] <= S < xs[1]+xs[2]:
                S = S - xs[1] + xs[0]
                break
        p = rmap[p]
    for x1, x2 in ul.batched(seeds, 2):
        if x1 <= S < x1 + x2:
            print(i)
            exit()
