from functools import lru_cache
import util

F = 7689
S = 0

def power(x, y):
    rack_id = x + 10
    a = rack_id * y
    a += F
    a *= rack_id
    b = str(a)
    if len(b) < 3:
        return 0
    return int(b[-3]) - 5

g = util.grid(301, 0)
for i in util.irange(1, 300):
    for j in util.irange(1, 300):
        g[i][j] = power(i,j)

M = 0
mx, my = 0, 0
for i in util.irange(1, 298):
    for j in util.irange(1, 298):
        S = 0
        for a in range(3):
            for b in range(3):
                S += g[i+a][j+b]
        if S > M:
            M = S
            mx, my = i, j
print(mx, my)

@lru_cache(4000000)
def area_power(x, y, s):
    if s == 1:
        return g[x][y]
    res = 0
    for i in range(y, y+s):
        res += g[x+s-1][i]
    for i in range(x, x+s):
        res += g[i][y+s-1]
    return res + area_power(x, y, s-1)

M = 0
mx, my, si = 0, 0, 0
for s in util.irange(1, 300):
    for i in util.irange(1, 300-s+1):
        for j in util.irange(1, 300-s+1):
            S = area_power(i, j, s)
            if S > M:
                M = S
                mx, my, si = i, j, s
print(mx, my, si)
