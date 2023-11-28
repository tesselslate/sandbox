import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]
F = [int(l) for l in F[0].split(',')]

def proc(Z, a, b):
    Z = Z.copy()
    Z[1] = a
    Z[2] = b
    i = 0
    while i < len(Z):
        a = Z[i]
        if a == 1:
            Z[Z[i+3]] = Z[Z[i+1]] + Z[Z[i+2]]
        elif a == 2:
            Z[Z[i+3]] = Z[Z[i+1]] * Z[Z[i+2]]
        elif a == 99:
            break
        i += 4
    return Z[0]

print(proc(F, 12, 2))

for i in range(100):
    for j in range(100):
        if proc(F, i, j) == 19690720:
            print(100 * i + j)
            exit()
