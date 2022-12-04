import collections, util
F = [l.strip() for l in open("inputs/04")]
F.sort()

guards = dict()

guard = 0
lastmin = 0
for l in F:
    _, _, min, rem = util.scan("[%s %d:%d] %s", l)
    if "Guard" in rem:
        guard, = util.scan("Guard #%d begins", rem)
        if guard not in guards:
            guards[guard] = collections.Counter()
    elif "falls" in rem:
        lastmin = min
    elif "wakes" in rem:
        for i in range(lastmin, min):
            guards[guard][i] += 1
g, _ = util.max_countdict(guards)
print(g * guards[g].most_common(1)[0][0])

M = (0, 0)
C = 0
for guard, v in guards.items():
    for min, count in v.items():
        if count > C:
            M = (min, guard)
            C = count
print(M[0]*M[1])
