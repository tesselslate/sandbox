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

arrows = {
    (0,1): ">",
    (0,-1): "<",
    (1,0): "v",
    (-1,0): "^",
    (0,0): "",
}

def revextend(d):
    nd = {}
    for k, v in d.items():
        nd[v] = k
        nd[k] = v
    return nd

numpad = revextend(numpad)
dirpad = revextend(dirpad)

def path_from(src, dst, pad):
    sr, sc = src
    dr, dc = dst
    h = (0, ul.sign(dc-sc))
    v = (ul.sign(dr-sr), 0)

    P = set()

    if (sr, dc) in pad:
        P.add(arrows[h] * abs(sc-dc) + arrows[v] * abs(sr-dr))
    if (dr, sc) in pad:
        P.add(arrows[v] * abs(sr-dr) + arrows[h] * abs(sc-dc))

    return P

def gen_pad_paths(src, code, pad):
    paths = []
    for a, b in itertools.pairwise(pad[src] + code):
        paths.append(path_from(pad[a], pad[b], pad))

    full_paths = list(itertools.product(*paths))
    return ["A".join(path) + "A" for path in full_paths]

@functools.cache
def moves(src, dst, depth):
    if depth == 1:
        return 1

    paths = path_from(src, dst, dirpad)
    best = math.inf

    for path in paths:
        n = 0
        for a, b in itertools.pairwise("A" + path + "A"):
            n += moves(dirpad[a], dirpad[b], depth - 1)

        best = min(best, n)

    return best

S = 0
for code in F:
    numpad_paths = gen_pad_paths(numpad["A"], code, numpad)
    best = math.inf

    for path in numpad_paths:
        n = 0
        print(path)
        for i, char in enumerate(path):
            if i == 0: prev = dirpad["A"]
            else: prev = dirpad[path[i-1]]
            n += moves(prev, dirpad[char], 26)

        best = min(best, n)

    print(code, best)
    S += ul.ints(code)[0] * best
print(S)
