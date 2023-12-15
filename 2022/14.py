import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
W = set()

for l in F:
    xs = l.split(" -> ")
    for (a,b) in itertools.pairwise(xs):
        x1, y1 = ul.scan("%d,%d", a.strip())
        x2, y2 = ul.scan("%d,%d", b.strip())
        x1, x2 = ul.minmax(x1, x2)
        y1, y2 = ul.minmax(y1, y2)

        it = zip(itertools.repeat(x1), range(y1, y2+1)) if x1 == x2 else zip(range(x1, x2+1), itertools.repeat(y1))
        for (x,y) in it: W.add((x,y))
floor = max(y for (x,y) in W) + 2

def sim(has_floor):
    S = set()
    def occupied(p):
        return p in S or p in W or (has_floor and p[1] == floor)

    while (500,0) not in S:
        s = (500,0)
        while True:
            spots = [(s[0],s[1]+1),(s[0]-1,s[1]+1),(s[0]+1,s[1]+1)]
            for spot in spots:
                if not occupied(spot):
                    s = spot
                    break
            else:
                break
            if s[1] >= floor: break
        if s[1] < floor: S.add(s)
        else: break
    return len(S)

print(sim(False))
print(sim(True))
