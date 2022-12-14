import util
from sys import argv

F = [l.strip() for l in open(argv[1])]

walls = []
for l in F:
    s = None
    words = l.split(" ")
    for i in range(0, len(words), 2):
        x, y = util.scan("%d,%d", words[i])
        if s == None:
            s = (x,y)
            continue
        walls.append((s, (x,y)))
        s = (x,y)
p = []
for w in walls:
    p += [w[0], w[1]]

PADDING = 200
MIN_X = min(p, key=lambda x : x[0])[0]
MAX_X = max(p, key=lambda x : x[0])[0]
MAX_Y = max(p, key=lambda x : x[1])[1]
XSIZE = MAX_X - MIN_X + PADDING * 2
YSIZE = MAX_Y + 3
G = util.grid2d(YSIZE, XSIZE, '.')
for w in walls:
    for r in util.irange(w[0][0], w[1][0]):
        for c in util.irange(w[0][1], w[1][1]):
            G[c][r-MIN_X-PADDING] = '#'

def settle(r,c):
    global G

    if G[r][c] == "o":
        return False
    while r < YSIZE and G[r][c] == '.':
        r += 1
    if r == YSIZE:
        return False

    if G[r][c] == '#' or G[r][c] == 'o':
        if G[r][c-1] == '.':
            return settle(r,c-1)
        elif G[r][c+1] == '.':
            return settle(r,c+1)
        else:
            G[r-1][c] = 'o'
            return True
    return False

while settle(0, 500-MIN_X-PADDING):
    pass
S = 0
for x in G:
    for y in x:
        if y == 'o': S += 1
print(S)

G = util.grid2d(YSIZE, XSIZE, '.')
for w in walls:
    for r in util.irange(w[0][0], w[1][0]):
        for c in util.irange(w[0][1], w[1][1]):
            G[c][r-MIN_X-PADDING] = '#'
for i in range(XSIZE):
    G[YSIZE-1][i] = '#'
while settle(0, 500-MIN_X-PADDING):
    pass
S = 0
for x in G:
    for y in x:
        if y == 'o': S += 1
print(S)
