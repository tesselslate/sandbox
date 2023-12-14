import ul

F = ul.input()
F = ul.double_linefeed(F)

elves = []
for ls in F:
    elves.append((sum(int(l) for l in ls)))
elves.sort()
print(elves[-1])
print(sum(elves[-3:]))
