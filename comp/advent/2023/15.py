import ul

F = ul.input()
F = [x for x in F[0].split(",")]

def h(x):
    n = 0
    for c in x:
        n += ord(c)
        n *= 17
        n %= 256
    return n
print(sum(h(x) for x in F))

boxes = [dict() for _ in range(256)]
for cs in F:
    label = cs[:-2 if cs[-2] == "=" else -1]
    box = h(label)
    if cs.endswith("-"):
        if label in boxes[box]:
            del boxes[box][label]
    else:
        boxes[box][label] = int(cs[-1])

S = 0
for j, box in enumerate(boxes):
    S += sum((i+1)*(j+1)*value for (i, value) in enumerate(box.values()))
print(S)
