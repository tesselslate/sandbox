import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

def mkgrid(grid):
    return {c: (i//3, i%3) for i, c in enumerate(grid) if c != " "}

numpad = mkgrid("789456123 0A")
dirpad = mkgrid(" ^A<v>")

def path_from(src, dst, pad):
    sr, sc = pad[src]
    dr, dc = pad[dst]

    h = ["", ">", "<"][ul.sign(dc-sc)]
    v = ["", "v", "^"][ul.sign(dr-sr)]

    P = set()

    if (sr, dc) in pad.values(): P.add(h * abs(sc-dc) + v * abs(sr-dr))
    if (dr, sc) in pad.values(): P.add(v * abs(sr-dr) + h * abs(sc-dc))

    return P

def gen_pad_paths(src, code, pad):
    paths = [
        path_from(a, b, pad)
        for a, b in itertools.pairwise(src + code)
    ]

    return ["A".join(path) + "A" for path in itertools.product(*paths)]

@functools.cache
def moves(src, dst, depth):
    if depth == 0:
        return 1

    paths = path_from(src, dst, dirpad)
    best = math.inf

    for path in paths:
        n = sum(
            moves(a, b, depth - 1)
            for a, b in itertools.pairwise("A" + path + "A")
        )
        best = min(best, n)

    return best

def complexity(code, depth):
    paths = gen_pad_paths("A", code, numpad)
    best = math.inf

    for path in paths:
        n = sum(
            moves(a, b, depth)
            for a, b in itertools.pairwise("A" + path)
        )
        best = min(best, n)

    return int(code[:3]) * best

print(sum(complexity(l, 2) for l in F))
print(sum(complexity(l, 25) for l in F))
