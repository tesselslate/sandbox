import util
from sys import argv

F = [l.strip() for l in open(argv[1])]

BUF = 40
l = F[0].split(" ")[2]
I = [False]*BUF + [True if c == "#" else False for c in l] + [False]*BUF
R = []
for l in F[2:]:
    a, b = util.scan("%s => %s", l)
    v = ([True if c == "#" else False for c in a], True if b == "#" else False)
    R.append(v)

def tick():
    global I
    N = [False for _ in I]
    for i in range(2, len(I)-2):
        e = I[i-2:i+3]
        for r in R:
            if r[0] == e:
                N[i] = r[1]
                break
    I = N

for i in range(20):
    tick()

S = 0
for i in range(len(I)):
    if I[i] == True:
        S += i - BUF
print(S)
print(2212 + 78*(50*10**9))
# no idea where the pattern here is from but not gonna complain
