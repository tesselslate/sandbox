import collections, util
from dataclasses import dataclass
from sys import argv

F = [l.strip() for l in open(argv[1])]

# data
@dataclass(eq = True, frozen = True, order = True)
class P():
    r: int = 0
    c: int = 0

    def __add__(self, x):
        return P(self.r + x[0], self.c + x[1])

    def adj(self):
        return [self+(-1,0), self+(0,-1), self+(0,1), self+(1,0)]

GOB = 0
ELF = 1
class Unit():
    atk: int = 3
    typ: int = 0
    hp: int = 200
    alive: bool = True

    def __init__(self, typ, atk=3):
        self.atk = atk
        self.typ = typ

# parse input
SIZE = len(F)
U: dict[P, Unit]
G = util.grid(SIZE, 0)

def parse(atk=3):
    global F, G, U, SIZE
    U = {}

    for i, l in enumerate(F):
        for j, c in enumerate(l):
            if c == '#':
                G[i][j] = 1
            elif c == 'E':
                U[P(i,j)] = Unit(ELF, atk)
            elif c == 'G':
                U[P(i,j)] = Unit(GOB, 3)

# functions
def print_state():
    print("\n\nRounds:", rounds + 1)
    for r in range(SIZE):
        s = ""
        units = []
        for c in range(SIZE):
            if G[r][c] == 1:
                s += "#"
                continue
            p = P(r,c)
            if p in U and U[p].alive:
                units.append(U[p])
                s += "E" if U[p].typ == ELF else "G"
            else:
                s += "."
        s += " "
        for u in units:
            t = "E" if u.typ == ELF else "G"
            s += f"{t}({u.hp}) "
        print(s)

def point_at(pos: P):
    if pos in U and U[pos].alive:
        return U[pos]

def attack(pos: P, elf_death: bool) -> bool:
    unit = U[pos]

    # check if there are any enemies in range
    in_range = [p for p in pos.adj() if point_at(p) and point_at(p).typ != unit.typ] # type: ignore
    
    # if there are, then attack and end the turn
    if len(in_range) > 0:
        in_range.sort(key=lambda x : (U[x].hp, x))
        u = U[in_range[0]]
        u.hp -= unit.atk
        if u.hp <= 0:
            if elf_death and u.typ == ELF:
                raise ValueError
            u.alive = False
        return True
    return False

def bfs(p: P):
    F = util.grid(SIZE, -1)
    F[p.r][p.c] = 0
    Q = collections.deque([(p, 0)])

    def add(pos: P, val: int):
        if F[pos.r][pos.c] >= 0 or G[pos.r][pos.c] or point_at(pos):
            return
        F[pos.r][pos.c] = val
        Q.append((pos, val)) # type: ignore

    while len(Q) > 0:
        E = Q.popleft()
        for p in E[0].adj():
            add(p, E[1]+1)
    return F

def score():
    S = 0
    for u in U.values():
        if u.alive:
            S += u.hp
    return S * rounds

def tick(elf_death):
    # do each unit's turn in reading order (T->B, L->R)
    for pos, unit in sorted(U.items(), key=lambda x : x[0]):
        if not unit.alive:
            continue

        # check if there are any enemies remaining
        enemies = [p for p in U if U[p].alive and U[p].typ != unit.typ]
        if not enemies:
            return False

        # try to attack
        if attack(pos, elf_death):
            continue

        # if there are not, move and then try attacking again
        # start by finding open squares adjacent to enemies
        in_range = []
        for e in enemies:
            in_range += [p for p in e.adj() if not G[p.r][p.c] and not point_at(p)]

        # use BFS to prune all unreachable squares, and then find the closest
        # by reading order. after this, we will have our target spot.
        distance = bfs(pos)
        in_range = [p for p in in_range if distance[p.r][p.c] >= 0]
        if len(in_range) == 0:
            continue
        best_spot = min(in_range, key=lambda x : (distance[x.r][x.c], x.r, x.c))

        # figure out which direction to go by doing BFS from the target square
        distance = bfs(best_spot)
        possible_moves = [p for p in pos.adj() if not point_at(p) and not G[p.r][p.c] and distance[p.r][p.c] >= 0]
        if len(possible_moves) == 0:
            continue
        best_move = min(possible_moves, key=lambda x : (distance[x.r][x.c], x.r, x.c))
    
        # move
        del U[pos]
        U[best_move] = unit

        # try to attack again after moving
        attack(best_move, elf_death)

    return True

# run game
rounds = 0

parse()
while tick(False):
    rounds += 1
print(rounds)
print(score())

for atk in range(4,1000):
    parse(atk)
    try:
        rounds = 0
        while tick(True):
            rounds += 1
        print(atk)
        print(score())
        break
    except:
        print("fail", atk)
