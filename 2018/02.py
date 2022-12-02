import string
F = [l.strip() for l in open("inputs/02")]

twos = 0
threes = 0
for l in F:
    a = False
    b = False
    for c in string.ascii_lowercase:
        if not a and l.count(c) == 2:
            twos += 1
            a = True
        elif not b and l.count(c) == 3:
            threes += 1
            b = True
print(twos*threes)

for l in F:
    for j in F:
        c = 0
        for i in range(len(l)):
            if l[i] == j[i]:
                c += 1
        if c == len(l) - 1:
            print(l, j)
