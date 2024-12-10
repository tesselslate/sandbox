import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()[0]
S = 0

# SLOTS = []
# for i in range(len(F)):
#     y = F[i]
#     if i % 2 == 0:
#         for x in range(int(y)):
#             SLOTS.append(i // 2)
#     else:
#         for x in range(int(y)):
#             SLOTS.append(None)
# STR = ""
# print("".join(str(x) if x != None else "." for x in SLOTS))
#
# while True:
#     while SLOTS[-1] == None:
#         SLOTS = SLOTS[:-1]
#     try:
#         x = SLOTS.index(None)
#         SLOTS[x] = SLOTS[-1]
#         SLOTS = SLOTS[:-1]
#     except:
#         break
#
# S = 0
# for (i, x) in enumerate(SLOTS):
#     S += i * x
# print(S)

SLOTS = []
for i in range(len(F)):
    y = F[i]
    if i % 2 == 0:
        SLOTS.append((i//2, int(y)))
    else:
        SLOTS.append((None, int(y)))

# while True:
#     j = len(SLOTS) - 1
#     swaps = 0
#     while j >= 0:
#         if j < 0 or SLOTS[j][0] is None:
#             j -= 1
#             continue
#         if j == 0: break
#         file = SLOTS[j]
#         j -= 1
#
#         for (i, x) in enumerate(SLOTS):
#             x, y = x
#             if x is None and y == file[1]:
#                 SLOTS[i] = file
#                 SLOTS[j] = (None, file[1])
#                 swaps += 1
#             elif x is None and y > file[1]:
#                 SLOTS[i] = file
#                 SLOTS.insert(i+1, ((None, y-file[1])))
#                 SLOTS[j] = (None, file[1])
#                 swaps += 1
#     print(swaps, SLOTS)
#     if swaps == 0:
#         break

# while True:
#     ops = 0
#     for j in range(len(SLOTS) - 1, -1, -1):
#         src = SLOTS[j]
#         if src[0] is None: continue
#
#         for i in range(len(SLOTS)):
#             print(SLOTS)
#             dst = SLOTS[i]
#             if dst[0] is not None: continue
#             if dst[1] == src[1]:
#                 SLOTS[j], SLOTS[i] = SLOTS[i], SLOTS[j]
#                 ops += 1
#                 break
#             elif dst[1] > src[1]:
#                 SLOTS.insert(i, (None, dst[1]-src[1]))
#                 SLOTS[i] = src
#                 SLOTS[j] = dst
#                 ops += 1
#                 break
#
#     for i in range(len(SLOTS)-2, -1, -1):
#         a, b = SLOTS[i], SLOTS[i+1]
#         if a[0] is None and b[0] is None:
#             SLOTS[i] = (None, a[1] + b[1])
#             del SLOTS[i+1]
#             ops += 1
#     if ops == 0: break

def pprint(xs):
    STR = ""
    for x in xs:
        if x[0] is None: STR += "." * x[1]
        else: STR += str(x[0]) * x[1]
    print(STR)

def pprintx(xs):
    STR = ""
    for x in xs:
        if x[0] is None: STR += "." * x[1]
        else: STR += str(x[0]) * x[1]
    return STR

while True:
    ops = 0

    for src_idx in range(len(SLOTS) - 1, -1, -1):
        src = SLOTS[src_idx]
        if src[0] is None: continue

        for dst_idx in range(src_idx):
            dst = SLOTS[dst_idx]
            if dst[0] is not None: continue

            if src[1] == dst[1]:
                SLOTS[src_idx], SLOTS[dst_idx] = dst, src
                ops += 1
                break
            elif dst[1] > src[1]:
                SLOTS[src_idx], SLOTS[dst_idx] = (None, dst[1]-(dst[1]-src[1])), src
                if SLOTS[dst_idx + 1][0] is None:
                    SLOTS[dst_idx + 1][1] += dst[1]-src[1]
                else:
                    SLOTS.insert(dst_idx + 1, (None, dst[1]-src[1]))
                ops += 1
                break
        else:
            continue
        break
    if ops == 0:
        break

pprint(SLOTS)
print(SLOTS)
S = 0
acc = 0
for x in SLOTS:
    x, y = x
    if x is not None:
        for j in range(y):
            S += (acc+j)*x
    acc += y
print(S)


# files = []
#
# i = 0
# for a, b in zip(F[::2], F[1::2]):
#     print(a)
#     files.append((i,int(a)))
#     i += 1
#
# print(files)
# print(sum(math.prod(x) for x in files))
