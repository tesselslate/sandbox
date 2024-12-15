import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.double_linefeed(ul.input())
G = ul.grid(F[0])

M = "".join(F[1])

NG = []
for r in G:
    a = []
    for c in r:
        if c == "#":
            a.append("#")
            a.append("#")
        elif c == "O":
            a.append("[")
            a.append("]")
        elif c == ".":
            a.append(".")
            a.append(".")
        else:
            a.append("@")
            a.append(".")
    NG.append(a)
G = NG

sr, sc = 0,0
for (r,c) in ul.gridpoints(G):
    if G[r][c] == "@":
        sr,sc = r,c
        G[r][c] = "."
        break

OC = 0
for (r,c)in ul.gridpoints(G):
    if G[r][c] == "O": OC += 1

dirs = {
        "^": (-1, 0),
        "v": (1,0),
        "<": (0,-1),
        ">": (0,1),
}

def move(pt, d):
    return (pt[0] + d[0], pt[1] + d[1])

def pgrid():
    for r in range(len(G)):
        assert G[sr][sc] == "."
        G[sr][sc] = "@"
        print("".join(G[r]))
        G[sr][sc] = "."
    print("\n\n\n\n\n")

def canpush(pos, vdir):
    r, c = pos
    if G[r][c] == "#": return False
    if G[r][c] == ".": return True
    if G[r][c] == "[": # ]
        return canpush((r+vdir,c), vdir) and canpush((r+vdir,c+1), vdir)
    else:
        assert G[r][c] == "]"
        return canpush((r+vdir,c-1), vdir) and canpush((r+vdir,c), vdir)

def pushv(pos, vdir, pushed):
    r, c = pos

    if pos in pushed: return
    pushed.add(pos)
    print("push", r, c)
    # pgrid()

    if G[r][c] == "[": # ]
        pushv((r+vdir, c), vdir, pushed)
        pushv((r+vdir, c+1), vdir, pushed)
        G[r+vdir][c] = "[" #]
        G[r+vdir][c+1] = "]"
        G[r][c] = "."
        G[r][c+1] = "."
    elif G[r][c] == "]":
        pushv((r+vdir, c), vdir, pushed)
        pushv((r+vdir, c-1), vdir, pushed)
        G[r+vdir][c] = "]"
        G[r+vdir][c-1] = "[" #]
        G[r][c] = "."
        G[r][c-1] = "."
    else:
        assert G[r][c] == "."

def push(pos, dir):
    global G
    pgrid()
    op = pos
    if dir[0] == 0:
        # horz
        count = 0
        while G[pos[0]][pos[1]] == "[" or G[pos[0]][pos[1]] == "]":
            pos = move(pos, dir)
            count += 1
        if G[pos[0]][pos[1]] == "#": return False
        print(count)

        pos = op

        if dir[1] == 1:
            # right
            G[pos[0]][pos[1]+1:pos[1]+count+1] = G[pos[0]][pos[1]:pos[1]+count]
            G[pos[0]][pos[1]] = "."
            print(pos[1] + count + 1)
            # for c in range(pos[1] + count + 1, pos[1], -1):
            #     G[pos[0]][c] = G[pos[0]][c-1]
        else:
            # left
            G[pos[0]][pos[1]-count:pos[1]] = G[pos[0]][pos[1]-count+1:pos[1]+1]
            G[pos[0]][pos[1]] = "."
            print(pos[1] - count)
            # for c in range(pos[1] - count, pos[1]):
            #     G[pos[0]][c] = G[pos[0]][c+1]
    else:
        # vert
        ok = canpush(pos, dir[0])
        if not ok: return False

        pushv(pos, dir[0], set())
    print(sr,sc,d, m)
    #pgrid()
    return True

for m in M:
    d = dirs[m]

    r, c = move((sr, sc), d)
    if G[r][c] == "#": continue
    if G[r][c] == "[" or G[r][c] == "]":
        if push((r, c), d):
            sr, sc = r, c
    else:
        sr, sc = r, c

    print("step", sr, sc, d, m)
    # print(sr,sc,d, m)
    # pgrid()

S = 0
print(OC)
OC = 0
for (r,c) in ul.gridpoints(G):
    if G[r][c] == "[":
        S += (r)*100 + c
        OC += 1

print(S)
print(OC)
