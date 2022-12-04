from sys import argv

F = [l.strip() for l in open(argv[1])]
S = 0

for l in F:
    h = l.split(",")
    c = h[0].split("-")
    d = h[1].split("-")
    a, b, x, y = int(c[0]), int(c[1])+1, int(d[0]), int(d[1])+1
    i, j = set(range(a, b)), set(range(x, y))
    if i <= j or j <= i:
        S += 1
print(S)

S = 0
for l in F:
    h = l.split(",")
    c = h[0].split("-")
    d = h[1].split("-")
    a, b, x, y = int(c[0]), int(c[1])+1, int(d[0]), int(d[1])+1
    i, j = set(range(a, b)), set(range(x, y))
    a = list(set(i) & set(j))
    if len(a) > 0:
        S += 1
print(S)
