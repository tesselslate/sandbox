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

for l in F:
    a = []
    for c in l:
        if c.isdigit(): a.append(c)
    S += int(str(a[0]) + str(a[-1]))
print(S)

d = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

S = 0
for l in F:
    a = []
    for i, c in enumerate(l):
        if c.isdigit(): a.append(c)
        for w in d:
            if l[i:].startswith(w):
                a.append(d.index(w) + 1)
    v = int(str(a[0]) + str(a[-1]))
    S += v
print(S)
