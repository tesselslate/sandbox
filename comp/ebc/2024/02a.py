import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

target = F[0].split(":")[1].split(",")
words = F[2]

S = 0
for i in range(len(words)):
    for word in target:
        if words[i:].startswith(word): S += 1

print(S)
