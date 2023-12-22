import ul, z3

F = ul.input()

x = []
for l in F:
    words = l.split()
    words = [words[0].strip(":"), "= lambda:"] + [word+"()" if len(word) == 4 else word for word in words[1:]]
    x.append(" ".join(words))
x.append("print(root())")
exec("\n".join(x))

s = z3.Solver()
names = [l.split()[0].strip(":") for l in F]
ints = {name: z3.Int(name) for name in names}
xs = None
for l in F:
    words = l.split()
    name = words[0].strip(":")
    if name != "humn" and name != "root":
        if len(words) == 2:
            s.add(ints[name] == int(words[1]))
        else:
            match words[2]:
                case "+": s.add(ints[name] == ints[words[1]] + ints[words[3]])
                case "-": s.add(ints[name] == ints[words[1]] - ints[words[3]])
                case "*": s.add(ints[name] == ints[words[1]] * ints[words[3]])
                case "/": s.add(ints[name] == ints[words[1]] / ints[words[3]])
    if name == "root":
        s.add(ints[words[1]] == ints[words[3]])
s.check()
print(s.model().eval(ints["humn"]))
