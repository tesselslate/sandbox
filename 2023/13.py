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
F = ul.double_linefeed(F)
G = [ul.grid(g) for g in F]

S = 0

def pgrid(g):
    for r in g:
        print("".join(r))

def check_vert(g, c):
    a = [g[r][:c] for r in range(len(g))]
    b = [g[r][c:] for r in range(len(g))]
    l = a if len(a[0]) > len(b[0]) else b
    s = a if len(a[0]) < len(b[0]) else b
    d = len(l[0]) - len(s[0])
    s = [list(reversed(r)) for r in s]
    for r in range(len(s)):
        for c in range(len(s[0])):
            if l[r][d+c] != s[r][c]: return False
    return True

def check_horiz(g, r):
    a = g[:r]
    b = g[r:]
    l = a if len(a) > len(b) else b
    s = a if len(a) < len(b) else b
    d = len(l) - len(s)
    s.reverse()
    for r in range(len(s)):
        for c in range(len(g[0])):
            if l[r+d][c] != s[r][c]: return False
    return True

S = 0
for g in G:
    for i in range(1, len(g[0])):
        if check_vert(g, i):
            print("vert",i)
            S += i
            break
    else:
        for i in range(1, len(g)):
            if check_horiz(g, i):
                print("horiz 100", i)
                S += i * 100
                break
        else: assert False
print(S)
