F = [l.strip() for l in open("inputs/03")]

sum = 0
for l in F:
    a = len(l) // 2
    x = l[:a]
    y = l[a:]
    common = ''.join(set(x).intersection(y))
    p = 0
    a = common
    if a.islower():
        p = 1 + ord(a) - ord('a')
    else:
        p = 27 + ord(a) - ord('A')
    sum += p
print(sum)

sum = 0
for i in range(0, len(F), 3):
    x = F[i]
    y = F[i+1]
    z = F[i+2]
    common = ''.join(set(x).intersection(y).intersection(z))
    p = 0
    a = common
    if a.islower():
        p = 1 + ord(a) - ord('a')
    else:
        p = 27 + ord(a) - ord('A')
    sum += p
print(sum)
