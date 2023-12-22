import ul
from collections import deque

F = ul.input()
G = ul.grid(F)

sr, sc = 0, 0
for (r,c) in ul.gridpoints(G):
    if G[r][c] == "S": sr, sc = r, c; break

V = {(sr,sc): 0}
Q = deque([(sr,sc,0)])
while len(Q):
    (r,c,d) = Q.popleft()
    for rr, cc in ul.padj4():
        rr, cc = rr+r, cc+c
        if not ul.gridcheck(G,rr,cc) or G[rr][cc] == "#": continue
        if (rr,cc) in V: continue
        V[rr,cc] = d+1
        Q.append((rr,cc,d+1))

print(len([(r,c) for (r,c), d in V.items() if d % 2 == 0 and d <= 64]))

N = 26501365 // 131
assert N == 202300

# https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21
# My initial solution figured out a similar trick except I had 14 different numbers instead
# of 4. This is much nicer.

odd             = len([(r,c) for (r,c), d in V.items() if d % 2 == 1])
even            = len([(r,c) for (r,c), d in V.items() if d % 2 == 0])
odd_corners     = len([(r,c) for (r,c), d in V.items() if d % 2 == 1 and d > 65])
even_corners    = len([(r,c) for (r,c), d in V.items() if d % 2 == 0 and d > 65])

odd *= (N+1) ** 2
even *= N ** 2

odd_corners *= (N+1)
even_corners *= N

print(odd + even - odd_corners + even_corners)
