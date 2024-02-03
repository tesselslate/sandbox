import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque
from copy import deepcopy

F = ul.input()
F = ul.double_linefeed(F)

N = 9
stacks = [[] for _ in range(N)]

for r in range(len(F[0])-1):
    for c in range(N):
        x = c * 4 + 1
        if x < len(F[0][r]):
            ch = F[0][r][x]
            if ch != " ": stacks[c].insert(0, ch)

stacks2 = deepcopy(stacks)

for l in F[1]:
    a, b, c = ul.scan("move %d from %d to %d", l)
    Q = deque()
    Q2 = deque()
    for _ in range(a):
        Q.append(stacks[b-1].pop())
        Q2.append(stacks2[b-1].pop())
    while len(Q):
        stacks[c-1].append(Q.popleft())
        stacks2[c-1].append(Q2.pop())
print("".join([stack[-1] for stack in stacks]))
print("".join([stack[-1] for stack in stacks2]))
