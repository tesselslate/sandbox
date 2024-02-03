import itertools, ul

F = ul.input()
G = ul.grid(F)

RR = {r for r in range(len(G)) if G[r].count(".") == len(G[r])}
CC = {c for c in range(len(G)) if ul.gcol(G, c).count(".") == len(G)}

galaxies = [(r,c) for (r,c) in ul.gridpoints(G) if G[r][c] == "#"]

def find(mult):
    S = 0
    for (a, b) in itertools.product(galaxies, repeat=2):
        er = len(set(range(*ul.minmax(a[0], b[0]))) & RR)
        ec = len(set(range(*ul.minmax(a[1], b[1]))) & CC)
        S += abs(a[0]-b[0]) + abs(a[1]-b[1]) + (er + ec) * (mult - 1)
    return S // 2
print(find(2))
print(find(1000000))
