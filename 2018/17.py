import util
from sys import argv

PADDING = 10
F = [l.strip() for l in open(argv[1])]

C = set()

for l in F:
    a, b = l.replace(",", "").split(" ")
    rc = b[0]
    x1, x2, y1, y2 = 0, 0, 0, 0
    if rc == 'x':
        y = int(a[2:])
        y1, y2 = y, y
        x1, x2 = util.scan("x=%d..%d", b)
    else:
        x = int(a[2:])
        x1, x2 = x, x
        y1, y2 = util.scan("y=%d..%d", b)

    for x in util.irange(x1, x2):
        for y in util.irange(y1, y2):
            C.add((x, y))

MIN_X = min(C, key=lambda x : x[0])[0]
MIN_Y = min(C, key=lambda x : x[1])[1]
MAX_X = max(C, key=lambda x : x[0])[0]
MAX_Y = max(C, key=lambda x : x[1])[1]
XSIZE = MAX_X - MIN_X + PADDING * 2 + 1
YSIZE = MAX_Y + 2
G = util.grid2d(XSIZE, YSIZE, '.')

for c in C:
    G[c[0]-MIN_X+PADDING][c[1]] = '#'

def print_grid(grid):
    for x in range(YSIZE):
        s = ""
        for y in range(XSIZE):
            s += grid[y][x]
        print(s)

R = set()
R.add((500-MIN_X+PADDING, MIN_Y))

useless = 0
while useless < 10:
    l = len(R)

    G[500-MIN_X+PADDING][MIN_Y] = '|'
    for x in range(XSIZE):
        for y in range(YSIZE):
            if G[x][y] != '|' or y == YSIZE - 2:
                continue

            if G[x][y+1] == '.':
                R.add((x, y+1))
                G[x][y+1] = '|'
            elif G[x][y+1] == '~' or G[x][y+1] == '#':
                lb, rb = 0, XSIZE - 2
                ld, rd = False, False

                for i in range(x, 0, -1):
                    if G[i][y+1] == '.' or G[i][y+1] == '|':
                        lb, ld = i, True
                        break
                    if G[i][y] == '#':
                        lb = i
                        break
                for i in range(x, XSIZE - 1):
                    if G[i][y+1] == '.' or G[i][y+1] == '|':
                        rb, rd = i, True
                        break
                    if G[i][y] == '#':
                        rb = i
                        break
                lb = lb if ld else lb + 1
                rb = rb if rd else rb - 1
                for j in util.irange(lb, rb):
                    R.add((j,y))
                    G[j][y] = '|' if ld or rd else '~'

    if l == len(R):
        useless += 1
        continue
    useless = 0
print(len(R))

S = 0
for i in G:
    for j in i:
        if j == '~':
            S += 1
print(S)
