import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

from z3 import *

inp = ul.input()
F = ul.double_linefeed(inp)
S = 0

xs = {}
ys = {}
for l in F[0]:
    ll = l.split()
    if l.startswith('x'): xs[ll[0][:-1]] = bool(int(ll[1]))
    if l.startswith('y'): ys[ll[0][:-1]] = bool(int(ll[1]))

startx = 0
starty = 0

for i in reversed(range(45)):
    startx = startx * 2 + (1 if xs["x" + format(i, "#02")] else 0)
    starty = starty * 2 + (1 if ys["y" + format(i, "#02")] else 0)

target = startx + starty
print(target)

target_bits = []
for i in range(48):
    target_bits.append(1 if (target & (1 << i)) != 0 else 0)

norm_bits = []
for i in range(48):
    norm_bits.append(1 if (53755311654662 & (1 << i)) != 0 else 0)

print(target_bits)
print(norm_bits)
print(sum(target_bits[i] != norm_bits[i] for i in range(len(target_bits))))

for i in range(48):
    if target_bits[i] != norm_bits[i]: print(i, target_bits[i], norm_bits[i])

gates = set()
gatenames = set()
for l in F[1]:
    ll = l.split()
    gates.add((ll[0], ll[1], ll[2], ll[3], ll[4]))
    gatenames.add(ll[0])
    gatenames.add(ll[2])
    gatenames.add(ll[4])

bits = {}
for l in F[0]:
    ll = l.split()
    bits[ll[0][:-1]] = bool(int(ll[1]))

def trywith(G, B):
    def caneval(gate):
        return gate[0] in B and gate[2] in B

    def eval(gate):
        if gate[1] == "AND":
            return B[gate[0]] and B[gate[2]]
        elif gate[1] == "XOR":
            return bool(B[gate[0]]) != bool(B[gate[2]])
        elif gate[1] == "OR":
            return B[gate[0]] or B[gate[2]]
        assert False

    for i in range(1000):
        for gate in G:
            if gate[0] in B and gate[2] in B:
                if gate[4] in B: x = B[gate[4]]
                B[gate[4]] = eval(gate)

        z = []
        for i in range(46):
            name = "z" + format(i, "#02")
            if name not in B: break
            z.append(B[name])
        else:
            n = 0
            for bit in reversed(z):
                n = n * 2 + (1 if bit else 0)
            return n
    return None

def flip(a,b,c=None,d=None,e=None,f=None,g=None,h=None):
    ng = set()
    k=0
    for gate in gates:
        if gate[4] in {a,b,c,d,e,f,g,h}:
            if gate[4] == a: ng.add((gate[0],gate[1],gate[2],gate[3],b)); k += 1
            if gate[4] == b: ng.add((gate[0],gate[1],gate[2],gate[3],a)); k += 1
            if gate[4] == c: ng.add((gate[0],gate[1],gate[2],gate[3],d));k +=1
            if gate[4] == d: ng.add((gate[0],gate[1],gate[2],gate[3],c));k+=1
            if gate[4] == e: ng.add((gate[0],gate[1],gate[2],gate[3],f));k+=1
            if gate[4] == f: ng.add((gate[0],gate[1],gate[2],gate[3],e));k+=1
            if gate[4] == g: ng.add((gate[0],gate[1],gate[2],gate[3],h));k+=1
            if gate[4] == h: ng.add((gate[0],gate[1],gate[2],gate[3],g));k+=1
        else:
            ng.add(gate)

    print("flipped", k,"\n\n\n\n")
    bb = bits.copy()
    ret = trywith(ng, bb)
    for x in [a,b,c,d,e,f,g,h]:
        if x is not None and x in bb: print(x, bb[x])
    print(bb["mvv"])
    return ret

def diffbits(x, y):
    a = x^y
    n = 0
    for i in range(48):
        if (x & (1 << i)) != (y & (1<<i)):n +=1; print(i)
    return n

print("\n\n\n\n\n\n\n\n\n")
# qfg vjk
#flipped = flip("gcs", "z05", "htp", "z15", "hhh", "z20")
# dkr,z05  or  gcs,z05
flipped = flip("dkr", "z05", "htp", "z15", "hhh", "z20", "rhv", "ggk")
if flipped is not None:
    print(flipped, target, flipped^target, diffbits(flipped,target))
exit()



