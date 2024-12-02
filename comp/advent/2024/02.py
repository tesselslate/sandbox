import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

def safe(xs):
    diff = all(1 <= abs(x - y) <= 3 for (x, y) in itertools.pairwise(xs))
    inc = all(x < y for (x, y) in itertools.pairwise(xs))
    dec = all(x > y for (x, y) in itertools.pairwise(xs))

    return diff and (inc or dec)

def safe2(xs):
    if safe(xs): return True

    for i in range(len(xs)):
        if safe([xs[j] for j in range(len(xs)) if i != j]):
            return True

    return False

print(sum(1 for l in F if safe(ul.ints(l))))
print(sum(1 for l in F if safe2(ul.ints(l))))
