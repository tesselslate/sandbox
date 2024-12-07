import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

def possible(l, ops):
    t, *xs = ul.ints(l)

    for ops in itertools.product(ops, repeat=len(xs)-1):
        x = xs[0]
        for i, op in enumerate(ops):
            if op == "+":
                x += xs[i + 1]
            elif op == "*":
                x *= xs[i + 1]
            else:
                x = int(str(x) + str(xs[i+1]))
        if x == t:
            return t
    return 0

print(sum(possible(l, ["+", "*"]) for l in F))
print(sum(possible(l, ["+", "*", "||"]) for l in F))
