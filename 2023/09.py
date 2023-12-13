import itertools, ul

F = ul.input()
F = [[int(y) for y in x.split()] for x in F]

S = 0
for l in F:
    histories = [l.copy()]
    while not all(x == 0 for x in histories[-1]):
        xs = []
        for (a, b) in itertools.pairwise(histories[-1]):
            xs.append(b-a)
        histories.append(xs)
    for x in histories:
        S += x[-1]
print(S)

S = 0
for l in F:
    histories = [l.copy()]
    while not all(x == 0 for x in histories[-1]):
        xs = []
        for (b, a) in itertools.pairwise(histories[-1]):
            xs.append(b-a)
        histories.append(xs)
    for x in histories:
        S += x[0]
print(S)
