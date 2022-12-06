# target: 226688
import collections, util
from dataclasses import dataclass
from sys import argv

F = [l.strip() for l in open(argv[1])]
SIZE = len(F)

@dataclass(eq=True, frozen=True)
class P():
    r: int = 0
    c: int = 0

def get_adjacent(p):
    return [
            P(p.r-1,p.c),
            P(p.r,p.c-1),
            P(p.r,p.c+1),
            P(p.r+1,p.c)
    ]

def tiebreaker(p, options):
    adj = get_adjacent(p)
    for i in range(4):
        if adj[i] in options:
            return adj[i]
    raise ValueError

class Game():
    G = []
    rounds = 0

    def __init__(self, grid):
        self.G = grid

    def __str__(self):
        S = ""
        for r in range(SIZE):
            s = ""
            h = []
            for c in range(SIZE):
                e = self.G[r][c]
                if e == None:
                    s += "."
                elif e == 1:
                    s += "#"
                elif isinstance(e, Goblin):
                    if e.hp == 200:
                        s += "G"
                    else:
                        s += "g"
                    h.append(str(e.hp))
                else:
                    if e.hp == 200:
                        s += "E"
                    else:
                        s += "e"
                    h.append(str(e.hp))
            S += s + " " + ", ".join(h) + "\n"
        return S

    def adjacent_enemies(self, p: P) -> list[P]:
        O = []
        el = self.get(p)
        isgob = isinstance(el, Goblin)
        iself = not isgob
        for coords in get_adjacent(p):
            if isgob and isinstance(self.get(coords), Elf):
                O.append(coords)
            elif iself and isinstance(self.get(coords), Goblin):
                O.append(coords)
        return O

    def any_enemies(self, p: P) -> list[P]:
        O = []
        goblin = isinstance(self.get(p), Goblin)
        for r in range(SIZE):
            for c in range(SIZE):
                if goblin and isinstance(self.G[r][c], Elf):
                    O.append(P(r,c))
                elif not goblin and isinstance(self.G[r][c], Goblin):
                    O.append(P(r,c))
        return O

    def attack(self, p: P) -> bool:
        # check for any adjacent enemies
        adjacent = self.adjacent_enemies(p)
        if adjacent:
            # attack the most vulnerable adjacent enemy,
            # then let the next unit have their turn
            self.drain_health(self.most_vulnerable(p, adjacent))
            return True
        return False

    def drain_health(self, p: P):
        self.get(p).hp -= 3
        if self.get(p).hp <= 0:
            self.set(p, None)

    def floodfill(self, p: P):
        def add_element(r, c, v):
            if self.G[r][c] != None:
                return
            if not FF[r][c]:
                FF[r][c] = v
                Q.append((r, c, v))

        # start at the given point.
        # floodfill outwards in each direction, increasing the value
        # by 1 each time.
        FF = util.grid(SIZE, None)
        Q = collections.deque([(p.r, p.c, 0)])
        while len(Q) > 0:
            E = Q.popleft()
            add_element(E[0]+1, E[1], E[2]+1)
            add_element(E[0]-1, E[1], E[2]+1)
            add_element(E[0], E[1]+1, E[2]+1)
            add_element(E[0], E[1]-1, E[2]+1)
            FF[E[0]][E[1]] = E[2] # type: ignore
        return FF # type: ignore

    def outcome(self) -> int:
        S = 0
        for r in range(SIZE):
            for c in range(SIZE):
                el = self.G[r][c]
                if isinstance(el, Elf):
                    S += el.hp
                elif isinstance(el, Goblin):
                    S += el.hp
        S *= self.rounds
        return S

    def most_vulnerable(self, player: P, enemies: list[P]) -> P:
        hp = { p:self.get(p).hp for p in enemies }
        m = min(hp.values())
        s = [p for (p,v) in hp.items() if v == m]
        if len(s) == 1:
            return s[0]
        return tiebreaker(player, s)

    def get(self, p: P):
        return self.G[p.r][p.c]

    def set(self, p: P, v):
        self.G[p.r][p.c] = v

    def run(self):
        while True:
            if self.tick():
                return
            else:
                self.rounds += 1

    def tick(self):
        for r in range(SIZE):
            for c in range(SIZE):
                #! identify enemies
                  #! if none left, end (return TRUE to signify done)
                #! if in range of a target:
                  #! attack. choose the adjacent enemy with the lowest hp
                  #! if there are multiple enemies with "the" lowest hp, first
                  #! in reading order
                  #! subtract 3 hp, if <= 0, remove enemy (set grid to none)
                #! if no open squares in range of any enemy, next unit
                #! OPEN SQUARE NEXT TO ENEMY:
                  #! find reachable squares in range of an enemy (not blocked
                  #! by other units). if none, next unit
                  #! find nearest reachable square
                  # take one step to nearest reachable square based on reading order
                    # prioritize up, then right

                # return if this space is not occupied by a unit
                point = P(r, c)
                el = self.get(point)
                if not isinstance(el, Elf) and not isinstance(el, Goblin):
                    continue
                if el.moved:
                    continue

                # check for any enemies at all.
                # if there are none left, end the turn early. the game is over
                enemies = self.any_enemies(point)
                if len(enemies) == 0:
                    return True

                adj = self.adjacent_enemies(point)
                if len(adj) == 0: # move if no adjacent enemies
                    # find the set of all spots within range of an enemy
                    in_range_spots = set()
                    for enemy in enemies:
                        for spot in get_adjacent(enemy):
                            if self.get(spot) == None:
                                in_range_spots.add(spot)

                    # if there are no inrange spots, next unit
                    if len(in_range_spots) == 0:
                        continue

                    # determine which steps are reachable and in how many
                    # steps with a floodfill
                    reachables = {}
                    FF = self.floodfill(point)
                    for spot in in_range_spots:
                        v = FF[spot.r][spot.c]
                        if v != None:
                            reachables[spot] = v

                    # if no spots are reachable, continue
                    if len(reachables) == 0:
                        continue

                    # pick the spot which is closest
                    m = min(reachables.values())
                    spots = [p for p, v in reachables.items() if v == m]
                    spot = None
                    if len(spots) == 1:
                        spot = spots[0]
                    else:
                        spot = min(spots, key=lambda n : (n.r, n.c))

                    # traverse back through the floodfill grid to find which step
                    # to take.
                    # perform another floodfill going back from the destination and
                    # then pick the square adjacent to the unit with the lowest value
                    # and sorted by reading order.
                    FF2 = self.floodfill(spot)
                    dirs = get_adjacent(point)
                    prios = [FF2[a.r][a.c] for a in dirs]
                    m = 10000
                    for v in prios:
                        if v != None and v < m:
                            m = v
                    s = [p for p in dirs if FF2[p.r][p.c] == m]
                    step = tiebreaker(point, s)

                    # now that we've determined the best step, take it.
                    self.G[step.r][step.c] = el
                    self.set(point, None)
                    el.moved = True
                    point = step
                self.attack(point)

        for r in range(SIZE):
            for c in range(SIZE):
                el = self.G[r][c]
                if not isinstance(el, Goblin) and not isinstance(el, Elf):
                    continue
                self.G[r][c].moved = False
        return False

class Goblin():
    hp = 200
    moved = False

class Elf():
    hp = 200
    moved = False

grid = util.grid(SIZE)
for r in range(SIZE):
    for c in range(SIZE):
        e = F[r][c]
        if e == "G":
            grid[r][c] = Goblin() # type: ignore
        elif e == "E":
            grid[r][c] = Elf() # type: ignore
        elif e == "#":
            grid[r][c] = 1 # type: ignore
        else:
            grid[r][c] = None

G = Game(grid)
G.run()
print(G.outcome())
print(G)

# CHECK ORDERS:
# - 1,2,3,4
# - 1,2,4,3
# - 1,3,2,4
# - 3,1,2,4
