import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()[0]

costs = {
    "A": 0,
    "B": 1,
    "C": 3,
    "D": 5,
}

S = 0
for xs in ul.batched(F, 2):
    S += sum(costs[x] for x in xs if x in costs)
    if "x" not in xs:
        S += 2
print(S)
