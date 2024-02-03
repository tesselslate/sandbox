import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])][0]
S = 0

F = [int(x) for x in F.split()]

def read(idx):
    global S
    cc = F[idx]
    mc = F[idx+1]
    idx += 2
    for _ in range(cc):
        idx = read(idx)
    for _ in range(mc):
        S += F[idx]
        idx += 1
    return idx

read(0)
print(S)

def nread(idx):
    cc = F[idx]
    mc = F[idx+1]
    idx += 2
    s = 0
    children = []
    for _ in range(cc):
        idx, val = nread(idx)
        children.append(val)
    for _ in range(mc):
        if cc == 0:
            s += F[idx]
        elif F[idx] <= len(children):
            s += children[F[idx]-1]
        idx += 1
    return idx, s

print(nread(0))
