import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [int(l.strip()) for l in open(argv[1])]

def a():
    for i in range(len(F)):
        for j in range(len(F)):
            if F[i] + F[j] == 2020:
                print(F[i] * F[j])
                return

def b():
    for i in range(len(F)):
        for j in range(len(F)):
            for k in range(len(F)):
                if F[i] + F[j] + F[k] == 2020:
                    print(F[i] * F[j] * F[k])
                    exit()

a()
b()
