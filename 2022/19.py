import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
B = []

for l in F:
    _, or_or, cl_or, ob_or, ob_cl, ge_or, ge_ob = [int(x) for x in re.findall(r'\d+', l)]
    B.append((
        (or_or, 0, 0, 0),
        (cl_or, 0, 0, 0),
        (ob_or, ob_cl, 0, 0),
        (ge_or, 0, ge_ob, 0)
    ))

# blueprint format
# (ore bot cost, clay bot cost, ob bot cost, geode bot cost)
# each "cost" is a tuple containing (ore, clay, ob)

# optimizations:
# - do not wait and then make a bot if we could have made it before
# - do not follow suboptimal states
#
# - max robots:
#   - do not make more clay robots than obsidian robot clay cost
#   - do not make more obsidian robots than geode robot obsidian cost
#   - do not make more ore robots than max(ore, clay, obsidian, geode)

costs = None
heuristics = [None] * 4

cache = defaultdict(int)

@functools.cache
def afford(typ, items):
    for cost, count in zip(costs[typ], items):
        if count < cost: return False
    return True

def sim(bots, items, prev, time):
    if cache[bots, items, time] > items[3]:
        # this path is not worth following
        return -1
    if time == 0: return items[3]

    new_items = tuple(map(lambda a, b: a + b, bots, items))
    M = items[3]

    new_prev = []
    for i in range(4):
        can_make = afford(i, items)
        new_prev.append(can_make)

        if can_make and not prev[i] and bots[i] < heuristics[i]:
            newer_items = tuple(map(lambda a, b: a - b, new_items, costs[i]))
            new_bots = tuple(x if i != j else x+1 for j, x in enumerate(bots))
            M = max(M, sim(new_bots, newer_items, (0, 0, 0, 0), time - 1))

    # make no bot
    M = max(M, sim(bots, new_items, new_prev, time - 1))
    cache[bots, items, time] = M
    return M

S = 0
for i, b in enumerate(B, 1):
    costs = b
    heuristics = [max(b[i][0] for i in range(4)), b[2][1], b[3][2], math.inf]
    cache.clear()
    afford.cache_clear()

    S += i * sim((1, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), 24)
print(S)

S = 1
for b in B[:3]:
    costs = b
    heuristics = [max(b[i][0] for i in range(4)), b[2][1], b[3][2], math.inf]
    cache.clear()
    afford.cache_clear()
    S *= sim((1, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), 32)
print(S)
