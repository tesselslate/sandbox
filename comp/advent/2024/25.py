import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.double_linefeed(ul.input())
GS = [ul.grid(x) for x in F]

locks = []
keys = []

for G in GS:
    if all(x == "#" for x in G[0]) and all(x == "." for x in G[-1]):
        locks.append(G)
    else:
        keys.append(G)

nlocks = []
nkeys = []
for lock in locks:
    heights = []
    for i in range(len(lock[0])):
        col = ul.gcol(lock, i)
        heights.append(col.index(".")-1)
    nlocks.append(tuple(heights))

for key in keys:
    heights = []
    for i in range(len(key[0])):
        col = ul.gcol(key, i)
        heights.append(col.count("#") - 1)
    nkeys.append(tuple(heights))

pairs = set()
for lock in nlocks:
    for key in nkeys:
        print(lock,key)
        for a, b in zip(lock, key):
            if a+b > 5: break
        else: pairs.add((lock, key))
print(len(pairs))
