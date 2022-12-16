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

M = 0

@dataclass
class State:
    S = 0
    C = "AA"
    opened = set()

    def add_flow(self):
        global M
        for valve in self.opened:
            self.S += flow[valve]
        M = max(M, self.S)
        if M == self.S:
            print(M, self)

    def run(self, ticks):
        if ticks == 0:
            return

        open = flow[self.C] != 0
        for move in G.dependents(self.C):
            if move in self.opened:
                continue

            new_state = State()
            new_state.S = self.S
            new_state.C = move
            new_state.opened = self.opened
            new_state.run(ticks - 1)
            if open:
                new_state.opened = self.opened | {self.C}
                new_state.run(ticks - 1)

        self.add_flow()

S = State()
S.run(30)
print(S.S)
