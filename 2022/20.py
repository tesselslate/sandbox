from sys import argv

F = [l.strip() for l in open(argv[1])]
I = []

for idx, num in enumerate(F):
    I.append((idx, int(num)))

def mix(A):
    for i in range(len(A)):
        j = -1
        for idx, val in enumerate(A):
            if val[0] == i:
                j = idx
                break
        if j == -1:
            raise ValueError

        val = A[j]
        del A[j]
        A.insert((j + val[1]) % len(A), val)
    return A

def solve(A):
    j = -1
    for i in range(len(A)):
        if A[i][1] == 0:
            j = i
            break
    if j == -1:
        raise ValueError
    a = A[(j+1000)%len(A)]
    b = A[(j+2000)%len(A)]
    c = A[(j+3000)%len(A)]
    print(a[1]+b[1]+c[1])

solve(mix(I.copy()))
A = [(x[0], x[1] * 811589153) for x in I]
for _ in range(10):
    A = mix(A)
solve(A)
