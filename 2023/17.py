import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque
import heapq

F = ul.input()
G = ul.grid(F, int)

Q = [(0, (0,0), "E", 0, ((0, 0)))]
V = set()
M = {}
while len(Q):
    (cost, (r, c), dir, dirc, path) = heapq.heappop(Q)
    k = (r,c,dir,dirc)
    if k not in V:
        V.add(k)
        if (r,c) == (len(G)-1, len(G[0])-1) and dirc >= 4:
            print(cost)
            exit()

        #nextdirs = dir if dirc < 3 else ""
        nextdirs = dir if dirc < 10 else ""
        if dirc >= 4:
            if dir in "NS": nextdirs += "EW"
            if dir in "EW": nextdirs += "NS"
        dirs = ul.dirs_rc(nextdirs)
        for ch, d in zip(nextdirs, dirs):
            ndirc = 1 if ch != dir else dirc+1
            rr, cc = r + d[0], c + d[1]
            if not ul.gridcheck(G,rr,cc): continue
            ncost = cost + G[rr][cc]
            k = (rr,cc,ch,ndirc)
            if k not in M or ncost < M[k]:
                M[k] = ncost
                heapq.heappush(Q, (ncost, (rr, cc), ch, ndirc, (*path, (rr, cc))))

                # 953 984 1079 bad
