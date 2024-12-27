import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()[0]

costs = {
    "B": 1,
    "C": 3,
}

print(sum(costs[x] for x in F if x in costs))
