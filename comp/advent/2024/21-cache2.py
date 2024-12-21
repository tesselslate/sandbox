import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
S = 0

positions1 = {
        (0,0):"7",
        (0,1):"8",
        (0,2):9,
        (1,0):4,
        (1,1):5,
        (1,2):6,
        (2,0):1,
        (2,1):2,
        (2,2):3,
        (3,1):0,
        (3,2):"A",
}
positions = {str(v): k for k, v in positions1.items()}
movearrows = {
    (-1,0):"^",
    (1,0):"v",
    (0,1):">",
    (0,-1):"<",
    }

positionsB1 = {
        (0,1):"^",
        (0,2):"A",
        (1,0):"<",
        (1,1):"v",
        (1,2):">",
}
positionsB = {v: k for k, v in positionsB1.items()}

pos = (3,2)

@functools.cache
def manhat(code):
    pos = (0, 2)
    s = 0

    for a,b in itertools.pairwise(code):
        a, b = positionsB[a], positionsB[b]
        s += abs(a[0]-b[0]) + abs(a[1]-b[1])

    return s

@functools.cache
def all_moves(src, dst, ok):
    ok = fpads[ok]
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

ok_numpad = {k for k in positions1.keys()}
ok_dirpad = {k for k in positionsB1.keys()}

numpad = positions
dirpad = positionsB

pads = [numpad, dirpad]
fpads = [frozenset(k for k in pad.values()) for pad in pads]

from textwrap import wrap
from math import log2

def all_move_sequences_split(code, padkey, start):
    segments = wrap(code, 4096)

    FULLMOVES = []

    for segment in segments:
        moves, start = allmoveseqsplitinner(segment, padkey, start, 4096)
        # moves, start = all_move_sequences(segment, padkey, start)
        FULLMOVES.append(moves)

    return "".join(FULLMOVES)

@functools.cache
def allmoveseqsplitinner(code, padkey, start, wraplen):
    if wraplen > 64 and len(code) > wraplen:
        segments = wrap(code, wraplen)
        FULLMOVES = []

        for segment in segments:
            moves, start = allmoveseqsplitinner(segment, padkey, start, wraplen // 32)
            FULLMOVES.append(moves)

        return "".join(FULLMOVES), start
    else:
        return all_move_sequences(code, padkey, start)

def all_move_sequences(code, padkey, start):
    pad = pads[padkey]

    FULLMOVES = ""

    while len(code) > 0:
        next_moves = all_moves(start, pad[code[0]], padkey)
        FULLMOVES = next_moves + "A" + FULLMOVES
        start = pad[code[0]]
        code = code[1:]

    return FULLMOVES, start

def best_nested(code, depth, start=(0,2)):
    if depth == 0: return code

    moves = all_move_sequences_split(code, 1, start)
    print(f"done depth {depth}, {len(moves)}")
    return best_nested(moves, depth - 1, start)

# for code in F:
#     a, _ = all_move_sequences(code, 0, (3,2))
#     best = best_nested(a, 25)
#
#     S += ul.ints(code)[0] * len(best)
#     print(code, len(best))
#
# print("all_moves", all_moves.cache_info().misses, all_moves.cache_info().hits)
# print("all_move_seq_split", allmoveseqsplitinner.cache_info().misses, allmoveseqsplitinner.cache_info().hits)
# print(S)

for char in "<>v^":
    best = best_nested(char, 20)
    print(char, len(best))
