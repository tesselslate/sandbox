import copy

IM = [
        [72,64,51,57,93,97,68],
        [62],
        [57,94,69,79,72],
        [80,64,92,93,64,56],
        [70,88,95,99,78,72,65,94],
        [57,95,81,61],
        [79,99],
        [68,98,62],
]

O = [
        lambda n : n * 19,
        lambda n : n * 11,
        lambda n : n + 6,
        lambda n : n + 5,
        lambda n : n + 7,
        lambda n : n * n,
        lambda n : n + 2,
        lambda n : n + 3,
]

T = [
        lambda n : 4 if n % 17 == 0 else 7,
        lambda n : 3 if n % 3 == 0 else 2,
        lambda n : 0 if n % 19 == 0 else 4,
        lambda n : 2 if n % 7 == 0 else 0,
        lambda n : 7 if n % 2 == 0 else 5,
        lambda n : 1 if n % 5 == 0 else 6,
        lambda n : 3 if n % 11 == 0 else 1,
        lambda n : 5 if n % 13 == 0 else 6,
]


def tick(div):
    global S, M

    for i in range(len(M)):
        S[i] += len(M[i])
        for item in M[i]:
            v = O[i](item)
            if div:
                v //= 3
            M[T[i](v)].append(v)
        M[i] = []

M = copy.deepcopy(IM)
S = [0]*len(M)
for _ in range(20):
    tick(True)
S = list(reversed(sorted(S)))
print(S[0]*S[1])

M = copy.deepcopy(IM)
S = [0]*len(M)
for i in range(10000):
    for i in range(len(M)):
        for j in range(len(M[i])):
            M[i][j] %= 17*3*19*7*2*5*11*13
    tick(False)
S = list(reversed(sorted(S)))
print(S[0]*S[1])
