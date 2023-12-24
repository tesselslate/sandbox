import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

fs = {}
cd = []

def gd():
    dir = fs
    for d in cd:
        if d not in dir: dir[d] = {}
        dir = dir[d]
    return dir

for l in F:
    l = l.split()
    if l[0] == "$":
        if l[1] == "cd":
            if l[2] == "/": cd.clear()
            elif l[2] == "..": cd.pop()
            else: cd.append(l[2])
    else:
        sz, n = l
        dir = gd()
        if sz == "dir":
            dir[n] = {}
        else:
            dir[n] = int(sz)

S = 0
T = 0
sizes = {}
def walk(path, dir):
    global S, T
    s = 0
    for k, v in dir.items():
        if type(v) == int:
            s += v
            T += v
        else:
            s += walk(path + "/" + k, v)
    if s <= 100000: S += s
    sizes[path] = s
    return s
walk("/", fs)
print(S)

M = math.inf
for v in sizes.values():
    if 70000000 - T + v >= 30000000:
        if v < M: M = v
print(M)
