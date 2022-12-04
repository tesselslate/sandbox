import sys
sys.setrecursionlimit(1000000)

def grid(size, fill=None):
    return [[fill]*size for _ in range(size)]

def grid3d(size, fill=None):
    return [grid(size, fill) for _ in range(size)]

def halves(x):
    l = len(x) // 2
    return x[:l], x[l:]

def manhattan(a, b, x, y):
    return abs(a-x) + abs(b-y)

def print_grid(grid):
    for y in grid:
        s = ""
        for x in y:
            s += str(x)
        print(s)
