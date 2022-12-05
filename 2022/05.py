import copy, util
from sys import argv

F = [l.strip("\n") for l in open(argv[1])]
G = []

for i in range(9):
    R = []
    for j in range(8):
        c = F[j][1+i*4]
        if c != " ":
            R.append(c)
    R.reverse()
    G.append(R)
G2 = copy.deepcopy(G)
actions = []
for i in range(10, len(F)):
    l = F[i]
    a, b, c = util.scan("move %d from %d to %d", l)
    actions.append((a,b,c))

for a in actions:
    for i in range(a[0]):
        G[a[2]-1].append(G[a[1]-1].pop())
print(''.join([c[len(c)-1] for c in G]))
for a in actions:
    L = []
    for i in range(a[0]):
        L.append(G2[a[1]-1].pop())
    L.reverse()
    G2[a[2]-1] += L
print(''.join([c[len(c)-1] for c in G2]))
