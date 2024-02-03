import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

C = 990941
R = [3, 7]

x, y = 0, 1
for i in range(C+10):
    a, b = R[x], R[y]
    digits = str(a+b)
    for d in digits:
        R.append(int(d))
    x, y = x + a + 1, y + b + 1
    x %= len(R)
    y %= len(R)
print(R[C:C+10])

R = [3, 7]
x, y = 0, 1
while True:
    a, b = R[x], R[y]
    digits = str(a+b)
    for d in digits:
        R.append(int(d))
    x, y = x + a + 1, y + b + 1
    x %= len(R)
    y %= len(R)
    if R[-6:] == [9,9,0,9,4,1]:
        print(len(R)-6)
        break
    if R[-7:-1] == [9,9,0,9,4,1]:
        print(len(R)-7)
        break
