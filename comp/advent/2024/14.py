import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

W = 101
H = 103

robots = []
for l in F:
    x, y, vx, vy = ul.ints(l)
    robots.append((x, y, vx, vy))

def sim(robots):
    n = []
    for r in robots:
        x, y, vx, vy = r
        n.append(((x + vx) % W, (y + vy) % H, vx, vy))
    return n

for _ in range(100):
    robots = sim(robots)

quads = [0] * 4
for r in robots:
    x, y, *_ = r
    if x == W // 2 or y == H // 2: continue

    xp, yp = x < W // 2, y < H // 2
    quads[int(xp) * 2 + int(yp)] += 1
print(math.prod(quads))

robots = []
for l in F:
    x, y, vx, vy = ul.ints(l)
    robots.append((x, y, vx, vy))

for i in range(1, 10**10):
    robots = sim(robots)
    if len({(x,y) for x, y, *_ in robots}) == len(robots):
        print(i)
        break
