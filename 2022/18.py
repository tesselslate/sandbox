import ul
from collections import deque

F = ul.input()
G = set()

for l in F:
    x, y, z = ul.scan("%d,%d,%d", l)
    G.add((x,y,z))

A = set()
Q = deque([(20,20,20)])
while len(Q):
    (x,y,z) = Q.popleft()
    if (x,y,z) in G: continue
    for (a,b,c) in ul.ndadj(3):
        a, b, c = a+x, b+y, c+z
        if -1 <= a <= 20 and -1 <= b <= 20 and -1 <= c <= 20:
            if (a,b,c) in A: continue
            A.add((a,b,c))
            Q.append((a,b,c))

S = 0
S2 = 0
for (x,y,z) in G:
    for (a,b,c) in ul.ndadj(3):
        a, b, c = a+x, b+y, c+z
        if (a,b,c) not in G: S += 1
        if (a,b,c) not in G and (a,b,c) in A: S2 += 1
print(S)
print(S2)
