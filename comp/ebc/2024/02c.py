import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.double_linefeed(ul.input())

target = F[0][0].split(":")[1].split(",")
G = ul.grid(F[1])

S = set()
for (r,c) in ul.gridpoints(G):
    for (rr,cc) in ul.padj4():
        for word in target:
            chars = []
            for i in range(len(word)):
                if not ul.gridcheck(G, r+(rr*i), 0): break
                chars.append(G[(r+(rr*i))][(c+(cc*i))%len(G[0])])
            else:
                if "".join(chars) == word:
                    for i in range(len(word)):
                        S.add(((r+(rr*i)),(c+(cc*i))%len(G[0])))

print(S)
print(len(S))
