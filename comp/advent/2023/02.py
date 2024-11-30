import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

S = 0
S2 = 0
for l in F:
    id, cubes = ul.scan("Game %d: %s", l)
    games = [game.strip() for game in cubes.split(";")]

    counts = defaultdict(int)
    for game in games:
        for pair in game.split(", "):
            count, color = ul.scan("%d %s", pair)
            counts[color] = max(counts[color], count)

    if counts["red"] <= 12 and counts["green"] <= 13 and counts["blue"] <= 14:
        S += id
    S2 += math.prod(counts.values())
print(S)
print(S2)
