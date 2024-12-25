import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.double_linefeed(ul.input())

bits = {}
gates = {}
gates_bw = defaultdict(list)

for l in F[0]:
    name, value, *_ = l.split()
    bits[name[:-1]] = int(value)

for l in F[1]:
    a, op, b, _, dst, *_ = l.split()
    gates[dst] = (a, op, b)
    gates_bw[a].append((a, op, b, dst))
    gates_bw[b].append((a, op, b, dst))

@functools.cache
def evaluate(dst):
    if dst in bits:
        return bits[dst]

    gate = gates[dst]
    a, b = evaluate(gate[0]), evaluate(gate[2])
    match gate[1]:
        case "AND": return a & b
        case "XOR": return a ^ b
        case "OR":  return a | b

zbits = [evaluate(f"z{i:#02}") for i in reversed(range(46))]
print(int("".join(str(z) for z in zbits), base=2))

swaps = []

bad_z = []
for i in range(1,45):
    if gates[f"z{i:#02}"][1] != "XOR":
        bad_z.append(i)

for i in range(1,45):
    # one instance of swapped XOR/AND outputs
    gates = gates_bw[f"x{i:#02}"]
    bxor = [x for x in gates if x[1] == "XOR"][0]
    band = [x for x in gates if x[1] == "AND"][0]

    bxor_gates = gates_bw[bxor[3]]
    if len(bxor_gates) != 2:
        swaps += [bxor[3], band[3]]

    # three instances of messed up Z gates
    if i in bad_z:
        bxor2 = [x for x in bxor_gates if x[1] == "XOR"][0]
        swaps += [f"z{i:#02}", bxor2[3]]

print(",".join(sorted(swaps)))
