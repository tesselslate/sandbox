import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.double_linefeed(ul.input())
A = ul.ints(F[0][0])[0]
B = ul.ints(F[0][1])[0]
C = ul.ints(F[0][2])[0]

PROG = ul.ints(F[1][0])

def run(A, B, C):
    out = []

    def evalcombo(operand):
        if 0 <= operand <= 3: return operand
        elif    operand == 4: return A
        elif    operand == 5: return B
        elif    operand == 6: return C

    PC = 0
    while PC < len(PROG):
        instr = PROG[PC]
        operand = PROG[PC+1]

        if instr == 0: # adv
            A = A // (2 ** evalcombo(operand))
        elif instr == 1: # bxl
            B ^= operand
        elif instr == 2: # bst
            B = evalcombo(operand) % 8
        elif instr == 3: # jnz
            if A != 0: PC = operand; continue
        elif instr == 4: # bxc
            B ^= C
        elif instr == 5: # out
            out.append(evalcombo(operand) % 8)
        elif instr == 6: # bdv
            B = A // (2 ** evalcombo(operand))
        elif instr == 7: # cdv
            C = A // (2 ** evalcombo(operand))

        PC += 2
    return out

print(",".join([str(x) for x in run(A, B, C)]))

def dfs(A, i=0):
    if i > 20: return
    for j in range(8):
        out = run(A * 8 + j, B, C)
        if out == PROG[len(PROG)-len(out):]:
            if out == PROG: print(A * 8 + j); exit()
            dfs(A * 8 + j, i + 1)
dfs(0)
