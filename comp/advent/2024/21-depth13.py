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

@functools.cache
def all_move_sequences(code, padkey, start):
    pad = pads[padkey]

    # if len(code) == 0: return ""
    #
    # next_moves = all_moves(start, pad[code[0]], frozenset(k for k in pad.values()))
    # return next_moves + "A" + all_move_sequences(code[1:], padkey, pad[code[0]])

    FULLMOVES = ""

    while len(code) > 0:
        next_moves = all_moves(start, pad[code[0]], padkey)
        FULLMOVES = next_moves + "A" + FULLMOVES
        start = pad[code[0]]
        code = code[1:]

    return FULLMOVES

@functools.cache
def best_nested(code, depth, start=(0,2)):
    if depth == 0: return code

    moves = all_move_sequences(code, 1, start)
    print(f"done depth {depth} ({len(moves)})")
    return best_nested(moves, depth - 1, start)

for code in F:
    # x = []
    # a = all_move_sequences(code, 0, (3,2))
    # a_target = min(len(y) for y in a)
    # a = [y for y in a if len(y) == a_target]
    # print("\t",len(a))
    # for a in a:
    #     b = all_move_sequences(a, 1, (0,2))
    #     b_target = min(len(y) for y in b)
    #     b = [y for y in b if len(y) == b_target]
    #     print("\t",len(b))
    #     for b in b:
    #         c = all_move_sequences(b, 1, (0,2))
    #         x.extend(c)

    a = all_move_sequences(code, 0, (3,2))
    best = best_nested(a, 25)

    S += ul.ints(code)[0] * len(best)
    print(code, len(best))

print(S)

# def find_moves(pos, target, movedict, avoid):
#     if pos == target: return ""
#
#     Q = deque([(pos, "", None)])
#     V = set((pos,None))
#     allmoves = []
#     while len(Q):
#         pos, moves, dir = Q.popleft()
#
#         if pos == target:
#             allmoves.append(moves)
#             continue
#
#         r, c = pos
#         for (rr, cc) in ul.padj4():
#             if movearrows[rr,cc] != dir: continue
#             nr,nc = r+rr, c+cc
#             if (nr,nc) in movedict and (nr,nc,rr,cc) not in V and (nr,nc) not in avoid:
#                 V.add((nr,nc,rr,cc))
#                 Q.append(((nr,nc),moves + movearrows[rr,cc], movearrows[rr,cc]))
#         for (rr, cc) in ul.padj4():
#             nr,nc = r+rr, c+cc
#             if (nr,nc) in movedict and (nr,nc,rr,cc) not in V and (nr,nc) not in avoid:
#                 V.add((nr,nc,rr,cc))
#                 Q.append(((nr,nc),moves + movearrows[rr,cc], movearrows[rr,cc]))
#
#     return allmoves[0]
#
# for code in F:
#     moves = ""
#     pos = (3,2)
#     for char in code:
#         target = positions[char]
#         moves = moves + find_moves(pos, target, positions1, {(3,0)}) + "A"
#         pos = target
#
#     print(moves)
#
#     moves2 = ""
#     pos = (0,2)
#     for char in moves:
#         target = positionsB[char]
#
#         moves2 = moves2 + find_moves(pos, target, positionsB1, {(0,0)}) + "A"
#
#         pos = target
#
#     print(moves2)
#
#     moves3 = ""
#     pos = (0,2)
#     for char in moves2:
#         target = positionsB[char]
#
#         moves3 = moves3 + find_moves(pos, target, positionsB1, {(0,0)}) + "A"
#
#         pos = target
#
#
#     moves2 = moves3
#     print(code, moves2, len(moves2), ul.ints(code)[0])
#
#     S += len(moves2) * ul.ints(code)[0]
#
# print(S)
