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
trygates = {'bvc', 'qfg', 'dkr', 'fdd', 'gcs', 'hdc', 'dhf', 'hrr',  'nsg', 'kkt', 'thc', 'rrr', 'tkd', 'shd', 'qhg', 'jgj', 'mts', 'ntr', 'wwc', 'hch', 'wsg', 'pnw', 'y00'}
print(len(trygates))
print(trywith(_gates))
for a, b, c, d, e, f, g, h in itertools.combinations(trygates, 8):
    newgates = _gates.copy()

    flips = []
    ng2 = set()
    for gate in newgates:
        if gate[4] in {a,b,c,d,e,f,g,h}:
            flips.append(gate)
        else: ng2.add(gate)

    if len(flips) < 8: continue
    a, b, c, d, e, f, g, h = flips

    ng2.add((a[0], a[1], a[2], a[3], b[0]))
    ng2.add((b[0], b[1], b[2], b[3], a[0]))
    ng2.add((c[0], c[1], c[2], c[3], d[0]))
    ng2.add((d[0], d[1], d[2], d[3], c[0]))
    ng2.add((e[0], e[1], e[2], e[3], f[0]))
    ng2.add((f[0], f[1], f[2], f[3], e[0]))
    ng2.add((g[0], g[1], g[2], g[3], h[0]))
    ng2.add((h[0], h[1], h[2], h[3], g[0]))

    x = trywith(ng2)
    if x is not None: print(expect ^ x)
    if expect == x:
        print(a,b,c,d,e,f,g,h)

    # del newgates[a]
    # del newgates[b]
    # del newgates[c]
    # del newgates[d]
    # del newgates[e]
    # del newgates[f]
    # del newgates[g]
    # del newgates[h]
    # newgates.remove(a)
    # newgates.remove(b)
    # newgates.remove(c)
    # newgates.remove(d)
    # newgates.remove(e)
    # newgates.remove(f)
    # newgates.remove(g)
    # newgates.remove(h)
    # newgates.add((a[0], a[1], a[2], a[3], b[0]))
    # newgates.add((b[0], b[1], b[2], b[3], a[0]))
    # newgates.add((c[0], c[1], c[2], c[3], d[0]))
    # newgates.add((d[0], d[1], d[2], d[3], c[0]))
    # newgates.add((e[0], e[1], e[2], e[3], f[0]))
    # newgates.add((f[0], f[1], f[2], f[3], e[0]))
    # newgates.add((g[0], g[1], g[2], g[3], h[0]))
    # newgates.add((h[0], h[1], h[2], h[3], g[0]))
    #
    # if expect == trywith(newgates):
    #     print(a,b,c,d,e,f,g,h)
