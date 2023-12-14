import collections, itertools, re, sys

sys.setrecursionlimit(10 ** 6)

"""
Helpers
"""

def batched(xs, n):
    """Returns tuples of size `n` from the iterator `xs`."""
    assert n > 0
    it = iter(xs)
    while batch := tuple(itertools.islice(it, n)):
        yield batch

def itersplit(inp, delim):
    """Returns lists of values from the given iterator `inp` separated by the value `delim`."""
    xs = []
    for x in inp:
        if x == delim:
            yield xs
            xs = []
        else:
            xs += [x]
    yield xs

def minmax(*xs):
    """Returns the minimum and maximum of the given values."""
    return min(xs), max(xs)

def range_intersect(a, b):
    """Returns the intersection of the given (start, stop) tuples, or None if none exists."""
    x = (max(a[0], b[0]), min(a[1], b[1]))
    return x if x[0] <= x[1] else None

def transpose(xs):
    """Transposes the given 2D list (or other similar structure.) Returns a 2D list."""
    return [*map(list, zip(*xs))]

"""
2D functions
"""

def gcol(grid, col):
    """Returns a column from a grid. Elements are copied."""
    return [grid[row][col] for row in range(len(grid))]

def grid(inp, func=None):
    """Creates a grid from an input (list of strings). Runs the provided function on each character."""
    if not func:
        func = lambda x : x
    return [[func(x) for x in l] for l in inp]

def gridcheck(grid, r, c):
    """Checks if r,c is in bounds."""
    return r >= 0 and r < len(grid) and c >=0 and c < len(grid[0])

def gridpoints(grid):
    """Returns an iterator of (x,y) pairs representing points in the grid."""
    for x in itertools.product(range(len(grid)), range(len(grid[0]))):
        yield x

def manhat(a, b):
    """Manhattan distance of two points stored as complex numbers."""
    return abs(a.real-b.real) + abs(a.imag-b.imag)

EAST = 1

"""
2D (integer point) functions
"""

def dirs_rc(inp):
    """Returns a list of 2d offsets based on the given list of inputs (WSEN, LDRU)"""
    m = {
            "W": 0, "L": 0,
            "S": 1, "D": 1,
            "E": 2, "R": 2,
            "N": 3, "U": 3,
    }
    return [padj4()[m[c]] for c in inp]

def dirs_xy(inp):
    """Returns a list of 2d offsets based on the given list of inputs (NESW, URDL)"""
    m = {
            "N": 0, "U": 0,
            "E": 1, "R": 1,
            "S": 2, "D": 2,
            "W": 3, "L": 3,
    }
    return [padj4()[m[c]] for c in inp]

def padj4():
    """All 4 2d adjacent offsets (x,y tuples)"""
    return [(0,-1),(1,0),(0,1),(-1,0)]

def padj8():
    """All 8 2d adjacent offsets (x,y tuples)"""
    return [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]

def pccw(x, y):
    """Rotate 2d point (integers) counter-clockwise around the origin"""
    return y, -x

def pcw(x, y):
    """Rotate 2d point (integers) clockwise around the origin"""
    return -y, x

"""
N-dimensional functions
"""

def ndadj(n):
    """Iterator of offsets directly adjacent to a given point in N-dimensional space"""
    for p in itertools.product(*([range(-1,2)] * n)):
        if p.count(0) == len(p) - 1:
            yield p

def ndadj_all(n):
    """Iterator of offsets within 1 tile of a given point in N-dimensional space"""
    for p in itertools.product(*([range(-1,2)] * n)):
        if p.count(0) < len(p):
            yield p

"""
Graph functions
"""

def rev_graph(g):
    """Takes a graph (two-layer dictionary) and reverses the direction."""
    n = dict()
    for j in g.keys():
        for k, v in g[j].items():
            if k not in n:
                n[k] = {}
            n[k][j] = v
    return n

"""
Parsing functions
"""

def double_linefeed(inp):
    """
    Splits the given input into nested lists by double newlines.
    Parse the following input like so:

    A
    B

    C

    D
    EF
    [["A", "B"], ["C"], ["D", "EF"]]
    """
    return [[l.strip() for l in x] for x in itersplit(inp, "")]

def halves(x):
    """Two halves of a string or list."""
    l = len(x)
    assert l % 2 == 0
    return x[:l//2], x[l//2:]

def input():
    F = [l.strip() for l in sys.stdin.readlines()]
    while F[-1] == "":
        del F[-1]
    return F

def scan(fmt, inp):
    """
    Basic sscanf copycat for quick input parsing.

    %d - Base 10 number
    %f - Float
    %s - String
    %x - Base 16 (hex) number
    """
    out = []
    idx = 0
    fmt_idx = 0
    while fmt_idx < len(fmt):
        fc = fmt[fmt_idx]

        # process non-format characters
        if fc != '%':
            if inp[idx] != fc:
                raise ValueError(f"mismatch at {idx} ({inp}): expected {fc}, got {inp[idx]}")
            fmt_idx += 1
            idx += 1
            continue

        # read text for this capture
        typ = fmt[fmt_idx + 1]
        content = ""
        if fmt_idx + 2 == len(fmt):
            fmt_idx = len(fmt)
            content = inp[idx:]
        else:
            delim = fmt[fmt_idx + 2]
            while inp[idx] != delim:
                content += inp[idx]
                idx += 1
        fmt_idx += 2

        # convert capture and continue
        if typ == 'd':
            out.append(int(content))
        if typ == 'f':
            out.append(float(content))
        if typ == 's':
            out.append(content)
        if typ == 'x':
            out.append(int(content, 16))
    return out

if __name__ == "__main__":
    # TODO: test
    pass
