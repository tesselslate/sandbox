import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]

samples = []
for i in range(0, 3120, 4):
    x = []
    a, b, c, d = util.scan("Before: [%d, %d, %d, %d]", F[i])
    x.append([a, b, c, d])
    a, b, c, d = util.scan("%d %d %d %d", F[i+1])
    x.append([a, b, c, d])
    a, b, c, d = util.scan("After:  [%d, %d, %d, %d]", F[i+2])
    x.append([a, b, c, d])
    samples.append(x)
prog = []
for i in range(3123, len(F)):
    a, b, c, d = util.scan("%d %d %d %d", F[i])
    prog.append([a, b, c, d])

# ops
def addr(regs, a, b, c):
    regs[c] = regs[a] + regs[b]
    return regs

def addi(regs, a, b, c):
    regs[c] = regs[a] + b
    return regs

def mulr(regs, a, b, c):
    regs[c] = regs[a] * regs[b]
    return regs

def muli(regs, a, b, c):
    regs[c] = regs[a] * b
    return regs

def banr(regs, a, b, c):
    regs[c] = regs[a] & regs[b]
    return regs

def bani(regs, a, b, c):
    regs[c] = regs[a] & b
    return regs

def borr(regs, a, b, c):
    regs[c] = regs[a] | regs[b]
    return regs

def bori(regs, a, b, c):
    regs[c] = regs[a] | b
    return regs

def setr(regs, a, b, c):
    regs[c] = regs[a]
    return regs

def seti(regs, a, b, c):
    regs[c] = a
    return regs

def gtir(regs, a, b, c):
    regs[c] = 1 if a > regs[b] else 0
    return regs

def gtri(regs, a, b, c):
    regs[c] = 1 if regs[a] > b else 0
    return regs

def gtrr(regs, a, b, c):
    regs[c] = 1 if regs[a] > regs[b] else 0
    return regs

def eqir(regs, a, b, c):
    regs[c] = 1 if a == regs[b] else 0
    return regs

def eqri(regs, a, b, c):
    regs[c] = 1 if regs[a] == b else 0
    return regs

def eqrr(regs, a, b, c):
    regs[c] = 1 if regs[a] == regs[b] else 0
    return regs

ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

S = 0
possible = [set() for _ in range(16)]
for s in samples:
    c = 0
    regs = s[0]
    instr = s[1]
    for op in ops:
        if op(regs.copy(), instr[1], instr[2], instr[3]) == s[2]:
            possible[instr[0]].add(op)
            c += 1
    if c >= 3:
        S += 1
print(S)

# solved by hand lol
regs = [0,0,0,0]
ops = [bani, banr, muli, setr, bori, eqrr, gtir, mulr, gtrr, seti, gtri, eqri, addi, borr, eqir, addr]
for instr in prog:
    regs = ops[instr[0]](regs, instr[1], instr[2], instr[3])
print(regs[0])
