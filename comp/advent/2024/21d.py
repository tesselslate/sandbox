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
def all_moves(src, dst, ok):
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

    target = min(len(x) for x in V)
    return [x for x in V if len(x) == target]

ok_numpad = {k for k in positions1.keys()}
ok_dirpad = {k for k in positionsB1.keys()}

numpad = positions
dirpad = positionsB

pads = [numpad, dirpad]

@functools.cache
def all_move_sequences(code, padkey, start):
    pad = pads[padkey]
    V = []

    if len(code) == 0: return ['']

    for move_set in all_moves(start, pad[code[0]], frozenset(k for k in pad.values())):
        poss = all_move_sequences(code[1:], padkey, pad[code[0]])
        for p in poss:
            V.append(move_set + "A" + p)

    return V

@functools.cache
def best_nested(code, depth, start=(0,2)):
    V = []
    if depth == 0: return [code]
    for moves in all_move_sequences(code, 1, start):
        poss = best_nested(moves, depth - 1, start)
        V.extend(poss)
    target = min(len(x) for x in V)
    return [x for x in V if len(x) == target]

for code in F:
    print(code)
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
    x = []
    for a in a:
        x.extend(best_nested(a, 2))

    best = "904857698456745986745967459684756983457609384576039485670394586734095867340958673450986734590687435096874350968347560983475609843576098435760934857609348567340958673495867349058674390586734590867435906873459608347560984375609843576098345769804357690843257690824357690834275698345769038457609384576093485673098456"
    for inputs in x:
        if len(inputs) < len(best):
            best = inputs
    S += ul.ints(code)[0] * len(best)
    print(code, len(best), best)
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
