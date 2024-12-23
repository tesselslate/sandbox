import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
S = 0

U = defaultdict(set)

UU = {}
C = Counter()

def find(x):
    if UU[x] == x:
        return x

    return find(UU[x])

def unite(x, y):
    x = find(x)
    y = find(y)

    UU[x] = y

for l in F:
    a, b = l.split("-")

    UU[a] = a
    UU[b] = b

    U[a].add(b)
    U[b].add(a)

    unite(a, b)

for k in U:
    #print(k, sorted(tuple(U[k])))
    pass

def check(k):
    def checksub(poss):
        for point in poss:
            for point2 in poss:
                if point != point2 and point not in U[point2]: return False
        print(k, ",".join(sorted(poss)))
    for poss in itertools.combinations(U[k], 12):
        if checksub(poss): return poss

for k in U:
    if check(k): print(k)

# for P in itertools.combinations(U.keys(), 13):
#     for i in P:
#         for j in P:
#             if i == j: continue
#             if i not in U[j]: break
#         else: continue
#         break
#     else:
#         print(P)



















# for k in U:
#     connected = defaultdict(set)
#     for p in U[k]:
#         for p2 in U[p]:
#             if p2 in connected[p].add(p2)

# C = Counter()
# for k in UU:
#     C[find(k)] += 1
#
# print(U["ox"])

# best = 0
# for k in U:
#     poss = U[k]
#     matches = Counter()
#
#     if len(poss) < best: continue
#     for p in poss:
#         for p2 in poss:
#             if p in U[p2]: matches[p] += 1
#
#     print(matches)

# L = []
#
# LL = [k for k in C.keys()]
#
# for x in LL:
#     connected = U[x]
#     print(x, connected)
#     ok = connected.copy()
#     for a, b in itertools.combinations(connected, 2):
#         if a not in U[b] or b not in U[a]: 
#             if a in ok: ok.remove(a)
#             if b in ok: ok.remove(b)
#     else: print(x, ok, len(ok))

# for k in U:
#     if "ox" in U[k] and k in U["ox"]: print(k); L.append(k)
#
# print(",".join(sorted(L)))

SS = set()
# for a, b, c in itertools.combinations(U.keys(), 3):
#     if a == b or a == c or b == c: continue
#     if a in U[b] and a in U[c] and b in U[a] and b in U[c] and c in U[a] and c in U[b]:
#         if a[0] == "t" or b[0] == "t" or c[0] == "t":
#             SS.add(tuple(sorted((a,b,c))))


"""THIS ONE IS OK"""
# for i_ in range(7, len(U)):
#     for P in itertools.combinations(U.keys(), i_):
#         P = list(P)
#         if any(len(U[p]) < 7 for p in P): continue
#         for i in range(len(P)):
#             for j in range(len(P)):
#                 if i == j: continue
#                 if P[i] not in U[P[j]] or P[j] not in U[P[i]]: break
#             else: continue
#             break
#         else:
#             if i_ > 3: print(i_, P)
#
# import graphviz
# d = graphviz.Graph()
# for k, v in U.items():
#     d.node(k)
#     for x in v:
#         d.edge(k,x)
# d.engine = 'osage'
# d.render('d.gv', view=True, )
