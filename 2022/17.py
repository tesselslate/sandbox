import itertools, ul

F = ul.input()[0]

wind = itertools.cycle(F)
rocks = [ul.grid(G) for G in ul.double_linefeed("""
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
""".split("\n"))[1:-1]]

G = set((0, c) for c in range(7))
M = 0

def collide(rock, r, c):
    if c < 0 or r == 0: return True
    for rr in range(len(rock)):
        for cc in range(len(rock[0])):
            t = rock[rr][cc] == "#"
            if r+rr >= 0 or c+cc >= 7: return True
            if t and (r+rr, c+cc) in G: return True
    return False

p = ul.periodic()
h = []
for i in itertools.count():
    rock = rocks[i % len(rocks)]
    r = M - 3 - len(rock)
    c = 2

    while (w := next(wind)):
        w = -1 if w == "<" else 1
        if not collide(rock, r, c+w):
            c += w
        if collide(rock, r+1, c):
            for rr in range(len(rock)):
                for cc in range(len(rock[0])):
                    if rock[rr][cc] == "#": G.add((r+rr,c+cc))
            break
        r += 1

    M = min(r, M)
    p.append(frozenset((r-M,c) for r in range(M, M+40) for c in range(7) if (r,c) in G))
    h.append(M+len(rock)-1)
    if i == 2022: print(abs(M+len(rock)-1))
    if i >= 2022 and p.has_cycle(): break

N = 1000000000000
s, l = p.cycle_start, p.cycle_len
ncycles = (N-s) // l
off = (N-s) % l
print(abs(h[s] + ncycles*(h[s+l]-h[s]) + (h[s+off]-h[s]) + 1))
