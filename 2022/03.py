import string, util
F = [l.strip() for l in open("inputs/03")]

sum = 0
for l in F:
    a, b = util.halves(l)
    sum += 1 + string.ascii_letters.index(''.join(set(a)&set(b)))
print(sum)

sum = 0
for i in range(0, len(F), 3):
    a, b, c = F[i], F[i+1], F[i+2]
    sum += 1 + string.ascii_letters.index(''.join(set(a)&set(b)&set(c)))
print(sum)
