import collections, util
from sys import argv

F = [l.strip() for l in open(argv[1])][0]
S = 0

pcount, last = util.scan("%d players; last marble is worth %d points", F)

idx = 0
marble = 1
player = 0
players = [0 for _ in range(pcount)]
circle = collections.deque([0])

while True:
    if marble % 23 == 0:
        circle.rotate(-7)
        players[player] += circle.pop()
        players[player] += marble
    else:
        circle.rotate(2)
        circle.append(marble)
    marble += 1
    player = (player + 1) % pcount
    if marble == last:
        print(max(players))
    if marble == last * 100:
        print(max(players))
        break
