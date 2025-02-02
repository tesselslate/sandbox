# person standing on center of platform from [-1, 1]
# each jump chosen uniformly randomly from [-1, 1]
# average steps to jump off platform

import random

def sim():
    pos = 0
    steps = 0
    while abs(pos) <= 1:
        pos += random.uniform(-1, 1)
        steps += 1

    return steps

TRIALS = 10**7

avg = 0
mi, ma = float("inf"), float("-inf")
for _ in range(TRIALS):
    n = sim()

    mi = min(mi, n)
    ma = max(ma, n)
    avg += n

print(avg/TRIALS)
print(mi, ma)
