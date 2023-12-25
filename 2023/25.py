import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

G = defaultdict(set)
p = set()
for l in F:
    w = l.split()
    a = w[0].strip(":")
    xs = w[1:]
    for x in xs:
        G[a].add(x)
        G[x].add(a)
        p.add((a,x))
G = dict(G)

# import graphviz
# d = graphviz.Graph()
# for k,v in G.items():
#     d.node(k)
#     for x in v:
#         d.edge(k, x)
# d.engine = 'neato'
# d.render('d.gv', view=True, )

# M = defaultdict(lambda: math.inf)
# for k, v in G.items():
#     for x in v:
#         M[k,x] = 1
#         M[x,k] = 1
# for b, a, c in itertools.product(G.keys(), repeat=3):
#     M[a,c] = min(M[a,c], M[a,b] + M[b,c])
#
#

#
def search(d, start):
    Q = deque([start])
    V = set()
    while len(Q):
         k = Q.popleft()
         xs = d[k]
         V.add(k)
         for x in xs:
             if x not in V: Q.append(x)
    return V

# rsm, bvc
# zmq pgh
# ldk bkm

G['rsm'].remove('bvc')
G['bvc'].remove('rsm')
G['zmq'].remove('pgh')
G['pgh'].remove('zmq')
G['bkm'].remove('ldk')
G['ldk'].remove('bkm')

x = search(G, 'rsm')
y = search(G, 'bvc')
print(len(x)*len(y))
