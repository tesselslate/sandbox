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
ranges = deque([("in", -1, {})])
while len(ranges):
    (current, rule_num, ratings) = ranges.popleft()
    #
    # if rule_num == -1:
    #     # find targets
    #     workflow = workflows[current]
    #     nums = defaultdict(list)
    #     for rule in workflow:
    #         target = rule[0]
    #         xs = [int(x) for x in re.findall(r"\d+", rule)]
    #         if xs:
    #             assert len(xs) == 1
    #             nums[target].append(xs[0])
    #
    #     # create new ranges
    #     ranges.append((current, 0, dict(nums)))
    #     continue
    #
