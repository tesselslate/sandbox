import util
from sys import argv

F = [l.strip("\n") for l in open(argv[1])][:-2]
G = util.grid(len(F), ' ')
SZ = 50

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

R = facings[0]
L = facings[2]
U = facings[3]
D = facings[1]

def left(f):
    return facings[(facings.index(f)-1)%4]

def right(f):
    return facings[(facings.index(f)+1)%4]

# we do a little hardcoding
adj = {
        (1,R): (2,R),
        (1,L): (4,R),
        (1,U): (6,R),
        (1,D): (3,D),
        (2,R): (5,L),
        (2,L): (1,L),
        (2,U): (6,U),
        (2,D): (3,L),
        (3,R): (2,U),
        (3,L): (4,D),
        (3,U): (1,U),
        (3,D): (5,D),
        (4,R): (5,R),
        (4,L): (1,R),
        (4,U): (3,R),
        (4,D): (6,D),
        (5,R): (2,L),
        (5,L): (4,L),
        (5,U): (3,U),
        (5,D): (6,L),
        (6,R): (5,U),
        (6,L): (1,D),
        (6,U): (4,U),
        (6,D): (2,D),
}

transforms = {
        (R,R): lambda r, c: (r, 0),
        (D,D): lambda r, c: (0, c),
        (L,R): lambda r, c: (SZ-1-r, 0),
        (U,R): lambda r, c: (c, 0),
        (L,L): lambda r, c: (r, SZ-1),
        (D,L): lambda r, c: (c, SZ-1),
        (R,L): lambda r, c: (SZ-1-r, SZ-1),
        (U,U): lambda r, c: (SZ-1, c),
        (R,U): lambda r, c: (SZ-1, r),
        (L,D): lambda r, c: (0, r),
}

def get_face(a, b):
    G = util.grid(SZ, '.')
    for x in range(SZ):
        for y in range(SZ):
            G[y][x] = F[y+b][x+a]
    return G

faces = [
        None,
        get_face(SZ, 0),
        get_face(2*SZ, 0),
        get_face(SZ, SZ),
        get_face(0, 2*SZ),
        get_face(SZ, 2*SZ),
        get_face(0, 3*SZ)
]

score = [
        lambda r, c : 1000*(r+1) + 4*(c+1),
        lambda r, c : score[0](r, SZ+c),
        lambda r, c : score[0](r, 2*SZ+c),
        lambda r, c : score[0](SZ+r, SZ+c),
        lambda r, c : score[0](2*SZ+r, c),
        lambda r, c : score[0](2*SZ+r, SZ+c),
        lambda r, c : score[0](3*SZ+r, c),
]

face = 1
pos = (0, 0)
facing = facings[0]

def move(face, p, f):
    new = (p[0] + f[0], p[1] + f[1])
    if new[0] < 0 or new[1] < 0 or new[0] > SZ-1 or new[1] > SZ-1:
        nf, nd = adj[(face,f)]
        nr, nc = transforms[(f,nd)](p[0],p[1])
        if faces[nf][nr][nc] == '#':
            return face, p, f
        return nf, (nr, nc), nd
    elif faces[face][new[0]][new[1]] == '#':
        return face, p, f
    return face, new, f

i = 0
while i < len(M):
    s = ""
    while i < len(M) and M[i].isdigit():
        s += M[i]
        i += 1
    for _ in range(int(s)):
        face, pos, facing = move(face, pos, facing)
    if i < len(M):
        if M[i] == 'L': facing = left(facing)
        else: facing = right(facing)
        i += 1

print(score[face](pos[0], pos[1]) + facings.index(facing))
