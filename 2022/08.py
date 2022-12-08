import util
from sys import argv

F = [l.strip() for l in open(argv[1])]
S = 0

SIZE = len(F)

G = util.grid(SIZE, 0)

for i in range(SIZE):
    for j in range(SIZE):
        G[i][j] = int(F[i][j])

for i in range(SIZE):
    for j in range(SIZE):
        if i == 0 or i == SIZE-1 or j == 0 or j == SIZE-1:
            S += 1
        elif max([G[x][j] for x in range(0, i)]) < G[i][j]:
            S += 1
        elif max([G[x][j] for x in range(i+1, SIZE)]) < G[i][j]:
            S += 1
        elif max([G[i][x] for x in range(0, j)]) < G[i][j]:
            S += 1
        elif max([G[i][x] for x in range(j+1,SIZE)]) < G[i][j]:
            S += 1
print(S)

def view(v, it):
    global G
    s = 0
    for i in it:
        s += 1
        if G[i[0]][i[1]] >= v:
            break
    return s

S = 0
for i in range(1,SIZE-1):
    for j in range(1,SIZE-1):
        v = G[i][j]

        s = 1
        s *= view(v, reversed([(x,j) for x in range(0,i)]))
        s *= view(v, [(x,j) for x in range(i+1,SIZE)])
        s *= view(v, reversed([(i,x) for x in range(0,j)]))
        s *= view(v, [(i,x) for x in range(j+1,SIZE)])
        S = max(s, S)
print(S)
