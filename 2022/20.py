import ul
from collections import deque

F = ul.input()
Q = deque([(i,int(x)) for i, x in enumerate(F)])

def mix(Q):
    for i in range(len(Q)):
        for j in range(len(Q)):
            if Q[j][0] == i: break
        else: assert False
        x = Q[j]
        Q.rotate(-j)
        assert Q.popleft() == x
        Q.rotate(-(x[1] % len(Q)))
        Q.insert(0, (x[0], x[1]))

def ans():
    for i in range(len(Q)):
        if Q[i][1] == 0: break
    else: assert False
    print(sum(Q[(i+x*1000)%len(F)][1] for x in range(1,4)))

mix(Q)
ans()

Q = deque([(i,int(x)*811589153) for i, x in enumerate(F)])
for _ in range(10): mix(Q)
ans()
