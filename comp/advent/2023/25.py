import math, random, ul
from collections import Counter, defaultdict, deque

F = ul.input()

G = defaultdict(set)
for l in F:
    w = l.split()
    a = w[0].strip(":")
    for x in w[1:]:
        G[a].add(x)
        G[x].add(a)

def pathfind(start, goal):
    Q = deque([(start, [start])])
    V = set([start])
    while len(Q):
        (k, path) = Q.popleft()
        if k == goal: return path
        for next in G[k]:
            if next not in V:
                V.add(next)
                Q.append((next, [n for n in path] + [next]))
    return None

c = Counter()
keys = list(G.keys())
for _ in range(500):
    a, b = 0, 0
    while a == b:
        a, b = random.randint(0,len(keys)-1), random.randint(0,len(keys)-1)
    path = pathfind(keys[a], keys[b])
    for node in path: c[node] += 1
check = c.most_common(6)

def search(start, ignore):
    start = start[0]
    Q = deque([start])
    V = set([start])
    while len(Q):
        k = Q.popleft()
        for next in G[k]:
            if next not in V and next not in ignore:
                V.add(next)
                Q.append(next)
    return V

counts = set()
for node in check:
    counts.add(len(search(node, {node[0] for node in check}))+2)
print(counts)
print(math.prod(counts))
