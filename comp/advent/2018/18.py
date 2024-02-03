import util
from sys import argv

F = [l.strip() for l in open(argv[1])]
SIZE = 50

G = util.grid(SIZE, '.')
for i in range(SIZE):
    for j in range(SIZE):
        G[i][j] = F[i][j]

def adj_count(x, y, v):
    global G, SIZE
    pos = [
        (x-1,y-1),
        (x-1,y),
        (x-1,y+1),
        (x+1,y-1),
        (x+1,y),
        (x+1,y+1),
        (x,y-1),
        (x,y+1),
    ]
    s = 0
    for p in pos:
        x, y = p[0], p[1]
        if x >= 0 and x < SIZE and y >= 0 and y < SIZE:
            if G[x][y] == v:
                s += 1
    return s

I = 1000000000
for i in range(I):
    NG = util.grid(SIZE, '0')
    w = 0
    l = 0
    for x in range(SIZE):
        for y in range(SIZE):
            if G[x][y] == '.':
                if adj_count(x, y, '|') >= 3:
                    NG[x][y] = '|'
                    w += 1
                else:
                    NG[x][y] = '.'
            elif G[x][y] == '|':
                if adj_count(x, y, '#') >= 3:
                    NG[x][y] = '#'
                    l += 1
                else:
                    NG[x][y] = '|'
                    w += 1
            elif G[x][y] == '#':
                if adj_count(x, y, '#') >= 1 and adj_count(x, y, '|') >= 1:
                    NG[x][y] = '#'
                    l += 1
                else:
                    NG[x][y] = '.'
    G = NG

    v = w*l
    print(i, ":", v, w, l)
