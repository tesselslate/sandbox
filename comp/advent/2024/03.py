import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = "\n".join(ul.input())

S = 0
S2 = 0

do = True

for i in range(len(F)):
    if F[i:].startswith("do()"): do = True
    if F[i:].startswith("don't()"): do = False

    if not F[i:].startswith("mul("): # )
        continue

    try:
        a, b = F[i+4:F.index(")", i)].split(",")
        p = int(a) * int(b)

        S += p
        if do: S2 += p
    except:
        continue

print(S)
print(S2)
