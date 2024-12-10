import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()[0] + "0"

disk = []
for i, (file, free) in enumerate(zip(F[::2], F[1::2])):
    disk.extend([i] * int(file))
    disk.extend([None] * int(free))

i, j = 0, len(disk) - 1
while True:
    while disk[i] != None:
        i += 1
    while disk[j] == None:
        j -= 1
    if i > j:
        break

    disk[i], disk[j] = disk[j], disk[i]

print(sum(i*x for i, x in enumerate(disk[:disk.index(None)])))

pos = 0
files = [] # pos, sz, id
frees = [] # pos, sz
for i, (file, free) in enumerate(zip(F[::2], F[1::2])):
    files.append((pos, int(file), i))
    pos += int(file)

    frees.append((pos, int(free)))
    pos += int(free)

for i in range(len(files) - 1, -1, -1):
    pos, sz, id = files[i]

    for j in range(len(frees)):
        free_pos, free_sz = frees[j]
        if free_pos > pos: break

        if free_sz == sz:
            files[i] = (free_pos, sz, id)
            frees[j] = (free_pos, 0)
            break
        elif free_sz > sz:
            files[i] = (free_pos, sz, id)
            frees[j] = (free_pos + sz, free_sz - sz)
            break

S = 0
for pos, sz, id in files:
    for i in range(pos, pos+sz):
        S += i * id
print(S)
