import math, ul

F = ul.input()
inputs = F[0]

I = {}
for l in F[2:]:
    a, b, c = ul.scan("%s = (%s, %s)", l)
    I[a] = (b,c)

spot = "AAA"
i = 0
while spot != "ZZZ":
    instr = inputs[i%len(inputs)]
    if instr == "L":
        spot = I[spot][0]
    else:
        spot = I[spot][1]
    i += 1
print(i)

Q = []
for k in I.keys():
    if k.endswith("A"): Q.append(k)

cycles = {}

i = 0
while len(cycles) < 6:
    NQ = []
    while len(Q):
        E = Q.pop()
        if E.endswith("Z"):
            if E not in cycles:
                cycles[E] = i

        spot = I[E]
        if inputs[i%len(inputs)] == "L":
            NQ.append(spot[0])
        else:
            NQ.append(spot[1])
    Q = NQ
    i += 1
print(math.lcm(*cycles.values()))
