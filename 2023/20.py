import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = {}

LO = False
HI = True

for l in F:
    a, xs = ul.scan("%s -> %s", l)
    G[a] = [x.strip() for x in xs.split(",")]

S_F = {k[1:]: False for k in G if k.startswith("%")}
S_C = {k[1:]: {} for k in G if k.startswith("&")}
for k, xs in G.items():
    for x in xs:
        if x in S_C: S_C[x][k[1:]] = LO

ks = list(G.keys())
for k in ks:
    if k[0] == "&" or k[0] == "%":
        G[k[1:]] = G[k]
        del G[k]

lo, hi = 0, 0
v = set()
for i in itertools.count():
    if i == 1000: print("part 1:", lo * hi)
    rx_lo, rx_hi = 0, 0

    pulses = deque([(None, "broadcaster", LO)])
    while len(pulses):
        (sender, module, ptype) = pulses.popleft()
        if ptype == LO: lo += 1
        else: hi += 1

        if module == "broadcaster":
            for child in G["broadcaster"]:
                pulses.append((module, child, ptype))
        elif module in S_F:
            if ptype == LO:
                send_type = LO if S_F[module] else HI
                for child in G[module]:
                    pulses.append((module, child, send_type))
                S_F[module] = not S_F[module]
        elif module in S_C:
            S_C[module][sender] = ptype
            send_type = LO if list(S_C[module].values()).count(HI) == len(S_C[module]) else HI
            for child in G[module]:
                pulses.append((module, child, send_type))
        else:
            assert module == "rx"
            if ptype == LO: rx_lo += 1
            else: rx_hi += 1

    k = "".join(['1' if S_F[x] else '0' for x in S_F] + ['1' if list(S_C[x].values()).count(HI) == len(S_C[x]) else '0' for x in S_C])
    if k in v: print(i, k)
    v.add(k)
    if rx_lo == 1 and rx_hi == 0: print("part 2:", i, k); break
