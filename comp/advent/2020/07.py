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

S = 0
G = defaultdict(dict)

for l in F:
    a, b, c = ul.scan("%s %s bags contain %s", l.strip("."))
    key = " ".join([a,b])
    if "no other bags" in c:
        continue
    for i in range(0, len(c), 4):
        x = c.split(" ")[i:i+4]
        if len(x) == 0:
            break
        n, y, z = int(x[0]), x[1], x[2]
        key2 = " ".join([y, z])
        G[key][key2] = n

v = set()
def re(t):
    global v
    for k in t.keys():
        v.add(k)
        if k in G:
            re(G[k])
    
G = ul.rev_graph(G)
re(G["shiny gold"])
print(len(v))

G = ul.rev_graph(G)
def re2(t):
    s = 0
    for k, v in t.items():
        if k in G:
            s += (1 + re2(G[k])) * v
        else:
            s += v
    return s
print(re2(G["shiny gold"]))
