import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
F = ul.double_linefeed(F)

workflows = {}

for l in F[0]:
    a, b = ul.scan("%s{%s}", l)
    xs = b.split(",")
    workflows[a] = xs

def check_rule(ratings, workflow):
    # ret: next_workflow, ok
    for rule in workflow:
        cond, dest = None, None
        if ":" not in rule:
            dest = rule
        else:
            cond, dest = rule.split(":")

        if not cond:
            if dest == "A": return None, True
            if dest == "R": return None, False
            return workflows[dest], True
        
        # exec_str = "\n".join([f"{k} = {v}" for k, v in ratings.items()]) + f"\nres = bool({cond})"
        estr = cond
        r = ratings
        estr = estr.replace("x", "r['x']")
        estr = estr.replace("m", "r['m']")
        estr = estr.replace("a", "r['a']")
        estr = estr.replace("s", "r['s']")
        result = eval(estr)
        if result:
            if dest == "A": return None, True
            if dest == "R": return None, False
            return workflows[dest], True
    assert False

S = 0
for l in F[1]:
    a, = ul.scan("{%s}", l)
    xs = a.split(",")
    ratings = {}
    for x in xs:
        a, b = x.split("=")
        ratings[a] = int(b)

    workflow = workflows["in"]
    while workflow:
        next_workflow, ok = check_rule(ratings, workflow)
        if not ok: break
        elif ok and not next_workflow: workflow = None
        else: workflow = next_workflow
    else:
        S += sum(ratings.values())

print(S)

S = 0
def add(r):
    global S
    S += math.prod([r[1] - r[0] for r in r.values()])

ranges = deque([("in", {k: (1,4001) for k in 'xmas'})])
while len(ranges):
    (workflow, ratings) = ranges.popleft()
    workflow = workflows[workflow]
    for rule in workflow:
        if ":" not in rule:
            if rule == "A": add(ratings)
            elif rule != "R": ranges.append((rule, ratings.copy()))
            break
        cond, dest = rule.split(":")
        var = cond[0]
        vv = ratings[var]
        comp = cond[1]
        val = int(cond[2:])

        p, f = None, None
        if comp == ">":
            p = (val+1, 4001)
            f = (1,val+1)
        else:
            p = (1,val)
            f = (val,4001)
        p = ul.range_intersect(p, vv)
        f = ul.range_intersect(f, vv)
        if p:
            nr = ratings.copy()
            nr[var] = p
            if dest == "A": add(nr)
            elif dest != "R": ranges.append((dest, nr))
        if not f: break
        ratings[var] = f
print(S)
