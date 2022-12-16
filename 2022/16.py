import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]
G = util.graph()
flow = {}

for l in F:
    a, b, c = None, None, None
    if "valves" in l:
        a, b, c = util.scan("Valve %s has flow rate=%d; tunnels lead to valves %s", l)
    else:
        a, b, c = util.scan("Valve %s has flow rate=%d; tunnel leads to valve %s", l)
    for w in c.split(" "):
        G.add_edge(a, w.strip(","))
    flow[a] = b

valves = [k for k in flow.keys() if flow[k] > 0]
visitable = {}
for valve in valves + ["AA"]:
    Q = collections.deque([(valve, 0)])
    V = {}
    while len(Q) > 0:
        E = Q.popleft()
        V[E[0]] = E[1]
        for next in G.dependents(E[0]):
            if next in V:
                continue
            V[next] = E[1]+1
            Q.append((next,E[1]+1)) # type: ignore
    visitable[valve] = {}
    for key in V:
        if key in valves and key != valve:
            visitable[valve][key] = V[key]
print(visitable)

M = 0
def walk(total, ticks, opened, c):
    global M
    if len(opened) == len(valves) or ticks <= 0:
        return

    # go to next valves
    for v in valves:
        if not v in opened:
            new_ticks = ticks - visitable[c][v] - 1
            val = total + (new_ticks)*flow[v]
            M = max(M, val)
            walk(val, new_ticks, opened | {v}, v)

walk(0, 30, set(), "AA")
print(M)
