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

def s1(a, b):
    cards = "23456789TJQKA"
    counter = Counter()
    c2 = []
    for c in a:
        counter[c] += 1
        c2.append(cards.index(c))
    c2 = tuple(c2)
    v = list(counter.values())
    v.sort()
    if v == [5]:
        return 10000, c2
    elif v == [1, 4]:
        return 5000, c2
    elif v == [2, 3]:
        return 3000, c2
    elif v == [1, 1, 3]:
        return 2000, c2
    elif v == [1,2,2]:
        return 1000, c2
    elif v == [1,1,1,2]:
        return 500, c2
    elif len(v) == 5:
        return 100, c2
    else:
        print(v, a, counter)
        assert False

def s2(a, b):
    cards = "J23456789TQKA"
    counter = Counter()
    c2 = []
    for c in a:
        counter[c] += 1
        c2.append(cards.index(c))
    nj = counter["J"]
    c2 = tuple(c2)

    max = 0
    card = a
    for rep in cards[1:]:
        def x():
            a = card
            a = a.replace("J", rep)

            counter = Counter()
            for c in a:
                counter[c] += 1

            v = list(counter.values())
            v.sort()
            if v == [5]:
                return 10000
            elif v == [1, 4]:
                return 5000
            elif v == [2, 3]:
                return 3000
            elif v == [1, 1, 3]:
                return 2000
            elif v == [1,2,2]:
                return 1000
            elif v == [1,1,1,2]:
                return 500
            elif len(v) == 5:
                return 100
            else:
                print(v, a, counter)
                assert False
        v = x()
        if v > max:
            max = v
    return max, c2

S = []
for l in F:
    a, b = ul.scan("%s %d", l)
    S.append((a,b))
S.sort(key=lambda t: s1(t[0], t[1]))
S.reverse()
SUM = 0
for i, x in enumerate(reversed(S)):
    SUM += x[1] * (i + 1)
print(SUM)

S = []
for l in F:
    a, b = ul.scan("%s %d", l)
    S.append((a,b))
S.sort(key=lambda t: s2(t[0], t[1]))
S.reverse()
SUM = 0
for i, x in enumerate(reversed(S)):
    SUM += x[1] * (i + 1)
print(SUM)
