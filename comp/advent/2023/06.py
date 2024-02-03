import math, ul

F = ul.input()

times = [int(x) for x in F[0].split() if x.isdigit()]
distances = [int(x) for x in F[1].split() if x.isdigit()]

def sim(t, md):
    v = 0
    for i in range(t):
        d = (t - i) * i
        if d > md:
            v += 1
    return v

S = []
for t, d in zip(times, distances):
    S.append(sim(t,d))
print(math.prod(S))

time = int("".join(F[0].split()[1:]))
dist = int("".join(F[1].split()[1:]))
print(sim(time,dist))
