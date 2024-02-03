import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]
F = [int(l) for l in F[0].split(',')]

i = 0
while i < len(F):
    n = F[i]
    mode = (0, 0, 0)

    def get(x):
        if mode[x-1]:
            return F[x+i]
        else:
            return F[F[x+i]]

    if n > 100:
        n = str(n)
        n = n.zfill(5)
        mode = (n[2] == "1", n[1] == "1", n[0] == "1")
        n = int(n) % 100
    else:
        mode = (0, 0, 0)

    if n == 1:
        F[F[i+3]] = get(1) + get(2)
        i += 4
    elif n == 2:
        F[F[i+3]] = get(1) * get(2)
        i += 4
    elif n == 3:
        F[F[i+1]] = int(input())
        i += 2
    elif n == 4:
        print(get(1))
        i += 2
    elif n == 5:
        if get(1) != 0:
            i = get(2)
        else:
            i += 3
    elif n == 6:
        if get(1) == 0:
            i = get(2)
        else:
            i += 3
    elif n == 7:
        F[F[i+3]] = 1 if get(1) < get(2) else 0
        i += 4
    elif n == 8:
        F[F[i+3]] = 1 if get(1) == get(2) else 0
        i += 4
    elif n == 99:
        break
    else:
        assert False, n
