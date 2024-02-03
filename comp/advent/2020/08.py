import functools, math, re, string, sys, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

if len(sys.argv) > 1:
    F = open(sys.argv[1])
else:
    F = sys.stdin.readlines()
    if not F[-1].strip():
        del F[-1]

F = [l.strip() for l in F]

S = 0

i = 0
acc = 0
r = set()
while i < len(F):
    if i in r:
        break
    r.add(i)
    l = F[i]
    a, b = ul.scan("%s %d", l)
    match a:
        case "acc":
            acc += int(b)
            i += 1
        case "jmp":
            i += int(b)
        case "nop":
            i += 1
print(acc)

indices = [i for i in range(len(F)) if "nop" in F[i] or "jmp" in F[i]]
for index in indices:
    i = 0
    acc = 0
    r = set()
    bad = False

    old = F[index]
    if "nop" in F[index]:
        F[index] = F[index].replace("nop", "jmp")
    elif "jmp" in F[index]:
        F[index] = F[index].replace("jmp", "nop")

    while i < len(F):
        if i in r:
            bad = True
            break
        r.add(i)
        l = F[i]
        a, b = ul.scan("%s %d", l)
        match a:
            case "acc":
                acc += int(b)
                i += 1
            case "jmp":
                i += int(b)
            case "nop":
                i += 1
    F[index] = old
    if not bad:
        assert i == len(F)
        print(acc)
        break
