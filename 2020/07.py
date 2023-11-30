import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]

G = {}
Z = {}
for l in F:
    w = l.split()
    t = " ".join([w[0], w[1]])
    w = w[4:]
    if "no other bags" in l:
        continue
    for i in range(0, len(w), 4):
        k = " ".join([w[1+i], w[i+2]])
        if k not in G:
            G[k] = {}
        G[k][t] = int(w[i])
        if t not in Z:
            Z[t] = {}
        Z[t][k] = int(w[i])

S = set()
def recurse(tbl):
    global S
    for k in tbl.keys():
        S.add(k)
        if k in G:
            recurse(G[k])
recurse(G["shiny gold"])
print(len(S))

def re2(tbl):
    a = 0
    for k, v in tbl.items():
        if k in Z:
            a += v * (re2(Z[k])+1)
        else:
            a += v
    return a
print(re2(Z["shiny gold"]))
