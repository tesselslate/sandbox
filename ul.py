import collections, itertools, re, sys

sys.setrecursionlimit(10 ** 6)

"""
2D functions
"""

def ccw(x):
    """Rotate 2d point counter-clockwise around the origin"""
    return x * -1j

def cw(x):
    """Rotate 2d point clockwise around the origin"""
    return x * 1j

def grid(inp, func=None):
    """Creates a grid from an input (list of strings). Runs the provided function on each character."""
    if not func:
        func = lambda x : x
    return [[func(x) for x in l] for l in inp]

def manhat(a, b):
    """Manhattan distance of two points stored as complex numbers."""
    return abs(a.real-b.real) + abs(a.imag-b.imag)

def rots():
    """All 2d rotations (multiply)"""
    return [1, -1, 1j, -1j]

"""
Graph functions
"""

def rev_graph(g):
    """Takes a graph (two-layer dictionary) and reverses the direction."""
    n = dict()
    for j in g.keys():
        for k, v in g[j]:
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
    return [[l.strip() for l in x] for x in itertools.groupby(inp, "")]

def halves(x):
    """Two halves of a string or list."""
    l = len(x)
    assert l % 2 == 0
    return x[:l], x[l:]

def ints(inp):
    """Return all ints in the given string in a list."""
    return [int(x) for x in re.findall(r'\d+', inp)]

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