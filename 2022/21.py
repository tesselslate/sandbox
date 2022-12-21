from sys import argv

F = [l.strip() for l in open(argv[1])]
M = {}

for l in F:
    words = l.split(" ")
    M[words[0].strip(":")] = words[1:]

def solve(monkey):
    if M[monkey][0].isdigit():
        return int(M[monkey][0])
    else:
        m = M[monkey]
        op = m[1] if m[1] != "/" else "//"
        return eval(f"{solve(m[0])} {op} {solve(m[2])}")

print(solve("root"))

path = []
c = "humn"
while c != "root":
    for k, v in M.items():
        if c in v:
            path.append(k)
            c = k
path.reverse()
path.append("humn")

def solve_for(node, value):
    if len(M[node]) == 1:
        return value
    else:
        node = M[node]
        a = node[0] in path
        other = solve(node[2]) if a else solve(node[0])

        tnode = node[0] if a else node[2]
        if node[1] == "+":
            return solve_for(tnode, value - other)
        elif node[1] == "-":
            if a:
                return solve_for(tnode, value + other)
            else:
                return solve_for(tnode, other - value)
        elif node[1] == "/":
            if a:
                return solve_for(tnode, value * other)
            else:
                return solve_for(tnode, other // value)
        else:
            return solve_for(tnode, value // other)

a = M["root"][0] == path[1]
v = solve_for(path[1], solve(M["root"][2] if a else M["root"][0]))
print(v)
