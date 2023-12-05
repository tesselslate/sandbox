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

S = 0

def tokenize(expr):
    i = 0
    l = []
    while i < len(expr):
        if expr[i].isdigit():
            j = i
            while i < len(expr) and expr[i].isdigit(): i += 1
            l.append(int(expr[j:i]))
            continue
        l.append(expr[i])
        i += 1
    return l

def closing(expr, i=1):
    n = 0
    while i < len(expr):
        if expr[i] == "(": n += 1
        if expr[i] == ")": n -= 1
        if n == 0: break
        i += 1
    return i

def evaluate(expr):
    v = 0
    while len(expr):
        E = expr[0]
        if type(E) == int:
            assert v == 0
            v = E
            del expr[0]
        else:
            match E:
                case "+":
                    if type(expr[1]) == int:
                        v += expr[1]
                        del expr[:2]
                    else:
                        v += evaluate(expr[2:closing(expr)])
                        del expr[:closing(expr)+1]
                case "*":
                    if type(expr[1]) == int:
                        v *= expr[1]
                        del expr[:2]
                    else:
                        v *= evaluate(expr[2:closing(expr)])
                        del expr[:closing(expr)+1]
                case "(":
                    x = evaluate(expr[1:closing(expr,0)])
                    expr[:closing(expr,0)+1] = [x]
                case ")":
                    assert False
    return v

for l in F:
    l = tokenize(l.replace(" ", ""))
    S += evaluate(l)
print(S)
