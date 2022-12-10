import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]

X = 1
C = 0
S = 0
G = util.grid(40, ".")

def update():
    global G, S
    if (C - 20) % 40 == 0:
        S += X*C
    for i in range(-1, 2):
        cx = (C-1) % 40
        if cx == X+i:
            G[C//40][cx] = "#"

for l in F:
    w = l.split(" ")
    if w[0] == "noop":
        C += 1
        update()
    else:
        C += 1
        update()
        C += 1
        update()
        X += int(w[1])
util.print_grid(G)
print(S)
