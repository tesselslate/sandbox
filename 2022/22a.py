import util
from sys import argv

F = [l.strip("\n") for l in open(argv[1])][:-2]
G = util.grid(200, ' ')

for r in range(len(F)):
    for c in range(len(F[r])):
        G[r][c] = F[r][c]

M = [l.strip() for l in open(argv[1])][-1]

facings = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
]

def left(f):
    return facings[(facings.index(f)-1)%4]

def right(f):
    return facings[(facings.index(f)+1)%4]

def move(p, f):
    new = (p[0] + f[0], p[1] + f[1])
    if new[0] < 0 or new[1] < 0 or new[0] > len(F) - 1 or new[1] > len(F[new[0]]) - 1 or G[new[0]][new[1]] == ' ':
        r, c = new
        if f[0] == 1:
            r = 0
        elif f[0] == -1:
            r = len(F) - 1
        elif f[1] == 1:
            c = 0
        elif f[1] == -1:
            c = len(F[r]) - 1
        while G[r][c] == ' ':
            r += f[0]
            c += f[1]
        return p if G[r][c] == '#' else (r, c), f
    elif G[new[0]][new[1]] == '.':
        return new, f
    return p, f

pos = (0, G[0].index('.'))
facing = facings[0]

i = 0
while i < len(M):
    s = ""
    while i < len(M) and M[i].isdigit():
        s += M[i]
        i += 1
    for _ in range(int(s)):
        pos, facing = move(pos, facing)
    if i < len(M):
        if M[i] == 'L': facing = left(facing)
        else: facing = right(facing)
        i += 1

print(pos[0]*1000 + pos[1]*4 + facings.index(facing) + 1004)
