import math, re, ul

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
# - give up immediately if we cannot beat the best geode count so far
#
# - max robots:
#   - do not make more clay robots than obsidian robot clay cost
#   - do not make more obsidian robots than geode robot obsidian cost
#   - do not make more ore robots than max(ore, clay, obsidian, geode)

costs = None
max_bots = [0] * 4
GM = 0

def afford(typ, items):
    for cost, count in zip(costs[typ], items):
        if count < cost: return False
    return True

def sim(bots, items, prev, time):
    global GM

    if time == 0: return (GM := max(GM, items[3]))
    if (items[3] + time * (time + bots[3])) < GM: return -1

    new_items = tuple(map(lambda a, b: a + b, bots, items))
    M = items[3]

    new_prev = []
    for i in range(4):
        can_make = afford(i, items)
        new_prev.append(can_make)

        if can_make and not prev[i] and bots[i] < max_bots[i]:
            newer_items = tuple(map(lambda a, b: a - b, new_items, costs[i]))
            new_bots = tuple(x if i != j else x+1 for j, x in enumerate(bots))
            M = max(M, sim(new_bots, newer_items, (0, 0, 0, 0), time - 1))

    # make no bot
    M = max(M, sim(bots, new_items, new_prev, time - 1))
    return M

def run(blueprint, time):
    global costs, max_bots, GM

    costs = blueprint
    max_bots = [
        max(blueprint[i][0] for i in range(4)), # max ore robots (max ore for any robot)
        blueprint[2][1],                        # max clay robots (obsidian clay cost)
        blueprint[3][2],                        # max obsidian robots (geode obsidian cost)
        999,                                    # max geode robots (inf)
    ]
    GM = 0

    return sim((1, 0, 0, 0), [0]*4, [0]*4, time)

print(sum(i * run(b, 24) for i, b in enumerate(B, 1)))
print(math.prod(run(b, 32) for b in B[:3]))
