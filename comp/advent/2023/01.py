import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

S = 0
for l in F:
    digits = [int(c) for c in l if c.isdigit()]
    S += (digits[0] * 10) + digits[-1]
print(S)

S = 0
for l in F:
    digits = []
    for i in range(len(l)):
        if l[i].isdigit():
            digits.append(int(l[i]))
        else:
            for (j, word) in enumerate(words):
                if l[i:].startswith(word):
                    digits.append(j + 1)
    S += (digits[0] * 10) + digits[-1]
print(S)
