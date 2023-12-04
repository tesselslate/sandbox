import functools, math, re, string, sys, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

if len(sys.argv) > 1:
    F = open(sys.argv[1])
else:
    F = sys.stdin.readlines()

F = [l.strip() for l in F]
while F[-1] == "":
    del F[-1]

S = 0

i = 0

winning = defaultdict(bool)
count = defaultdict(int)
for l in F:
    n, b = ul.scan("Card %d: %s", l)
    a, b = b.split("|")
    winning_ = []
    sum = 0
    for x in a.strip().split():
        winning_.append(int(x))
    won = False
    for x in b.strip().split():
        if int(x) in winning_:
            # if sum == 0:
            #     sum = 1
            # else:
            #     sum *= 2
            sum += 1
            won = True
    if won:
        winning[n] = True
        count[n] = sum
    if won:
        assert sum > 0
        S += 2 ** (sum-1)
print(S)

# S = 0
# @functools.cache
# def re(x):
#     v = 0
#     if count[x]: v += count[x]
#     for i in range(count[x]):
#         v += re(i+x+1)
#     print(x,v)
#     return v
# for k, v in winning.items():
#     S += re(k)
# print(S)

S = 0
V = defaultdict(int)
def win(card):
    V[card] += 1
    v = count[card]
    for i in range(count[card]):
        v += win(i+card+1)
    return v
for k in winning.keys():
    win(k)

for x in V.values():
    S += x
print(S)
