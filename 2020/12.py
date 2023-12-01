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

# NESW
dirs = [(0,-1),(1,0),(0,1),(-1,0)]
dir = dirs[1] # EAST
d = "NESW"

x, y = 0, 0
for l in F:
    a, b = l[0], int(l[1:])
    match a:
        case "N":
            x += dirs[d.index(a)][0] * b
            y += dirs[d.index(a)][1] * b
        case "S":
            x += dirs[d.index(a)][0] * b
            y += dirs[d.index(a)][1] * b
        case "E":
            x += dirs[d.index(a)][0] * b
            y += dirs[d.index(a)][1] * b
        case "W":
            x += dirs[d.index(a)][0] * b
            y += dirs[d.index(a)][1] * b
        case "L":
            n = b // 90
            i = dirs.index(dir)
            i = (i - n) % 4
            dir = dirs[i]
        case "R":
            n = b // 90
            i = dirs.index(dir)
            i = (i + n) % 4
            dir = dirs[i]
        case "F":
            x += dir[0] * b
            y += dir[1] * b

print(abs(x)+abs(y))

# NESW
dirs = [(0,-1),(1,0),(0,1),(-1,0)]
dir = dirs[1] # EAST
d = "NESW"

x, y = 0, 0
wx, wy = 10, -1
for l in F:
    a, b = l[0], int(l[1:])
    match a:
        case "N":
            wx += dirs[d.index(a)][0] * b
            wy+= dirs[d.index(a)][1] * b
        case "S":
            wx += dirs[d.index(a)][0] * b
            wy+= dirs[d.index(a)][1] * b
        case "E":
            wx += dirs[d.index(a)][0] * b
            wy+= dirs[d.index(a)][1] * b
        case "W":
            wx += dirs[d.index(a)][0] * b
            wy+= dirs[d.index(a)][1] * b
        case "L":
            n = b // 90
            for i in range(n):
                nx = wy
                ny = -wx
                wx = nx
                wy = ny
        case "R":
            n = b // 90
            for i in range(n):
                nx = -wy
                ny = wx
                wx = nx
                wy = ny
        case "F":
            x += (wx) * b
            y += (wy) * b

print(abs(x)+abs(y))
