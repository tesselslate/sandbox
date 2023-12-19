import math, ul

F = ul.input()
F = ul.double_linefeed(F)

workflows = {}

for l in F[0]:
    a, b = ul.scan("%s{%s}", l)
    xs = b.split(",")
    workflows[a] = xs

S = 0
for l in F[1]:
    x, m, a, s = ul.scan("{x=%d,m=%d,a=%d,s=%d}", l)
    label = "in"
    while label != "A" and label != "R":
        rules = workflows[label]
        for rule in rules:
            cond, dest = None, None
            if ":" in rule: cond, dest = rule.split(":")
            else: dest = rule

            if not cond or eval(cond):
                label = dest
                break
    if label == "A": S += x+m+a+s
print(S)

S = 0
ranges = [("in", {k: (1, 4001) for k in "xmas"})]
while len(ranges):
    (label, vars) = ranges.pop()
    if label == "A": S += math.prod(x[1] - x[0] for x in vars.values()); continue
    if label == "R": continue

    rules = workflows[label]
    for rule in rules:
        cond, dest = None, None
        if ":" in rule: cond, dest = rule.split(":")
        else: ranges.append((rule, vars.copy())); continue

        var, op, n = cond[0], cond[1], int(cond[2:])
        if op == "<":
            p = (1, n)
            f = (n, 4001)
        else:
            p = (n+1, 4001)
            f = (1, n+1)
        p = ul.range_intersect(p, vars[var])
        f = ul.range_intersect(f, vars[var])
        if p:
            nvars = vars.copy()
            nvars[var] = p
            ranges.append((dest, nvars))
        if not f: break
        vars[var] = f
print(S)
