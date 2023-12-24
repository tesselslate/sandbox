import itertools, ul
import z3

F = ul.input()
L = []

for l in F:
    x, y, z, vx, vy, vz = ul.ints(l)
    L.append(((x,y,z), (vx,vy,vz)))

MIN, MAX = 200000000000000, 400000000000000

def intersect2d(a,b):
    x1, y1, x2, y2, x3, y3, x4, y4 = a[0][0], a[0][1], a[1][0], a[1][1], b[0][0], b[0][1], b[1][0], b[1][1]
    x_num = (x1*y2 - y1*x2)*(x3 - x4) - (x1-x2)*(x3*y4 - y3*x4)
    x_den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    y_num = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4)
    y_den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if x_den == 0 or y_den == 0: return None
    return (x_num / x_den, y_num / y_den)

points = set()
for (a, b) in itertools.combinations(L, 2):
    a1 = a[0][:2]
    b1 = b[0][:2]
    a2 = tuple(map(lambda x, y: x+y, a[0][:2], a[1][:2]))
    b2 = tuple(map(lambda x, y: x+y, b[0][:2], b[1][:2]))

    p = intersect2d((a1, a2), (b1, b2))
    if p and MIN <= p[0] <= MAX and MIN <= p[1] <= MAX:
        at = (p[0] - a1[0]) / a[1][0]
        bt = (p[0] - b1[0]) / b[1][0]
        if at >= 0 and bt >= 0: points.add((a,b))
print(len(points))

s = z3.Solver()
rx, ry, rz, rvx, rvy, rvz = z3.Ints("rx ry rz rvx rvy rvz")

for i, l in enumerate(L[:3]):
    x, y, z, vx, vy, vz, t = z3.Ints(f"x{i} y{i} z{i} vx{i} vy{i} vz{i} t{i}")
    s.add(x == l[0][0])
    s.add(y == l[0][1])
    s.add(z == l[0][2])
    s.add(vx == l[1][0])
    s.add(vy == l[1][1])
    s.add(vz == l[1][2])
    s.add((x + vx * t) == (rx + rvx * t))
    s.add((y + vy * t) == (ry + rvy * t))
    s.add((z + vz * t) == (rz + rvz * t))

s.check()
print(s.model().eval(rx + ry + rz))
