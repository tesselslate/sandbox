import ul

F = ul.input()

S = 0
for l in F:
    for i, c in enumerate(reversed(l)):
        S += (5**i) * ("=-012".index(c) - 2)

s = []
while S > 0:
    s += "012=-"[S%5]
    S = (S + 2) // 5
print("".join(reversed(s)))
