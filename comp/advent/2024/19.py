import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.double_linefeed(ul.input())
S = 0

towels = F[0][0].replace(",", "").split()
patterns = F[1]
print(towels)

@functools.cache
def dfs(pattern):
    if pattern == "": return 1
    s = 0
    for towel in towels:
        if pattern.startswith(towel):
            s += dfs(pattern[len(towel):])
    return s

for pattern in patterns:
    S += dfs(pattern)

print(S)
