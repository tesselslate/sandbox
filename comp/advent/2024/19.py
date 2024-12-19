import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.double_linefeed(ul.input())

towels = F[0][0].replace(",", "").split()
patterns = F[1]

@functools.cache
def dfs(pattern):
    if pattern == "": return 1

    return sum(dfs(pattern[len(towel):]) for towel in towels if pattern.startswith(towel))

print(sum(dfs(pattern) > 0 for pattern in patterns))
print(sum(dfs(pattern) for pattern in patterns))
