import collections, util
from dataclasses import dataclass
from sys import argv

F = [l.strip() for l in open(argv[1])]
SIZE = len(F)

ELF = 0
GOB = 1

@dataclass(eq = True, frozen = True)
class P:
    r: int = 0
    c: int = 0

    def __add__(self, p):
        return P(self.r + p[0], self.c + p[1])

class Unit:
    p: P
    typ: int = -1
    hp: int = 200
    alive: bool = True

    def __init__(self, a, p: P, b=200, c=True):
        self.p = p
        self.typ = a
        self.hp = b
        self.alive = c

def adjacent(p: P) -> list[P]:
    return [
            p + (-1,0),
            p + (0,-1),
            p + (0,1),
            p + (1,0),
    ]

def reading_order(ps) -> list[P]:
    return sorted(ps, key=lambda x : (x.r, x.c))

class Game:
    G = []
    U: list[Unit] = []
    rounds = 0

    def __init__(self, g, u):
        self.G = g
        self.U = u

    def print(self):
        us = sorted(self.U, key=lambda x : (x.p.r, x.p.c))
        for i, y in enumerate(self.G):
            s = ""
            for j, x in enumerate(y):
                v = self.unit_at(P(i, j))
                if v and v.alive:
                    s += "G" if v.typ == GOB else "E"
                else:
                    s += "#" if x == 1 else "."
            s += " "
            for u in us:
                if u.alive and u.p.r == i:
                    s += "E |" if u.typ == 0 else "G |"
                    s += str(u.hp) + "| "
            print(s)

    def run(self):
        self.rounds = 0
        while self.tick() and self.rounds < 27:
            self.rounds +=1
            if self.rounds > 22:
                print(self.rounds)
                self.print()
        return self.rounds

    def outcome(self):
        S = 0
        for unit in self.U:
            if unit.alive:
                S += unit.hp
        return S * self.rounds

    def tick(self):
        units = sorted(self.U, key=lambda x : (x.p.r, x.p.c))
        for unit in units:
            pos = unit.p
            if not unit.alive:
                continue

            # end if there are no enemies
            all_enemies = self.all_enemies(unit)
            if len(all_enemies) == 0:
                return False

            # attack if in range
            adj = self.adj_enemies(unit)
            if len(adj) != 0:
                self.attack(adj)
                continue

            # not in range. move
            # start by creating a flat list of all spots adjacent
            # to enemies
            adj = [adjacent(p) for p in all_enemies]
            adj = [x for s in adj for x in s]

            # prune the list to just empty spots. end if there are none
            adj = [x for x in adj if self.G[x.r][x.c] == 0 and not self.unit_at(x)]
            if len(adj) == 0:
                continue

            # do bfs. get rid of all unreachable in-range positions, aka those
            # which were not reached by the bfs. if any remain, find the closest.
            bfs = self.floodfill(pos)
            adj = [x for x in adj if bfs[x.r][x.c] >= 0]
            if len(adj) == 0:
                continue
            closest = min(adj, key=lambda x : (bfs[x.r][x.c], x.r, x.c))

            # best spot found: do bfs again from the chosen spot to figure out
            # which direction to move.
            # - create a list of possible directions to move in
            # - if there are no possible moves, return
            # - find the best move (lowest distance, then reading order)
            # - move there
            bfs = self.floodfill(closest)
            possible_moves = [x for x in adjacent(pos) if self.G[x.r][x.c] == 0 and not self.unit_at(x) and bfs[x.r][x.c] >= 0]
            if len(possible_moves) == 0:
                continue
            best_move = min(possible_moves, key=lambda x : (bfs[x.r][x.c], x.r, x.c))

            unit.p = best_move

            # try to attack again after moving
            adj = self.adj_enemies(unit)
            if len(adj) != 0:
                self.attack(adj)

        return True

    def adj_enemies(self, unit: Unit) -> list[Unit]:
        O = []
        adjs = adjacent(unit.p)
        for adj in adjs:
            v = self.unit_at(adj)
            if v and v.typ != unit.typ and v.alive:
                O.append(v)
        return O

    def all_enemies(self, unit: Unit) -> list[P]:
        O = []
        for u in self.U:
            if u != unit and u.alive and u.typ != unit.typ:
                O.append(u.p)
        return O

    def attack(self, enemies: list[Unit]):
        enemy = sorted(enemies, key=lambda x : (x.hp, x.p.r, x.p.c))[0]
        enemy.hp -= 3
        if enemy.hp <= 0:
            enemy.alive = False

    def floodfill(self, pos: P):
        F = util.grid(SIZE, -1)
        Q = collections.deque([(pos, 0)])
        F[pos.r][pos.c] = 0

        def add(pos: P, val):
            if F[pos.r][pos.c] >= 0 or self.G[pos.r][pos.c] == 1 or self.unit_at(pos):
                return
            F[pos.r][pos.c] = val
            Q.append((pos, val))

        while len(Q) > 0:
            E = Q.popleft()
            add(E[0] + (-1, 0), E[1] + 1)
            add(E[0] + (0, -1), E[1] + 1)
            add(E[0] + (0, 1), E[1] + 1)
            add(E[0] + (1, 0), E[1] + 1)

        return F

    def unit_at(self, pos: P) -> Unit:
        for i in self.U:
            if i.p == pos:
                return i
        return None # type: ignore

grid = util.grid(SIZE, 0)
units = []
for r in range(SIZE):
    for c in range(SIZE):
        e = F[r][c]
        if e == "G":
            units.append(Unit(GOB, P(r,c)))
        elif e == "E":
            units.append(Unit(ELF, P(r,c)))
        elif e == "#":
            grid[r][c] = 1 

G = Game(grid, units)
G.run()
print(G.outcome())
