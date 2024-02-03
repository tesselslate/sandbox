import math, ul
from collections import defaultdict

F = ul.input()

S, S2 = 0, 0
for l in F:
    n, g = ul.scan("Game %d: %s", l)
    pos = True
    cubes = defaultdict(int)
    for nc, nt in ul.batched(g.replace(',','').replace(';','').strip().split(), 2):
        match (int(nc), nt):
            case (nc, "red") if nc > 12: pos = False
            case (nc, "green") if nc > 13: pos = False
            case (nc, "blue") if nc > 14: pos = False
        cubes[nt] = max(cubes[nt], nc)
    if pos: S += n
    S2 += math.prod(cubes.values())
print(S)
print(S2)
