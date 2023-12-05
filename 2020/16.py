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

def proc(x):
    _, a, b, c, d = ul.scan("%s: %d-%d or %d-%d", x)
    return ((a,b),(c,d))

criteria = [proc(x) for x in F[0]]

def inval(xs):
    for x in xs:
        v = 0
        for c in criteria:
            if (c[0][0] <= x <= c[0][1]) or (c[1][0] <= x <= c[1][1]):
                v += 1
        if v == 0:
            return x
    return None

S = 0
invalid = []
for i, t in enumerate(F[2][1:]):
    xs = [int(x) for x in t.strip().split(",")]
    v = inval(xs)
    if type(v) == int:
        S += v
        invalid.append(i+1)
print(S)

invalid.sort()
invalid.reverse()
for i in invalid:
    del F[2][i]

mappings = []
for t in F[2][1:]:
    xs = [int(x) for x in t.strip().split(",")]
    mapping = [set() for i in criteria]
    for i, x in enumerate(xs):
        for j, c in enumerate(criteria):
            if (c[0][0] <= x <= c[0][1]) or (c[1][0] <= x <= c[1][1]):
                mapping[j].add(i)
    mappings.append(mapping)

mappings = [set.intersection(*[mappings[i][x] for i in range(len(mappings))]) for x in range(len(mappings[0]))]

while max(map(len, mappings)) > 1:
    i = 0
    for i in range(len(mappings)):
        if len(mappings[i]) == 1:
            D = list(mappings[i])[0]
            for j in range(len(mappings)):
                if i != j and D in mappings[j]: mappings[j].remove(D)

S = []
xs = [int(x) for x in F[1][1].split(",")]
for i, mapping in enumerate(mappings):
    v = list(mapping)[0]
    l = F[0][i]
    if l.startswith("departure"):
        S.append(xs[v])
print(mappings)
print(math.prod(S))
