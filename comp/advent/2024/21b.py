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

def find_moves(pos, target, movedict):
    if pos == target: return ""

    Q = deque([(pos, "")])
    V = set(pos)
    while len(Q):
        pos, moves = Q.popleft()

        if pos == target:
            return moves

        r, c = pos
        for (rr, cc) in ul.padj4():
            nr,nc = r+rr, c+cc
            if (nr,nc) in movedict and (nr,nc) not in V:
                V.add((nr,nc))
                Q.append(((nr,nc),moves + movearrows[rr,cc]))

for code in F:
    moves = ""
    pos = (3,2)
    for char in code:
        target = positions[char]
        moves = moves + find_moves(pos, target, positions1) + "A"
        pos = target

    moves2 = ""
    pos = (0,2)
    for char in moves:
        target = positionsB[char]

        moves2 = moves2 + find_moves(pos, target, positionsB1) + "A"

        pos = target


    moves3 = ""
    pos = (0,2)
    for char in moves2:
        target = positionsB[char]

        moves3 = moves3 + find_moves(pos, target, positionsB1) + "A"

        pos = target


    moves2 = moves3
    print(code, moves2, len(moves2), ul.ints(code)[0])

    S += len(moves2) * ul.ints(code)[0]

print(S)
