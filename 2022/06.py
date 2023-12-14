import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()[0]

S = 0
S2 = 0
for i in range(4, len(F)):
    if not S and len(set(F[i-4:i])) == 4:
        S = i
    if not S2 and i >= 14 and len(set(F[i-14:i])) == 14:
        S2 = i
print(S)
print(S2)
