import util
from sys import argv

F = [l.strip() for l in open(argv[1])]
S = 0

I = []
for l in F:
    a, b = util.scan("%s %d", l)
    I.append([a,b])

def sign(n):
    return -1 if n < 0 else 1

def sim(k):
    global I

    V = set()
    K = [(0,0)]*k

    for i in I:
        m = (0,0)
        if i[0] == 'R':
            m = (1, 0)
        if i[0] == 'L':
            m = (-1, 0)
        if i[0] == 'U':
            m = (0, -1)
        if i[0] == 'D':
            m = (0, 1)

        for _ in range(i[1]):
            K[0] = (K[0][0] + m[0], K[0][1] + m[1])
            for idx in range(1, k):
                H = K[idx-1]
                T = K[idx]
                touching = abs(H[0] - T[0]) <= 1 and abs(H[1] - T[1]) <= 1
                if not touching:
                    v = H[1] != T[1]
                    h = H[0] != T[0]
                    
                    if v and not h:
                        T = (T[0], T[1] + sign(H[1] - T[1]))
                    elif h and not v:
                        T = (T[0] + sign(H[0] - T[0]), T[1])
                    elif h and v:
                        T = (T[0] + sign(H[0] - T[0]), T[1] + sign(H[1] - T[1]))
                K[idx] = T
                if idx == k-1:
                    V.add(T)
    return len(V)

print(sim(2))
print(sim(10))
