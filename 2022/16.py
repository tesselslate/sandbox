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

flow_count = len([k for k in flow.keys() if flow[k] > 0])
print(flow_count)
M = 0
def walk(total, ticks, opened, moves: list):
    global M
    if ticks <= 0:
        return
    if len(opened) == flow_count:
        return
    if total > M:
        print(total, opened)
    M = max(M, total)

    current = moves[-1]
    next = G.dependents(current)
    possible_opens = [x for x in next if x not in opened]
    if possible_opens:
        max_flow = max(possible_opens, key=lambda x:flow[x])
        walk(total + (max(ticks - 2, 0)) * flow[max_flow], ticks-2, opened | {max_flow}, moves.copy() + [max_flow])
    for move in next:
        if len(moves) > 1 and moves[-2] == move:
            continue
        m = moves.copy() + [move]
        walk(total, ticks-1, opened, m)

walk(0, 30, set(), ["AA"])
print(M)
