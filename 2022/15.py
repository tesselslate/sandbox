import util
from sys import argv

F = [l.strip() for l in open(argv[1])]

I = []
for l in F:
    a, b, c, d = util.scan("Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d", l)
    I.append(((a,b),(c,d)))

def no_beacon(scan, y):
    beacons = {s[1] for s in scan}
    S = set()
    for s in scan:
        a, b = s
        x1, y1 = a
        x2, y2 = b
        dist = util.manhattan(x1, y1, x2, y2)

        # x1, y1 = sensor
        x = x1
        while util.manhattan(x1, y1, x, y) < dist:
            x += 1
        d = x-x1
        for x in util.irange(x1-d, x1+d):
            if (x,y) not in beacons:
                S.add(x)
    return S

def find_beacon(scan, maxbound):
    dists = {}
    for s in scan:
        a, b = s
        x1, y1 = a
        x2, y2 = b
        d = util.manhattan(x1, y1, x2, y2)
        dists[a] = d+1

    s = set()
    for spot, dist in dists.items():
        j = dist
        x, y = spot[0], spot[1]
        for i in range(dist):
            s.add((x-j + i, y+i))
            s.add((x+j - i, y+i))
            s.add((x-j + i, y-i))
            s.add((x+j - i, y-i))

    v = None
    for spot in s:
        good = True
        for scanner, dist in dists.items():
            if util.manhattan(spot[0], spot[1], scanner[0], scanner[1]) <= dist-1:
                good = False
                break
            elif spot[0] < 0 or spot[0] > maxbound or spot[1] < 0 or spot[1] > maxbound:
                good = False
                break
        if good:
            v = spot
            break
    return v[0]*4000000+v[1]

print(len(no_beacon(I, 2000000)))
print(find_beacon(I, 4000000))
