import collections, itertools, util
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

valves = {k for k in flow.keys() if flow[k] > 0}
visitable = {}
for valve in valves | {"AA"}:
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

def walk(total, ticks, opened, c):
    global M
    if ticks <= 0:
        return

    # go to next valves
    for v in valves - opened:
        new_ticks = ticks - visitable[c][v] - 1
        val = total + (new_ticks)*flow[v]
        M = max(M, val)
        walk(val, new_ticks, opened | {v}, v)

def walk2(total, ticks, opened, a, b):
    global M
    if ticks <= 0:
        return

    wait = min(a[1], b[1])
    ticks -= wait
    a[1] -= wait
    b[1] -= wait

    if [a[1], b[1]] == [0, 0]:
        # both can move
        movable = valves - opened
        if len(movable) >= 2:
            for m in itertools.permutations(movable, 2):
                aw = visitable[a[0]][m[0]] + 1
                bw = visitable[b[0]][m[1]] + 1
                at = ticks - aw
                bt = ticks - bw
                val = total + at*flow[m[0]] + bt*flow[m[1]]
                M = max(M, val)
                walk2(val, ticks, opened | {m[0], m[1]}, [m[0], aw], [m[1], bw])
        elif len(movable) == 1:
            for v in movable:
                d = ticks - visitable[a[0]][v] - 1
                M = max(M, total + d*flow[v])
                d = ticks - visitable[b[0]][v] - 1
                M = max(M, total + d*flow[v])
    else:
        # one can move
        for v in valves - opened:
            n = None
            if a[1] == 0:
                n = a.copy()
            else:
                n = b.copy()
            n[1] = visitable[n[0]][v] + 1
            n[0] = v
            new_ticks = ticks - n[1]
            val = total + (new_ticks)*flow[v]
            M = max(M, val)
            na, nb = (n, b.copy()) if a[1] == 0 else (a.copy(), n)
            walk2(val, ticks, opened | {v}, na, nb)

M = 0
walk(0, 30, set(), "AA")
print(M)

M = 0
walk2(0, 26, set(), ["AA", 0], ["AA", 0])
print(M)
