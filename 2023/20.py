import itertools, math, ul
from collections import deque

F = ul.input()

LO, HI = False, True

M = {}
for l in F:
    name, outputs = ul.scan("%s -> %s", l)
    M[name] = [x.strip() for x in outputs.split(",")]
S = {k[1:]: {} if k.startswith("&") else LO for k in M}
S['rx'] = None
for k, outputs in M.items():
    for x in outputs:
        if type(S[x]) == dict: S[x][k[1:]] = LO
for k in list(M.keys()):
    M[k[1:]] = M[k]
    del M[k]

f = [k for k, v in M.items() if "rx" in v][0]
C = {k: -1 for k, v in M.items() if f in v}

lo, hi = 0, 0
for i in itertools.count(1):
    Q = deque([(None, "roadcaster", LO)])
    while len(Q):
        (sender, module, ptype) = Q.popleft()
        if ptype == LO: lo += 1
        else: hi += 1

        if sender in C and ptype == HI and C[sender] < 0: C[sender] = i

        if module == "roadcaster":
            for next in M[module]:
                Q.append((module, next, LO))
        elif type(S[module]) == bool: # flipflop
            if ptype == HI: continue
            S[module] = not S[module]
            for next in M[module]:
                Q.append((module, next, S[module]))
        elif type(S[module]) == dict: # conjunction
            S[module][sender] = ptype
            ptype = LO if list(S[module].values()).count(HI) == len(S[module]) else HI
            for next in M[module]:
                Q.append((module, next, ptype))
    if i == 1000: print(lo*hi)
    if min(C.values()) > 0: print(math.lcm(*C.values())); break
