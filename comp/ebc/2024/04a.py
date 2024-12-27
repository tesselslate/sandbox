import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
F = [int(l) for l in F]

m = min(F)
print(sum(x-m for x in F))
