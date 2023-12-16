import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F)

dstr = "NESW"
dirs = ul.dirs_rc(dstr)
def dir(x): return dirs[dstr.index(x)]

def energy(r, c, d):
    Q = deque([(r,c,d)])
    V = set()
    while True:
        NQ = deque()
        while len(Q):
            (r,c,d) = Q.popleft()

            if (r,c,d) in V: continue
            if ul.gridcheck(G,r,c): V.add((r,c,d))
            r += dir(d)[0]
            c += dir(d)[1]
            if not ul.gridcheck(G,r,c): continue

            match G[r][c]:
                case ".": NQ.append((r,c,d))
                case "-":
                    if d in "EW": NQ.append((r,c,d))
                    else: NQ.extend((r,c,d) for d in "EW")
                case "|":
                    if d in "NS": NQ.append((r,c,d))
                    else: NQ.extend((r,c,d) for d in "NS")
                case "/":
                    tt = {
                            "N": "E", "E": "N",
                            "S": "W", "W": "S",
                    }
                    NQ.append((r,c,tt[d]))
                case "\\":
                    tt = {
                            "N": "W", "W": "N",
                            "S": "E", "E": "S",
                    }
                    NQ.append((r,c,tt[d]))
        Q = NQ
        if not len(NQ): break
    return len(set((r,c) for (r,c,_) in V))

print(energy(0, -1, "E"))

M = 0
for (r,c) in ul.gridpoints(G):
    starts = []
    if r == 0: starts.append("S")
    if r == len(G)-1: starts.append("N")
    if c == 0: starts.append("E")
    if c == len(G[0])-1: starts.append("W")
    for d in starts:
        v = energy(r,c,d)
        if v > M: M = v
print(M)
