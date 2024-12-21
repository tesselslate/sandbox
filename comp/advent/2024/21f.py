import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

numpad = {
    (0,0): "7",
    (0,1): "8",
    (0,2): "9",
    (1,0): "4",
    (1,1): "5",
    (1,2): "6",
    (2,0): "1",
    (2,1): "2",
    (2,2): "3",
    (3,1): "0",
    (3,2): "A",
}

dirpad = {
    (0,1): "^",
    (0,2): "A",
    (1,0): "<",
    (1,1): "v",
    (1,2): ">",
}

movearrows = {
    (-1,0): "^",
    (1,0): "v",
    (0,1): ">",
    (0,-1): "<",
}

ok_numpad = frozenset(numpad.keys())
ok_dirpad = frozenset(dirpad.keys())

numpad_rev = {v: k for k, v in numpad.items()}
dirpad_rev = {v: k for k, v in dirpad.items()}

NP_START = numpad_rev["A"]
DP_START = dirpad_rev["A"]

@functools.cache
def manhat(code):
    s = 0

    for a,b in itertools.pairwise(code):
        a, b = dirpad_rev[a], dirpad_rev[b]
        s += abs(a[0]-b[0]) + abs(a[1]-b[1])

    return s

# @functools.cache
# def move_between(src, dst, ok):
#     Q = deque([(src, "", set())])
#     V = []
#
#     while len(Q):
#         pos, moves, visited = Q.popleft()
#
#         if pos == dst:
#             V.append(moves)
#             continue
#
#         for (rr, cc) in ul.padj4():
#             nr, nc = pos[0] + rr, pos[1] + cc
#             if (nr, nc) in ok and not (nr, nc) in visited:
#                 Q.append(((nr, nc), moves + movearrows[rr, cc], {(nr, nc)} | visited.copy()))
#
#     return V

def move_between(src, dst, ok):
    Q = deque([(src, "")])
    VV = set()
    V = []

    while len(Q):
        pos, moves = Q.popleft()

        if pos == dst:
            V.append(moves)
            continue

        for (rr, cc) in ul.padj4():
            nr, nc = pos[0] + rr, pos[1] + cc
            if (nr, nc) in ok and not (nr, nc) in VV:
                VV.add((nr, nc))
                Q.append(((nr, nc), moves + movearrows[rr, cc]))

    return V

def best(movesets, filter):
    target = min(filter(moveset) for moveset in movesets)
    return [moveset for moveset in movesets if filter(moveset) == target][0]

def all_numpad(code):
    pos = NP_START

    inputs = []
    Q = deque([(code, "")])
    while len(Q):
        code, moves = Q.popleft()

        if len(code) == 0:
            inputs.append(moves)
            continue

        movesets = move_between(pos, numpad_rev[code[0]], ok_numpad)
        for moveset in movesets:
            Q.append((code[1:], moves + moveset + "A"))

    return inputs

@functools.cache
def cost(src, dst, depth):
    if depth == 1:
        return len(best(move_between(src, dst, ok_dirpad), len)) + 1

    movesets = move_between(src, dst, ok_dirpad)

    best_n = math.inf
    for moveset in movesets:
        n = 0
        nsrc, ndst = src, dst

        for move in (moveset + "A"):
            ndst = dirpad_rev[move]
            n += cost(nsrc, ndst, depth - 1)
            nsrc = ndst

        best_n = min(best_n, n)

    return best_n

S = 0
for code in F:
    all_inputs = all_numpad(code)

    best_n = math.inf
    for inputs in all_inputs:
        src = DP_START
        s = 0

        for inp in inputs:
            dst = dirpad_rev[inp]
            s += cost(src, dst, 1)
            src = dst

        best_n = min(best_n, s)
    print(code, best_n)
    S += ul.ints(code)[0] * best_n
print(S)
