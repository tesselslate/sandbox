import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

SIZE = 7
F = [l.strip() for l in open(argv[1])]
grid = util.grid(SIZE)

def first_in_order(pairs):
    pairs.sort()
    return pairs[0]

class Game():
    G = []
    rounds = 0

    def __init__(self, grid):
        self.G = grid

    def __str__(self):
        S = ""
        for r in range(SIZE):
            s = ""
            for c in range(SIZE):
                e = self.G[r][c]
                if e == None:
                    s += "."
                elif e == 1:
                    s += "#"
                elif isinstance(e, Goblin):
                    s += "G"
                else:
                    s += "E"
            S += s + "\n"
        return S

    def adjacent_enemies(self, r, c):
        O = []
        el = self.G[r][c]
        goblin = isinstance(el, Goblin)
        check = [
                (r+1,c),
                (r-1,c),
                (r,c+1),
                (r,c-1),
        ]
        for coords in check:
            if coords[0] >= 0 and coords[0] < SIZE and coords[1] >= 0 and coords[1] < SIZE:
                if goblin and isinstance(self.G[coords[0]][coords[1]], Elf):
                    O.append(coords)
                elif not goblin and isinstance(self.G[coords[0]][coords[1]], Goblin):
                    O.append(coords)
        if len(O) == 0:
            return None
        return O

    def adjacent_spots(self, r, c):
        O = []
        check = [
                (r+1,c),
                (r-1,c),
                (r,c+1),
                (r,c-1),
        ]
        for coords in check:
            if coords[0] >= 0 and coords[0] < SIZE and coords[1] >= 0 and coords[1] < SIZE:
                if self.G[coords[0]][coords[1]] == None:
                    O.append(coords)
        return O

    def any_enemies(self, r, c):
        O = []
        goblin = isinstance(self.G[r][c], Goblin)
        for r in range(SIZE):
            for c in range(SIZE):
                if goblin and isinstance(self.G[r][c], Elf):
                    O.append((r,c))
                elif not goblin and isinstance(self.G[r][c], Goblin):
                    O.append((r,c))
        if len(O) == 0:
            return None
        return O

    def attack(self, r, c):
        self.G[r][c].hp -= 3
        if self.G[r][c].hp <= 0:
            self.G[r][c] = None

    def floodfill(self, r, c):
        def add_element(r, c, v):
            if self.G[r][c] != None:
                return
            if not FF[r][c] or FF[r][c] > v:
                FF[r][c] = v
                Q.append((r, c, v))

        # start at the given point.
        # floodfill outwards in each direction, increasing the value
        # by 1 each time.
        FF = util.grid(SIZE, None)
        Q = [(r, c, 0)]
        while len(Q) > 0:
            E = Q.pop()
            add_element(E[0]+1, E[1], E[2]+1)
            add_element(E[0]-1, E[1], E[2]+1)
            add_element(E[0], E[1]+1, E[2]+1)
            add_element(E[0], E[1]-1, E[2]+1)
            FF[E[0]][E[1]] = E[2] # type: ignore
        return FF

    def outcome(self):
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

    def most_vulnerable(self, enemies):
        enemies.sort(key = lambda e : (self.G[e[0]][e[1]].hp, e[0], e[1]))
        return enemies[0]

    def run(self):
        while True:
            if self.tick(): # over
                return
            else:
                self.rounds += 1
            print("tick", self.rounds)
            print(self, "\n\n")

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
                el = self.G[r][c]
                if not isinstance(el, Elf) and not isinstance(el, Goblin):
                    continue

                # check for any enemies at all.
                # if there are none left, end the turn early. the game is over
                enemies = self.any_enemies(r, c)
                if not enemies:
                    return True
                
                # check for any adjacent enemies
                adjacent = self.adjacent_enemies(r, c)
                if adjacent:
                    # attack the most vulnerable adjacent enemy,
                    # then let the next unit have their turn
                    vuln = self.most_vulnerable(adjacent)
                    self.attack(vuln[0], vuln[1])
                    continue

                # find the set of all spots within range of an enemy
                in_range_spots = set()
                for enemy in enemies:
                    for spot in self.adjacent_spots(enemy[0], enemy[1]):
                        in_range_spots.add(spot)

                # if there are no inrange spots, next unit
                if len(in_range_spots) == 0:
                    continue

                # determine which steps are reachable and in how many
                # steps with a floodfill
                reachables = {}
                FF = self.floodfill(r, c)
                for spot in in_range_spots:
                    v = FF[spot[0]][spot[1]]
                    if v:
                        reachables[spot] = v

                # if no spots are reachable, continue
                if len(reachables) == 0:
                    continue

                # pick the spot which is closest
                spot = min(reachables, key=reachables.get) # type: ignore

                # traverse back through the floodfill grid to find which step
                # to take.
                # perform another floodfill going back from the destination and
                # then pick the square adjacent to the unit with the lowest value
                # and sorted by reading order.
                FF2 = self.floodfill(spot[0], spot[1])
                dirs = [
                    (r+1,c),
                    (r,c-1),
                    (r,c+1),
                    (r-1,c)
                ]
                prios = [FF2[a[0]][a[1]] for a in dirs]
                m = (None, 10000)
                for i, p in enumerate(prios):
                    if p != None and p < m[1]:
                        print("d")
                        m = (i, p)
                step = dirs[m[0]] # type: ignore

                # now that we've determined the best step, take it.
                self.G[step[0]][step[1]] = el
                self.G[r][c] = None

        return False

class Goblin():
    hp = 200

class Elf():
    hp = 200

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
