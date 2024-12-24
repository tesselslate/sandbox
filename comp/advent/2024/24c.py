import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.double_linefeed(ul.input())
S = 0

z = set()
xx = set()
y = set()
_bits = {}
for l in F[0]:
    x = l.split()
    _bits[x[0].replace(":", "")] = bool(int(x[1]))
    name = x[0].replace(":", "")
    if name.startswith("x"): xx.add(name)
    if name.startswith("y"): y.add(name)

_gates = []
src = []

x = xx

for l in F[1]:
    _gates.append([*l.split()])

    a = l.split()
    if a[4].startswith("z"): z.add(a[4])

def trywith(gates):
    bits = _bits.copy()

    def caneval(gate):
        return gate[0] in bits and gate[2] in bits

    def eval(gate):
        if gate[1] == "AND":
            return bits[gate[0]] and bits[gate[2]]
        elif gate[1] == "XOR":
            return bool(bits[gate[0]]) != bool(bits[gate[2]])
        elif gate[1] == "OR":
            return bits[gate[0]] or bits[gate[2]]
        assert False

    for i in range(224):
        for gate in gates:
            if gate[0] in bits and gate[2] in bits:
                if gate[4] in bits: x = bits[gate[4]]
                bits[gate[4]] = eval(gate)

        z = []
        for i in range(46):
            name = "z" + format(i, "#02")
            if name not in bits: break
            z.append(bits[name])
        else:
            n = 0
            for bit in reversed(z):
                n = n * 2 + (1 if bit else 0)
            return n
    return None

nx = 0
ny = 0
for i in reversed(range(45)):
    nx = nx * 2 + (1 if _bits["x" + format(i, "#02")] else 0)
for i in reversed(range(45)):
    ny = ny * 2 + (1 if _bits["y" + format(i, "#02")] else 0)

print(nx,ny)
expect = nx+ny

_gates = set(tuple(x) for x in _gates)
val = trywith(_gates)
print(val, expect, val-expect, val^expect)

# for i in range(46):
#     if (val & (1 << i)) != (expect & (1 << i)):
#         print(i+1)

flips = [6,7,8,9,16,17,18,21,22,23]

flow = defaultdict(set)
for gate in _gates:
    flow[gate[4]].add(gate[0])
    flow[gate[4]].add(gate[2])

def affected_by(id):
    Q = deque([id])
    V = set()

    while len(Q):
        x = Q.popleft()
        for y in flow[x]:
            if y in V: continue
            V.add(y)
            Q.append(y)
    return V

flipnames = ["z" + format(i, "#02") for i in flips]
flips = []
for flipname in flipnames:
    xs = affected_by(flipname)
    print(len(xs))
    flips.append(xs)

allflips = flips[0].intersection(flips[1]).intersection(flips[2]).intersection(flips[3]).intersection(flips[4]).intersection(flips[5]).intersection(flips[6]).intersection(flips[7])
print(allflips)
