import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.double_linefeed(ul.input())

bits = {}
gates = {}

for l in F[0]:
    name, value, *_ = l.split()
    bits[name[:-1]] = int(value)

for l in F[1]:
    a, op, b, _, dst, *_ = l.split()
    gates[dst] = (a, op, b)

@functools.cache
def evaluate(dst):
    if dst in bits:
        return bits[dst]

    gate = gates[dst]
    a, b = evaluate(gate[0]), evaluate(gate[2])
    match gate[1]:
        case "AND": return a & b
        case "XOR": return a ^ b
        case "OR":  return a | b

zbits = [evaluate(f"z{i:#02}") for i in reversed(range(46))]
print(int("".join(str(z) for z in zbits), base=2))
