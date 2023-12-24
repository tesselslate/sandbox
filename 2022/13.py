import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
F = ul.double_linefeed(F)
F = [(eval(l[0]), eval(l[1])) for l in F]

# 1 good, 0 continue, -1 bad
def cmp(a, b):
    if type(a) == int and type(b) == int:
        if a < b: return 1
        if a == b: return 0
        if a > b: return -1
    elif type(a) == list and type(b) == list:
        for a, b in itertools.zip_longest(a, b):
            if a == None: return 1
            if b == None: return -1
            r = cmp(a, b)
            if r == 0: continue
            else: return r
        return 0
    else:
        if type(a) == int: a = [a]
        if type(b) == int: b = [b]
        return cmp(a, b)

print(sum(i + 1 for (i, l) in enumerate(F) if cmp(*l) == 1))

F = [x for xs in F for x in xs]
F.append([[2]])
F.append([[6]])
F = list(reversed(sorted(F, key=functools.cmp_to_key(cmp))))

F.insert(0, None) # skip +1
print(F.index([[2]])*F.index([[6]]))
