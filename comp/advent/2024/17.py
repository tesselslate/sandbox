import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.double_linefeed(ul.input())
_A = ul.ints(F[0][0])[0]
_B = ul.ints(F[0][1])[0]
_C = ul.ints(F[0][2])[0]

PROG = ul.ints(F[1][0])

def run(A, B, C):
    out = []

    def evalcombo(operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4: return A
        elif operand == 5: return B
        elif operand == 6: return C
        else: raise ValueError()
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
            if A != 0:
                # print(A)
                PC = operand; continue
        elif instr == 4: # bxc
            # read but ignore operand
            B ^= C
        elif instr == 5: # out
            # print("out, ", evalcombo(operand) % 8)
            out.append(evalcombo(operand) % 8)
        elif instr == 6: # bdv
            B = A // (2 ** evalcombo(operand))
        elif instr == 7: # cdv
            C = A // (2 ** evalcombo(operand))

        PC += 2
    return out

S = 88920464920329
assert S > 8**15
for i in range(109020022673161, S, -1):
    out = run(i, _B, _C)
    if out == PROG: print(i)

"""
[2, 4, 1, 5, 7, 5, 0, 3, 4, 1, 1, 5, 4, 0, 5, 1]
[2, 4, 1, 5, 7, 5, 0, 3, 4, 1, 1, 6, 5, 5, 3, 0]
- 88964052127497 


109020022673161





Register A: 47719761
Register B: 0
Register C: 0

Program: 2,4,1,5,7,5,0,3,4,1,1,6,5,5,3,0

2,4 bst A       B = A%8
1,5 bxl         B ^= 5
7,5 cdv         C = A // (2^B)
0,3 adv         A = A // 8
4,1 bxc         B ^= C
1,6 bxl         B ^= 6
5,5 out !       print(B % 8)
3,0 jnz !

B = A%8
C = A // (2**(B^5))
A = A // 8
B ^= 3 ^ C
print(B%8)


B = 4
print(2)

loop needs to run 16 times
A decreases by about 8 each time


88920011934106  2415751556304632
88920011935489  2415751556307401
88920011935497  2415751556307411
88920028645786  2415751656104632
88920028647169  2415751656107401
88920028647177  2415751656107411
88920028672777
88920028711322
88920028712705
88920028712713
"""
