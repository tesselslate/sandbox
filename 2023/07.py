import ul
from collections import Counter

F = ul.input()

def value(counter):
    match list(sorted(c.values())):
        case [5]:       return 10
        case [1, 4]:    return 9
        case [2, 3]:    return 8
        case [1, 1, 3]: return 7
        case [1, 2, 2]: return 6
        case [1,1,1,2]: return 5
        case _:         return 4

H = []
for l in F:
    cards = "23456789TJQKA"
    hand, bid = ul.scan("%s %d", l)
    c = Counter(hand)

    H.append((value(c), [cards.index(c) for c in hand], bid))
S = sum((i+1) * x[2] for (i, x) in enumerate(sorted(H)))
print(S)

H = []
for l in F:
    cards = "J23456789TQKA"
    hand, bid = ul.scan("%s %d", l)
    c = Counter(hand)

    if c["J"] == 5:
        H.append((10, [cards.index(c) for c in hand], bid))
    else:
        j = c["J"]
        del c["J"]
        x = c.most_common(1)[0][0]
        c[x] += j

        H.append((value(c), [cards.index(c) for c in hand], bid))
S = sum((i+1) * x[2] for (i, x) in enumerate(sorted(H)))
print(S)
