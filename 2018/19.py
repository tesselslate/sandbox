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
    icount = 0
    ip = regs[bip]
    while ip < len(prog):
        regs[bip] = ip
        instr = prog[ip]
        regs = ops[instr[0]](regs, instr[1], instr[2], instr[3])
        ip = regs[bip]
        ip += 1
        regs[bip] = ip
        if regs[5] > regs[4]:
            print(icount, ip, instr, regs)
        icount += 1
    return regs

#print(run([0]*6, bip, prog))
#print(run([1] + [0]*5, bip, prog))
print(run([3,0,5275662,2,10551326,10551327], bip, prog))

"""
seti 1 3 2 # ip = 1
seti 1 0 5
mulr 2 5 1
eqrr 1 4 1
addr 1 3 3
addi 3 1 3
addr 2 0 0
addi 5 1 5
gtrr 5 4 1
addr 3 1 3
seti 2 2 3
addi 2 1 2
gtrr 2 4 1
addr 1 3 3
seti 1 1 3
mulr 3 3 3
"""
