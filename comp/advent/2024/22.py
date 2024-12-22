import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
S = 0

def mix(n, secret):
    return n ^ secret

def prune(n):
    return n % 16777216

def ones(n):
    return n % 10

price_changes = []
prices = []
for l in F:
    n = int(l)
    first = [ones(n)]
    pc = []
    p = [n]
    for i in range(2000):
        n = prune(mix(n * 64, n))
        n = prune(mix(n // 32, n))
        n = prune(mix(n * 2048, n))
        first.append(ones(n))
        p.append(n)
    # print(l, n)
    # S += n
    for a, b in itertools.pairwise(first):
        pc.append(b-a)
    price_changes.append(pc)
    prices.append(p)

TARGET = (-2,1,-1,3)
C = Counter()
for i in range(len(F)):
    C2 = Counter()
    for j in range(1, len(price_changes[i]) - 4):
        cc = tuple(price_changes[i][j:j+4])
        if cc in C2: continue
        C2[cc] += prices[i][j+4] % 10

        if cc == TARGET: print(F[i], prices[i][j+4])
    for k, v in C2.items():
        C[k] += v

print(C[(-2,1,-1,3)])

best = 0
for k, v in C.items():
    if v > best:
        best = v
        print(k, best)
#
#
# def check(pcseq, seq):
#     for i in range(len(seq)-len(pcseq)):
#         if seq[i:i+len(pcseq)] == list(pcseq): return i
#     return None
#
# @functools.cache
# def tryseq(pcseq):
#     S = 0
#     for k, l in enumerate(F):
#         idx = check(pcseq, price_changes[k])
#         if idx is None: continue
#         selli = idx
#
#         n = int(l)
#         S += (prices[k][selli] + 1)%10
#     return S
#
# best = 0
# for _i in range(len(price_changes)):
#     for i in range(len(price_changes[_i])-4):
#         pcseq = price_changes[_i][i:i+4]
#
#         S = tryseq(tuple(pcseq))
#         if S > best: print(S, pcseq)
#         best = max(S,best)
# print(best)
#
# # not 1529
