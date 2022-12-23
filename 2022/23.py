import collections, util
from sys import argv

F = [l.strip() for l in open(argv[1])]
P = set()

for r in range(len(F)):
    for c in range(len(F[r])):
        if F[r][c] == "#":
            P.add((r,c))

dirs = collections.deque([
        lambda elf : (-1, 0) if not set([(elf[0]-1,elf[1]), (elf[0]-1, elf[1]-1), (elf[0]-1, elf[1]+1)]) & P else None,
        lambda elf : (1, 0) if not set([(elf[0]+1,elf[1]), (elf[0]+1, elf[1]-1), (elf[0]+1, elf[1]+1)]) & P else None,
        lambda elf : (0, -1) if not set([(elf[0]-1,elf[1]-1), (elf[0], elf[1]-1), (elf[0]+1, elf[1]-1)]) & P else None,
        lambda elf : (0, 1) if not set([(elf[0]-1,elf[1]+1), (elf[0], elf[1]+1), (elf[0]+1, elf[1]+1)]) & P else None
])

def tick():
    global P, dirs
    NP = set()
    proposed = {}
    for elf in P:
        # north
        dir = (0,0)
        adj = [
                (1,-1),
                (1,0),
                (1,1),
                (0,-1),
                (0,1),
                (-1,-1),
                (-1,0),
                (-1,1),
        ]
        f = False
        for p in adj:
            if (elf[0]+p[0], elf[1]+p[1]) in P:
                f = True
                break
        if f:
            for dirfn in dirs:
                v = dirfn(elf)
                if v:
                    dir = v
                    break
        if dir != (0,0):
            proposed[elf] = (elf[0]+dir[0],elf[1]+dir[1])
        else:
            NP.add(elf)
    mult = {}
    moves = list(proposed.values())
    for m in moves:
        mult[m] = moves.count(m)
    moved = False
    for elf, move in proposed.items():
        if mult[move] > 1:
            NP.add(elf)
            continue
        moved = True
        NP.add(move)
    dirs.rotate(-1)
    return NP, moved


def print_grid():
    mx = min([x[1] for x in P])
    Mx = max([x[1] for x in P])
    my = min([x[0] for x in P])
    My = max([x[0] for x in P])
    for y in util.irange(my, My):
        s = ""
        for x in util.irange(mx, Mx):
            if (y,x) not in P:
                s += "."
            else:
                s += "#"
        print(s)

for i in range(1000000):
    P, moved = tick()
    if i == 9:
        mx = min([x[1] for x in P])
        Mx = max([x[1] for x in P])
        my = min([x[0] for x in P])
        My = max([x[0] for x in P])
        S = 0
        for y in util.irange(my, My):
            for x in util.irange(mx, Mx):
                if (y,x) not in P:
                    S += 1
        print(S, len(P))
    if not moved:
        print(i+1)
        break
