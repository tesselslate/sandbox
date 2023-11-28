import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]
F = [int(l) for l in F[0].split('-')]

def proc(i):
    s = str(i)
    m = 0
    b = False
    for j in range(6):
        if int(s[j]) < m:
            return False
        if j > 0 and s[j] == s[j-1]:
            b = True
        m = int(s[j])
    return b
def proc2(i):
    s = str(i)
    m = 0
    b = False

    ch, ct = None, 0
    for j in range(6):
        if s[j] == ch:
            ct += 1
        else:
            if ct == 2:
                b = True
            ch, ct = s[j], 1
        if int(s[j]) < m:
            return False
        m = int(s[j])
    return b or ct == 2

S = 0
S2 = 0
for i in range(F[0], F[1]+1):
    if proc(i): S += 1
    if proc2(i): S2 += 1
print(S, S2)
