import util
from sys import argv

F = [l.strip() for l in open(argv[1])]
S = 0

for l in F:
    a, b, c, d = util.scan("%d-%d,%d-%d", l)
    x, y = set(util.irange(a,b)), set(util.irange(c,d))
    if x <= y or y <= x:
        S += 1
print(S)

S = 0
for l in F:
    a, b, c, d = util.scan("%d-%d,%d-%d", l)
    x, y = set(util.irange(a,b)), set(util.irange(c,d))
    if x & y:
        S += 1
print(S)
