import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip("\n") for l in open(argv[1])]

H = '-'
V = '|'

carts = []

fg = util.grid(150)
for i in range(len(F)):
    for j in range(len(F[i])):
        c = F[i][j]
        if not c in ['^', 'v', '<', '>']:
            fg[i][j] = c # type: ignore
        else:
            carts.append((i,j,c,0))
            if c in ['^', 'v']:
                fg[i][j] = V # type: ignore
            else:
                fg[i][j] = H # type: ignore

# i had this for debugging but it's cool so i'll leave it in
def print_tracks():
    global fg, carts
    for i in range(len(F)):
        s = ""
        for j in range(len(F[i])):
            cart = False
            for c in carts:
                if c[0] == i and c[1] == j:
                    s += c[2]
                    cart = True
                    break
            if not cart:
                s += fg[i][j] # type: ignore
        print(s)

d = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
}

c = {
    '\\': {
        '>': 'v',
        '^': '<',
        '<': '^',
        'v': '>',
    },
    '/': {
        '>': '^',
        'v': '<',
        '^': '>',
        '<': 'v',
    },
}

dirs = '<v>^'

def run(crash):
    global c, d, fg, carts
    while True:
        # sort by (y, x)
        carts.sort(key = lambda c : c[0] * 10000 + c[1])
        for i in range(len(carts)):
            cart = carts[i]
            track = fg[cart[0]][cart[1]]
            dir = cart[2]
            turn = cart[3]
            if track == '\\' or track == '/':
                dir = c[track][cart[2]] # type: ignore
            elif track == '+':
                if turn == 0:
                    dir = dirs[(dirs.index(dir)+1)%4]
                elif turn == 1:
                    dir = cart[2]
                elif turn == 2:
                    dir = dirs[(dirs.index(dir)-1)%4]
                turn = (turn+1)%3
            else:
                dir = cart[2]
            m = d[dir]
            carts[i] = (cart[0] + m[0], cart[1] + m[1], dir, turn)
            for j in range(len(carts)):
                if i == j:
                    continue
                if carts[i][0] == carts[j][0] and carts[i][1] == carts[j][1]:
                    if crash:
                        print(carts[i][1], carts[i][0])
                        return
                    # TODO: remove
run(False)
#run(True)
