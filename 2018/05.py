import string
F = [l.strip() for l in open("inputs/05")]
F = F[0]

def reduce(F):
    while True:
        acted = False
        idx = 0
        for idx in range(len(F)-1):
            if F[idx].isupper():
                if F[idx+1].islower() and F[idx+1].upper() == F[idx]:
                    acted = True
                    F = F[:idx] + F[idx+2:]
                    break
            else:
                if F[idx+1].isupper() and F[idx+1].lower() == F[idx]:
                    acted = True
                    F = F[:idx] + F[idx+2:]
                    break
        if not acted:
            return F

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
