import ul

F = ul.input()

S = 0
for l in F:
    v = [int(c) for c in l if c.isdigit()]
    S += v[0] * 10 + v[-1]
print(S)

nums = "one two three four five six seven eight nine".split()
S = 0
for l in F:
    v = []
    for i, c in enumerate(l):
        if c.isdigit(): v.append(int(c))
        for j, nw in enumerate(nums):
            if l[i:].startswith(nw): v.append(j+1)
    S += v[0] * 10 + v[-1]
print(S)
