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

@functools.cache
def move_between(src, dst, ok):
    Q = deque([(src, "", set())])
    V = []

    while len(Q):
        pos, moves, visited = Q.popleft()

        if pos == dst:
            V.append(moves)
            continue

        for (rr, cc) in ul.padj4():
            nr, nc = pos[0] + rr, pos[1] + cc
            if (nr, nc) in ok and not (nr, nc) in visited:
                Q.append(((nr, nc), moves + movearrows[rr, cc], {(nr, nc)} | visited.copy()))

    target = min(manhat(x) for x in V)
    return [x for x in V if manhat(x) == target][0]

def all_numpad(code):
    pos = NP_START
    inputs = []

    for char in code:
        inputs.extend(move_between(pos, numpad_rev[char], ok_numpad))
        inputs.append("A")
        pos = numpad_rev[char]

    return "".join(inputs)

@functools.cache
def cost(src, dst, depth):
    if depth == 1:
        return manhat(move_between(src, dst, ok_dirpad)) + 1

    moves = move_between(src, dst, ok_dirpad) + "A"
    n = 0

    for move in moves:
        dst = dirpad_rev[move]
        n += cost(src, dst, depth - 1)
        src = dst

    return n

S = 0
for code in F:
    s = 0
    inputs = all_numpad(code)
    print(inputs)

    src = DP_START
    for inp in inputs:
        dst = dirpad_rev[inp]
        s += cost(src, dst, 2)
        src = dst
    print(code,s)
    S += ul.ints(code)[0] * s
print(S)
