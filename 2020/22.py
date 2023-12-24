import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
F = ul.double_linefeed(F)

def f(x):
    return [int(y) for y in x[1:]]

a = deque(f(F[0]))
b = deque(f(F[1]))

while len(a) and len(b):
    x, y = a.popleft(), b.popleft()
    if x > y: a.extend([x,y])
    else: b.extend([y,x])
x = a or b
print(sum(i*y for i, y in enumerate(reversed(x), 1)))

a = deque(f(F[0]))
b = deque(f(F[1]))

def STR(a,b): return ",".join(map(str, a)) + ";" + ",".join(map(str, b))
def sim(a,b):
    dp = set()
    while len(a) and len(b):
        x = STR(a,b)
        if x in dp: return 1
        dp |= {x}

        x, y = a.popleft(), b.popleft()
        if len(a) >= x and len(b) >= y:
            winner = sim(deque(list(a)[:x]),deque(list(b)[:y]))
            if winner == 1: a.extend([x,y])
            else: b.extend([y,x])
        else:
            if x > y: a.extend([x,y])
            else: b.extend([y,x])
    assert bool(len(a)) != bool(len(b))
    return 1 if len(a) else 2
while len(a) and len(b):
    sim(a,b)
x = a or b
print(sum(i*y for i, y in enumerate(reversed(x), 1)))
