import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()[0]

Q = deque([int(x) for x in F])
cur = Q[0]

def turn(cur, Q):
    x = Q.index(cur)
    Q.rotate(-x)
    assert Q[0] == cur

    Q.rotate(-1)
    a, b, c = Q.popleft(), Q.popleft(), Q.popleft()

    d = cur-1
    if d < 1: d = len(Q)+3
    while d in set([a,b,c]):
        d -= 1
        if d < 1: d = len(Q)+3

    n = Q.index(d)
    Q.rotate(-n)
    assert Q[0] == d

    Q.rotate(-1)
    Q.extendleft([c,b,a])
    Q.rotate(2)

    cur = Q[(Q.index(cur)+1)%len(Q)]
    Q.rotate(x)

    return cur, Q

for _ in range(100):
    cur, Q = turn(cur, Q)

while Q[-1] != 1: Q.rotate(1)
Q.pop()
print("".join(map(str,Q)))
