import string, util
from sys import argv

F = [l.strip() for l in open(argv[1])]
G = util.graph()

for l in F:
    a, b = util.scan("Step %s must be finished before step %s can begin.", l)
    G.add_edge(a, b)

O = []
Q = [G.find_independent()[0]]
while len(Q) > 0:
    el = Q.pop()
    O.append(el)

    next = G.dependents(el)
    for n in next:
        if n in Q or n in O:
            continue
        if set(G.dependencies(n)) <= set(O):
            Q.append(n)
    Q.sort()
    Q.reverse()
print(''.join(O))

WC = 5
workers: list[tuple[str, int]] = [("", 0)]*WC
T = 0
D = []
while True:
    working = 0
    for v in workers:
        working += v[1]
    if working == 0 and len(O) == 0:
        break

    for i in range(WC):
        if workers[i][1] == 0:
            D.append(workers[i][0])

            # assign new task if possible
            for c in O:
                if set(G.dependencies(c)) <= set(D):
                    workers[i] = (c, 60 + string.ascii_uppercase.index(c))
                    O.remove(c)
                    break
        else:
            workers[i] = (workers[i][0], workers[i][1] - 1)
    T += 1
print(T)
