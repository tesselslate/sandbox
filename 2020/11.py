import functools, math, re, string, sys, itertools, ul
import copy
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

if len(sys.argv) > 1:
    F = open(sys.argv[1])
else:
    F = sys.stdin.readlines()
    if not F[-1].strip():
        del F[-1]

F = [l.strip() for l in F]
G = ul.grid(F)

S = 0

def adj(r, c):
    pos = [(r-1,c),(r+1,c),(r,c-1),(r,c+1),(r-1,c-1),(r-1,c+1),(r+1,c-1),(r+1,c+1)]
    a = []
    for p in pos:
        if p[0] >= 0 and p[0] < len(G):
            if p[1] >= 0 and p[1] < len(G[0]):
                a.append(G[p[0]][p[1]])
    return a

def r():
    global G
    change = False
    overlay = []
    for r in range(len(G)):
        for c in range(len(G[0])):
            x = G[r][c]
            match x:
                case "L":
                    if adj(r, c).count("#") == 0:
                        overlay.append((r,c,"#"))
                        change = True
                case "#":
                    xs = adj(r, c)
                    if xs.count("#") >= 4:
                        overlay.append((r,c,"L"))
                        change = True
    for x in overlay:
        G[x[0]][x[1]] = x[2]
    return change

i = 0
while r():
    i += 1

for r in range(len(G)):
    for c in range(len(G[0])):
        if G[r][c] == "#": S += 1
print(S)

G = ul.grid(F)
S = 0
def adj(r, c):
    pos = [(-1,0),(1,0),(0,1),(0,-1),(-1,-1),(-1,1),(1,-1),(1,1)]
    a = []
    x, y = r, c
    for p in pos:
        r, c = x, y
        r += p[0]
        c += p[1]
        while r >= 0 and r < len(G) and c >= 0 and c < len(G[0]) and G[r][c] == ".":
            r += p[0]
            c += p[1]
        if r < 0: a.append(".")
        elif r >= len(G): a.append(".")
        elif c < 0: a.append(".")
        elif c >= len(G[0]): a.append(".")
        else:
            a.append(G[r][c])
    return a

def r():
    global G
    change = False
    overlay = []
    for r in range(len(G)):
        for c in range(len(G[0])):
            x = G[r][c]
            match x:
                case "L":
                    if adj(r, c).count("#") == 0:
                        overlay.append((r,c,"#"))
                        change = True
                case "#":
                    xs = adj(r, c)
                    if xs.count("#") >= 5:
                        overlay.append((r,c,"L"))
                        change = True
    for x in overlay:
        G[x[0]][x[1]] = x[2]
    return change

i = 0
while r():
    i += 1

for r in range(len(G)):
    for c in range(len(G[0])):
        if G[r][c] == "#": S += 1
print(S)
