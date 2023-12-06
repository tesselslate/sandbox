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

times = ul.ints(F[0])
distances = ul.ints(F[1])
S = 0

def sim(t, md):
    v = 0
    for i in range(t):
        d = (t - i) * i
        if d > md:
            v += 1
    return v

S = []
for t, d in zip(times, distances):
    S.append(sim(t,d))
print(math.prod(S))

time = int("".join(F[0].split()[1:]))
dist = int("".join(F[1].split()[1:]))
print(sim(time,dist))
