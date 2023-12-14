import ul

F = ul.input()
G = ul.grid(F)
dirs = ul.dirs_rc("NWSE")

def tilt(d=(-1,0)):
    while True:
        n = 0
        for (r,c) in ul.gridpoints(G):
            if G[r][c] != "O": continue
            rr = r + d[0]
            cc = c + d[1]
            if ul.gridcheck(G, rr, cc) and G[rr][cc] == ".":
                G[rr][cc] = "O"
                G[r][c] = "."
                n += 1
        if n == 0:
            return

tilt()
print(sum(len(G)-r for (r,c) in ul.gridpoints(G) if G[r][c] == "O"))

G = ul.grid(F)
p = ul.periodic()
while not p.has_cycle():
    for d in dirs:
        tilt(d)
    v = frozenset((r,c) for (r,c) in ul.gridpoints(G) if G[r][c] == "O")
    p.append(v)
print(sum(len(G)-r for (r,c) in p[10**9]))
