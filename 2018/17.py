import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]
S = 0

C = set()

for l in F:
    a, b = l.replace(",", "").split(" ")
    rc = b[0]
    x1, x2, y1, y2 = 0, 0, 0, 0
    if rc == 'x':
        y = int(a[2:])
        y1, y2 = y, y
        x1, x2 = util.scan("x=%d..%d", b)
    else:
        x = int(a[2:])
        x1, x2 = x, x
        y1, y2 = util.scan("y=%d..%d", b)

    for x in util.irange(x1, x2):
        for y in util.irange(y1, y2):
            C.add((x, y))

MIN_X = min(C, key=lambda x : x[0])[0]
MAX_X = max(C, key=lambda x : x[0])[0]
MIN_Y = min(C, key=lambda x : x[1])[1]
MAX_Y = max(C, key=lambda x : x[1])[1]
SIZE = max(MAX_X - MIN_X, MAX_Y - MIN_Y) + 3
G = util.grid(SIZE, '.')

for c in C:
    G[c[0]-MIN_X+1][c[1]-MIN_Y+1] = '#'

def print_grid(grid):
    for y in range(len(grid)):
        s = ""
        for x in range(len(grid)):
            s += grid[x][y]
        print(s)

R = set()
R.add((500-MIN_X+1, 1))

pointless_ticks = 0
while pointless_ticks < 100:
    l = len(R)

    G[500-MIN_X+1][1] = '|'

    for x in range(SIZE):
        for y in range(SIZE):
            if G[x][y] != '|' or y == SIZE - 2:
                continue

            if G[x][y+1] == '.':
                G[x][y] = '.'
                R.add((x, y+1))
                G[x][y+1] = '|'
            elif G[x][y+1] != '|':
                lb, rb = 0, SIZE - 2
                ld, rd = False, False
                for i in range(x, 0, -1):
                    if G[i][y+1] == '.':
                        lb, ld = i, True
                        break
                    if G[i][y] == '#':
                        lb = i
                        break
                for i in range(x, SIZE - 1):
                    if G[i][y+1] == '.':
                        rb, rd = i, True
                        break
                    if G[i][y] == '#':
                        rb = i
                        break
                lb = lb if ld else lb + 1
                rb = rb if rd else rb - 1
                for j in util.irange(lb, rb):
                    R.add((j,y))
                    G[j][y] = '|' if ld or rd else '~'

    if l == len(R):
        pointless_ticks += 1
print(len(R))
