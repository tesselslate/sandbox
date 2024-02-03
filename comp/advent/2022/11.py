import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
F = ul.double_linefeed(F)

# new = old XYZ

def parse(x):
    x = [l.strip() for l in x[1:]]
    items = [int(n) for n in x[0].replace(',','').split() if n.isdigit()]
    op, = ul.scan("Operation: new = %s", x[1])
    op_lambda = eval(f"lambda old: {op}")
    div, = ul.scan("Test: divisible by %d", x[2])
    true, = ul.scan("If true: throw to monkey %d", x[3])
    false, = ul.scan("If false: throw to monkey %d", x[4])
    return (items,op_lambda,div,true,false)

M = [parse(x) for x in F]
I = [0 for _ in M]
lcm = math.lcm(*[m[2] for m in M])

def turn(div):
    for (i, m) in enumerate(M):
        I[i] += len(m[0])
        for w in m[0]:
            n = m[1](w)
            if div: n //= 3
            else: n %= lcm
            if n % m[2] == 0:
                M[m[3]][0].append(n)
            else:
                M[m[4]][0].append(n)
        m[0].clear()

for _ in range(20): turn(True)
I.sort()
print(math.prod(I[-2:]))

M = [parse(x) for x in F]
I = [0 for _ in M]

for _ in range(10000): turn(False)
I.sort()
print(math.prod(I[-2:]))
