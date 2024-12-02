import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

cards = defaultdict(int)
matches = defaultdict(int)

S = 0
for i, l in enumerate(F):
    a, b = l.split(":")[1].split("|")
    win, scratch = ul.ints(a), ul.ints(b)

    wins = sum(1 for x in scratch if x in win)
    if wins > 0:
        S += int(math.pow(2, wins - 1))
        matches[i] = wins

        for j in range(i+1, i+1+matches[i]):
            cards[j] += 1
print(S)

for i in range(len(F)):
    for j in range(i+1, i+1+matches[i]):
        cards[j] += cards[i]

print(sum(cards.values()) + len(F))
