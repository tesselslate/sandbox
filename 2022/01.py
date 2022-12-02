F = [l.strip() for l in open("inputs/01")]

elves = []
elf = 0
for l in F:
    if l == "":
        elves.append(elf)
        elf = 0
        continue
    elf += int(l)
elves.sort()
print(elves[-1])
print(elves[-1]+elves[-2]+elves[-3])
