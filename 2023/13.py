import sys, ul

F = ul.input()
G = [ul.grid(g) for g in ul.double_linefeed(F)]

def ndiff(g, r):
    x = min(r, len(g)-r)
    return sum(sum(g[r-rr-1][c] != g[r+rr][c] for c in range(len(g[0]))) for rr in range(x))

def diffs(g):
    return [ndiff(g, i) for i in range(1, len(g))]

def value(diffs, vert, smudges):
    i = diffs.index(smudges) + 1 if smudges in diffs else 0
    return i * (100 if vert else 1)

S = 0
S2 = 0
for g in G:
    a = diffs(g)
    b = diffs(ul.transpose(g))
    if (v := value(a, True, 0)) or (v := value(b, False, 0)): S += v
    if (v := value(a, True, 1)) or (v := value(b, False, 1)): S2 += v
print(S)
print(S2)
