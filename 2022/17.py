import util
from sys import argv

F = [l.strip() for l in open(argv[1])][0]
R = [
        [[1,1,1,1]],

        [[0,1,0],
         [1,1,1],
         [0,1,0]],

        [[1,1,1],
         [0,0,1],
         [0,0,1]],

        [[1],
         [1],
         [1],
         [1]],

        [[1,1],
         [1,1]]
]

def check_collision(rock, x, y):
    h = len(rock)
    w = len(rock[0])
    if x < 0 or x+w > 7 or y == -1:
        return True

    for x2 in range(w):
        for y2 in range(h):
            if rock[y2][x2] == 1 and G[x+x2][y+y2] != 0:
                return True
    return False

def place_rock(rock, x, y):
    global G
    for y2 in range(len(rock)):
        for x2 in range(len(rock[0])):
            if rock[y2][x2] == 1:
                G[x+x2][y+y2] = rock[y2][x2]

G = util.grid2d(7, 500000, 0)
wind = 0
max_y = 0

seen = []
dropped = 0
while True:
    i = dropped % 5
    rock = R[i]
    x, y = 2, max_y + 3

    while True:
        wind_dir = 1 if F[wind%len(F)] == ">" else -1
        wind += 1
        if not check_collision(rock, x+wind_dir, y):
            x += wind_dir
        if not check_collision(rock, x, y-1):
            y -= 1
        else:
            place_rock(rock, x, y)
            max_y = max(max_y, y + len(rock))
            break

    if dropped == 2021:
        print("2021:", max_y)
    if dropped == 50000:
        break
    seen.append(max_y)
    dropped += 1

def solve_cycle(start_ticks, start_score, target_ticks, cycle_length, cycle_score):
    cycles = (target_ticks - start_ticks) // cycle_length
    rem = (target_ticks - start_ticks) % cycle_length
    start_score += cycles * cycle_score
    start_score += seen[start_ticks + rem - 1] - seen[start_ticks]

    return start_score

def find_cycle():
    start = 1000
    for period in range(10, 10000):
        good = True
        diff = seen[start+period] - seen[start]
        for r in range(1, 10):
            if seen[start+period*r] - seen[start+period*(r-1)] != diff:
                good = False
                break
        if good:
            return period, diff
    return -1, -1

# test input: increase by 53 every 35 rocks
# print(solve_cycle(1972, 2993, 1000000000000, 35, 53))

start, score = find_cycle()
print(solve_cycle(1000, seen[1000], 1000000000000, start, score))
