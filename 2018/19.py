import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]

bip, = util.scan("#ip %d", F[0])
prog = []
for i in range(1, len(F)):
    a, b, c, d = util.scan("%s %d %d %d", F[i])
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

ops = {
        "addr": addr,
        "addi": addi,
        "mulr": mulr,
        "muli": muli,
        "banr": banr,
        "bani": bani,
        "borr": borr,
        "bori": bori,
        "setr": setr,
        "seti": seti,
        "gtir": gtir,
        "gtri": gtri,
        "gtrr": gtrr,
        "eqir": eqir,
        "eqri": eqri,
        "eqrr": eqrr
}

def run(regs, bip, prog):
    ip = 0
    while ip < len(prog):
        regs[bip] = ip
        instr = prog[ip]
        regs = ops[instr[0]](regs, instr[1], instr[2], instr[3])
        ip = regs[bip]
        ip += 1
        print(instr, regs)
    return regs[0]

print(run([0]*6, bip, prog))
print(run([1,0,0,0,0,0], bip, prog))
