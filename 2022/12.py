import collections, util
from sys import argv

F = [l.strip() for l in open(argv[1])]

R = len(F)
C = len(F[0])

S, D = (0,0), (0,0)

for r, x in enumerate(F):
    for c, y in enumerate(x):
        if y == 'S':
            S = (r,c)
        elif y == 'E':
            D = (r,c)

def elevation(p):
    global F
    c = F[p[0]][p[1]]
    if c == 'S':
        return 0
    elif c == 'E':
        return 25
    else:
        return ord(c) - ord('a')

def adj(p):
    return [
        (p[0] + 1, p[1]),
        (p[0] - 1, p[1]),
        (p[0], p[1] + 1),
        (p[0], p[1] - 1),
    ]

Q = collections.deque()
Q.append((S,0))
FF = util.grid2d(R, C, -1)

def pathfind(S, D):
    global Q, FF
    Q = collections.deque()
    Q.append((S,0))
    FF = util.grid2d(R, C, -1)

    def add(cur, next, val):
        global Q, FF
        if next[0] < 0 or next[0] >= R or next[1] < 0 or next[1] >= C:
            return
        cur_el = elevation(cur)
        next_el = elevation(next)
        if next_el - cur_el > 1:
            return
        if FF[next[0]][next[1]] > -1:
            return
        Q.append((next, val))
        FF[next[0]][next[1]] = val

    Q.append((S,0))
    while len(Q) > 0:
        E = Q.popleft()
        for point in adj(E[0]):
            add(E[0], point, E[1] + 1)
    return FF[D[0]][D[1]]

print(pathfind(S,D))

M = 1000000
for r, x in enumerate(F):
    for c, y in enumerate(x):
        if y == 'a':
            v = pathfind((r,c),D)
            if v > 0:
                M = min(M, v)
print(M)
