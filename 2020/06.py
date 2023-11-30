import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = open(argv[1]).read()
F = [l.strip() for l in F.split("\n\n")]
print(F)

T = 0
for l in F:
    S = set()
    for c in l:
        if c != "\n":
            S.add(c)
    T += len(S)
print(T)

T = 0
for l in F:
    ls = [l.strip() for l in l.split("\n")]
    
    sets = []
    B = {}
    for x in ls:
        for c in x:
            if c not in B:
                B[c] = 0
            B[c] += 1
    for k, v in B.items():
        if v == len(ls):
            T +=1
print(T)
