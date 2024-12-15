import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.double_linefeed(ul.input())
G = ul.grid(F[0])
M = "".join(F[1])

dirs = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}

def move(p, d):
    return (p[0] + d[0], p[1] + d[1])

walls = set()
boxes = set()
robot = None

for (r, c) in ul.gridpoints(G):
    x = G[r][c]
    if x == "@":
        robot = (r, c)
    elif x == "#":
        walls.add((r, c))
    elif x == "O":
        boxes.add((r, c))

for m in M:
    dir = dirs[m]
    pos = move(robot, dir)

    if pos in walls: continue
    if pos in boxes:
        push = set()

        while pos in boxes:
            push.add(pos)
            pos = move(pos, dir)
        if pos in walls: continue

        for box in push: boxes.remove(box)
        for box in push: boxes.add(move(box, dir))

    robot = move(robot, dir)

print(sum(r * 100 + c for (r, c) in boxes))

def pushv(pos, vdir):
    Q = deque([pos])

    move_l = set()
    move_r = set()

    if pos in lbox: Q.append(move(pos, (0, 1)))
    else: Q.append(move(pos, (0, -1)))

    while len(Q):
        r, c = Q.popleft()
        if (r, c) in walls:
            return False
        elif (r, c) in lbox and (r,c) not in move_l:
            move_l.add((r, c))
            Q.append(move((r, c), (vdir, 0)))
            Q.append(move((r, c), (0, 1)))
        elif (r, c) in rbox and (r,c) not in move_r:
            move_r.add((r, c))
            Q.append(move((r, c), (vdir, 0)))
            Q.append(move((r, c), (0, -1)))

    for box in move_l: lbox.remove(box)
    for box in move_l: lbox.add(move(box, (vdir, 0)))
    for box in move_r: rbox.remove(box)
    for box in move_r: rbox.add(move(box, (vdir, 0)))

    return True

walls = set()
rbox = set()
lbox = set()
robot = None

for (r, c) in ul.gridpoints(G):
    x = G[r][c]
    if x == "@":
        robot = (r, c * 2)
    elif x == "#":
        walls |= {(r, c * 2), (r, c * 2 + 1)}
    elif x == "O":
        lbox.add((r, c * 2))
        rbox.add((r, c * 2 + 1))

for m in M:
    dir = dirs[m]
    pos = move(robot, dir)

    if pos in walls: continue
    if pos in lbox or pos in rbox:
        if dir[0] == 0: # horizontal push
            push = set()

            while pos in lbox or pos in rbox:
                push.add((pos, pos in lbox))
                pos = move(pos, dir)
            if pos in walls: continue

            for box, left in push:
                if left:
                    lbox.remove(box)
                    lbox.add(move(box, dir))
                else:
                    rbox.remove(box)
                    rbox.add(move(box, dir))
        else: # vertical push
            if not pushv(pos, dir[0]): continue

    robot = move(robot, dir)

print(sum(r * 100 + c for (r, c) in lbox))
