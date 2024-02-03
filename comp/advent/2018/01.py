F = [l.strip() for l in open("inputs/01")]

sum = 0
for l in F:
    sum += int(l)
print(sum)

sum = 0
freqs = dict()
while True:
    for l in F:
        sum += int(l)
        if sum in freqs:
            print(sum)
            quit()
        freqs[sum] = True
