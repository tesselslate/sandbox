import ul

F = ul.input()

S = 0
for l in F:
    for i, c in enumerate(reversed(l)):
        S += (5**i) * ("=-012".index(c) - 2)

s = []
c = False
while S > 0 or c:
    n = (S+c) % 5
    s.append("012=-"[n])
    S //= 5
    c = n >= 3 or (c and n == 0)
print("".join(reversed(s)))
