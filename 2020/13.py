import functools, math, re, string, sys, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

if len(sys.argv) > 1:
    F = open(sys.argv[1])
else:
    F = sys.stdin.readlines()

F = [l.strip() for l in F]
while F[-1] == "":
    del F[-1]

S = 0

time = int(F[0])
F = F[1].split(",")

def p1():
    i = 0
    while True:
        for bus in F:
            if not bus.isdigit():
                continue
            if i * int(bus) >= time:
                v = ((i * int(bus)) - time) * int(bus)
                print(v)
                return
        i += 1
p1()

offsets = [(int(x), i) for i, x in enumerate(F) if x.isdigit()]

# period of valid answers (all buses in a row) is LCM of input bus IDs

offs = offsets.copy()
offs.sort()
offs.reverse()

OC = 4

period = math.lcm(*[x[0] for x in offs[:OC]])
print(period)

offset = 0
for i in range(1, period):
    good = True
    for x in offs[:OC]:
        if (i + x[1]) % x[0] != 0:
            good = False
            break
    if good:
        print("found offset", i)
        offset = i
        break

rem = offs[OC:]

i = offset
while True:
    good = True
    for x in rem:
        if (i + x[1]) % x[0] != 0:
            good = False
            break
    if good:
        break
    i += period
print(i)