W = Counter()
for l in F[1]:
    words = l.split()
    for word in words:
        W[word] += 1
for name in gatenames:
    if W[name] > 2: print(W[name], name)

import graphviz
g = graphviz.Digraph()
nodes = set()
colors = {"AND": "red", "OR": "green", "XOR": "blue"}
for gate in gates:
    if gate[0] not in nodes: nodes.add(gate[0]); g.node(gate[0])
    if gate[2] not in nodes: nodes.add(gate[2]); g.node(gate[2])
    if gate[4] not in nodes: nodes.add(gate[4]); g.node(gate[4])

    g.edge(gate[0], gate[4], color=colors[gate[1]])
    g.edge(gate[2], gate[4], color=colors[gate[1]])

g.engine = "neato"
g.render("d.gv",view=True)

"""
{'bvc', 'qfg', 'dkr', 'fdd', 'x06', 'y06', 'gcs', 'hdc', 'dhf', 'hrr',
 'x05', 'y05', 'nsg', 'kkt', 'x04', 'y04', 'thc', 'rrr', 'tkd', 'shd',
 'y03', 'x03', 'qhg', 'jgj', 'x02', 'y02', 'mts', 'ntr', 'wwc', 'hch',
 'x01', 'y01', 'wsg', 'pnw', 'y00', 'x00'}
"""

# z = set()
# xx = set()
# y = set()
# _bits = {}
# for l in F[0]:
#     x = l.split()
#     _bits[x[0].replace(":", "")] = bool(int(x[1]))
#     name = x[0].replace(":", "")
#     if name.startswith("x"): xx.add(name)
#     if name.startswith("y"): y.add(name)
#
# _gates = []
# src = []
#
# x = xx
#
# for l in F[1]:
#     _gates.append([*l.split()])
#
#     a = l.split()
#     if a[4].startswith("z"): z.add(a[4])

# def trywith(gates):
#     bits = _bits.copy()
#
#     def caneval(gate):
#         return gate[0] in bits and gate[2] in bits
#
#     def eval(gate):
#         if gate[1] == "AND":
#             return bits[gate[0]] and bits[gate[2]]
#         elif gate[1] == "XOR":
#             return bool(bits[gate[0]]) != bool(bits[gate[2]])
#         elif gate[1] == "OR":
#             return bits[gate[0]] or bits[gate[2]]
#         assert False
#
#     for i in range(224):
#         for gate in gates:
#             if gate[0] in bits and gate[2] in bits:
#                 if gate[4] in bits: x = bits[gate[4]]
#                 bits[gate[4]] = eval(gate)
#
#         z = []
#         for i in range(46):
#             name = "z" + format(i, "#02")
#             if name not in bits: break
#             z.append(bits[name])
#         else:
#             n = 0
#             for bit in reversed(z):
#                 n = n * 2 + (1 if bit else 0)
#             return n
#     return None
#
# nx = 0
# ny = 0
# for i in reversed(range(45)):
#     nx = nx * 2 + (1 if _bits["x" + format(i, "#02")] else 0)
# for i in reversed(range(45)):
#     ny = ny * 2 + (1 if _bits["y" + format(i, "#02")] else 0)
#
# print(nx,ny)
# expect = nx+ny
#
# _gates = set(tuple(x) for x in _gates)
# val = trywith(_gates)
# print(val, expect, val-expect, val^expect)
#
# # for i in range(46):
# #     if (val & (1 << i)) != (expect & (1 << i)):
# #         print(i+1)
#
# flips = [6,7,8,9,16,17,18,21,22,23]
#
# flow = defaultdict(set)
# for gate in _gates:
#     flow[gate[4]].add(gate[0])
#     flow[gate[4]].add(gate[2])
#
# def affected_by(id):
#     Q = deque([id])
#     V = set()
#
#     while len(Q):
#         x = Q.popleft()
#         for y in flow[x]:
#             if y in V: continue
#             V.add(y)
#             Q.append(y)
#     return V
#
# flipnames = ["z" + format(i, "#02") for i in flips]
# flips = []
# for flipname in flipnames:
#     xs = affected_by(flipname)
#     print(len(xs))
#     flips.append(xs)
#
# allflips = flips[0].intersection(flips[1]).intersection(flips[2]).intersection(flips[3]).intersection(flips[4]).intersection(flips[5]).intersection(flips[6]).intersection(flips[7])
# print(allflips)
