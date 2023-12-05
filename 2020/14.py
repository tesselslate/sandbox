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

F2 = []
i = 0
while i < len(F):
    assert F[i].startswith("mask")
    x, = ul.scan("mask = %s", F[i])
    i += 1
    a = []
    while i < len(F) and F[i].startswith("mem"):
        b, c = ul.scan("mem[%d] = %d", F[i])
        a.append((b,c))
        i += 1
    F2.append((x,a))
F = F2
del F2

mem = {}
for prog in F:
    for addr, v in prog[1]:
        val = v
        for i, char in enumerate(prog[0]):
            # bitmask
            match char:
                case "0": val &= ~(1 << (35 - i))
                case "1": val |= (1 << (35 - i))
                case "X": pass
        mem[addr] = val

print(sum(mem.values()))

mem = {}
for prog in F:
    for addr, v in prog[1]:
        bits = []
        for i, char in enumerate(prog[0]):
            match char:
                case "0": pass
                case "1": addr |= (1 << (35 - i))
                case "X":
                    bits.append(35 - i)
                    addr &= ~(1 << (35 - i))
        for i in range(2**len(bits)):
            mask = 0
            for j in range(i.bit_length()):
                if i & (1 << j):
                    mask |= (1 << bits[j])
            assert mask & addr == 0
            mem[mask | addr] = v

print(sum(mem.values()))
