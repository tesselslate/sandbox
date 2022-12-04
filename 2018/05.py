import string
F = [l.strip() for l in open("inputs/05")]
F = F[0]

def reduce(S):
    b = []
    for c in S:
        if len(b) > 0 and c.swapcase() == b[-1]:
            b.pop()
        else:
            b.append(c)
    return b

# part 1
print(len(reduce(F)))

# part 2
min = 1000000000
for c in string.ascii_lowercase:
    s = F
    s = s.replace(c, "")
    s = s.replace(c.upper(), "")
    val = len(reduce(s))
    if val < min:
        min = val
print(min)
