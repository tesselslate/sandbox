import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]
A = [l for l in F[0].split(',')]
B = [l for l in F[1].split(',')]
P = {}
D = 99999999

def proc(a, x):
    global D
    s = (0,0)
    P = {s}
    for instr in a:
        dir = instr[0]
        num = int(instr[1:])
        if dir == 'R':
            vec = (1,0)
        elif dir == 'L':
            vec = (-1,0)
        elif dir == 'U':
            vec = (0,1)
        elif dir == 'D':
            vec = (0,-1)
        for i in range(num):
            s = (s[0] + vec[0], s[1] + vec[1])
            P.add(s)
            if s in x:
                v = util.manhattan(s[0], s[1], 0, 0)
                if v < D:
                    D = v
    return P

P = proc(A, {})
proc(B, P)
print(D)

P = {}
D = 99999999

def proc2(a, x):
    global D
    s = (0,0)
    P = dict()
    c = 0
    for instr in a:
        dir = instr[0]
        num = int(instr[1:])
        if dir == 'R':
            vec = (1,0)
        elif dir == 'L':
            vec = (-1,0)
        elif dir == 'U':
            vec = (0,1)
        elif dir == 'D':
            vec = (0,-1)
        for i in range(num):
            c += 1
            s = (s[0] + vec[0], s[1] + vec[1])
            P[s] = c
            if s in x:
                v = x[s] + c
                if v < D:
                    D = v
    return P

P = proc2(A, {})
proc2(B, P)
print(D)
