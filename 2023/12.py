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

F2 = []
for l in F:
    a, b = ul.scan("%s %s", l)
    xs = [int(x.strip()) for x in b.split(",")]
    F2.append((a,xs))
F = F2

# naive
# S = 0
# for (scan, nums) in F:
#     indices = [x for x in range(len(scan)) if scan[x] == "?"]
#     scan = list(scan)
#     for xs in itertools.product("#.", repeat=len(indices)):
#         for i, x in enumerate(xs):
#             scan[indices[i]] = x
#
#         groups = [len(list(x)) for (c, x) in itertools.groupby(scan) if c == "#"]
#         if groups == nums: S += 1
# print(S)

@functools.cache
def solve(s_idx, d_idx, prev):
    (springs, dmg) = L
    while s_idx < len(springs) and springs[s_idx] != "?":
        match springs[s_idx]:
            case ".":
                if prev > 0:
                    if d_idx == len(dmg) or dmg[d_idx] != prev:
                        return 0
                    prev = 0
                    d_idx += 1
            case "#": prev += 1
            case "?": assert False
        s_idx += 1
    if s_idx == len(springs):
        if prev > 0 and (d_idx == len(dmg) or dmg[d_idx] != prev):
            return 0
        return 1 if d_idx == len(dmg) else 0

    assert springs[s_idx] == "?"
    s = solve(s_idx + 1, d_idx, prev + 1)
    if prev > 0:
        if d_idx < len(dmg) and dmg[d_idx] == prev:
            s += solve(s_idx + 1, d_idx + 1, 0)
    else:
        s += solve(s_idx + 1, d_idx, 0)
    return s

S = 0
for L in F:
    (springs, dmg) = L
    L = (springs + ".", dmg)
    S += solve(0, 0, 0)
    solve.cache_clear()
print(S)

S = 0
for L in F:
    (springs, dmg) = L
    L = ("".join([springs, "?"] * 5), dmg * 5)
    S += solve(0, 0, 0)
    solve.cache_clear()
print(S)
