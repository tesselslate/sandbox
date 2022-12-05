import util
from sys import argv

F = [l.strip() for l in open(argv[1])]
S = 0

points = []

for l in F:
    a, b, c, d = util.scan("position=<%d, %d> velocity=<%d, %d>", l)
    points.append((a,b,c,d))

def tick(steps):
    global points
    global S
    S += steps
    for i in range(len(points)):
        p = points[i]
        x, y = p[0] + p[2] * steps, p[1] + p[3] * steps
        points[i] = (x,y,p[2],p[3])

last = 1
while True:
    ax, ay = 0, 0
    for p in points:
        ax += p[0]
        ay += p[1]
    ax //= len(points)
    ay //= len(points)
    i = input().strip()
    steps = last
    XOFF = 100
    YOFF = 100
    if i == "a":
        XOFF, YOFF = ax, ay
    elif i == "u":
        YOFF -= 10
    elif i == "d":
        YOFF += 10
    elif i == "l":
        XOFF -= 10
    elif i == "r":
        XOFF += 10
    elif i != "":
        steps = int(i)
        last = steps
    print("\nsteps:", S, ax, ay, XOFF, YOFF)

    tick(steps)
    SIZE = 120
    grid = util.grid(SIZE, " ")
    for p in points:
        if 0 <= p[0]-YOFF < SIZE and 0 <= p[1]-XOFF < SIZE:
            grid[p[1]-XOFF][p[0]-YOFF] = "O"
    util.print_grid(grid)
