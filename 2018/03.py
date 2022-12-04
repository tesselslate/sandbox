import util
F = [l.strip() for l in open("inputs/03")]

claims = util.grid(1000, 0)
for l in F:
    n, x, y, w, h = util.scan("#%d @ %d,%d: %dx%d", l)
    for i in range(x, x+w):
        for j in range(y, y+h):
            claims[i][j] += 1
S = 0
for i in range(1000):
    for j in range(1000):
        if claims[i][j] > 1:
            S += 1
print(S)

for l in F:
    n, x, y, w, h = util.scan("#%d @ %d,%d: %dx%d", l)
    good = True
    for i in range(x, x+w):
        for j in range(y, y+h):
            if claims[i][j] > 1:
                good = False
    if good:
        print(n)
        quit()
