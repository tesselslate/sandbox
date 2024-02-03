import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

C = 0
I = 0
X = 1
adding = None

def cycle():
    global C, I, X, adding
    if adding is not None:
        C += 1
        X += adding
        adding = None
        return

    instr = F[I].split()
    match instr[0]:
        case "noop": pass
        case "addx":
            adding = int(instr[1])
    C += 1
    I += 1
    return

S = 0
O = [[0 for _ in range(40)] for _ in range(6)]
for i in range(1,241):
    during = X
    now = (i//40,(i-1)%40)
    if abs(X-now[1]) <= 1:
        O[now[0]][now[1]] = 1
    cycle()
    if (i-20) % 40 == 0:
        S += during * (i)
print(S)
for r in O:
    print("".join("#" if r[c] else "." for c in range(len(r))))
