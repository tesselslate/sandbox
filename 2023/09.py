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

F = [[int(y) for y in x.split()] for x in F]

S = 0
for l in F:
    histories = [l.copy()]
    while not all(x == 0 for x in histories[-1]):
        xs = []
        for (a, b) in itertools.pairwise(histories[-1]):
            xs.append(b-a)
        histories.append(xs)
    for x in histories:
        S += x[-1]
print(S)

S = 0
for l in F:
    histories = [l.copy()]
    while not all(x == 0 for x in histories[-1]):
        xs = []
        for (b, a) in itertools.pairwise(histories[-1]):
            xs.append(b-a)
        histories.append(xs)
    for x in histories:
        S += x[0]
print(S)
