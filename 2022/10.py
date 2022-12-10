import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]
F.append("noop")

X = 1
C = 1
S = 0

G = util.grid(40, 0)

ip = 0
addx = None
while ip < len(F) or addx != None:
    if (C - 20) % 40 == 0:
        S += X*C

    # crt draw
    b = False
    for i in range(-1, 2):
        cx = (C-1) % 40
        if cx == X+i:
            b = True
            G[C//40][cx] = 1

    if addx != None:
        X += addx
        addx = None
        C += 1
        continue

    C += 1

    w = F[ip].split(" ")
    ip += 1
    if w[0] == "noop":
        continue
    if w[0] == "addx":
        addx = int(w[1])
        continue
print(S)
for y in G[:6]:
    s = ""
    for x in y:
        s += "#" if x else "."
    print(s)
