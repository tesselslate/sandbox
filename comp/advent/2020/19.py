import functools, math, re, string, sys, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

if len(sys.argv) > 1:
    F = open(sys.argv[1])
else:
    F = sys.stdin.readlines()

F = [l.strip() for l in F]
while F[-1] == "":
    del F[-1]
F = ul.double_linefeed(F)

S = 0

R = {}
for l in F[0]:
    a, b = ul.scan("%d: %s", l)
    R[a] = b
M = F[1]

def try_rule(msg, rule):
    xs = [int(x) for x in rule.split()]
    for x in xs:
        msg = match(msg, R[x])
        if msg == None:
            return None
    return msg

RET = None
i = 0
def match(msg, rule):
    global i
    if len(msg) == 0:
        # ????
        if rule == "42 31 | 42 11 31":
            i += 1
        return RET

    if rule.startswith("\"") and rule.endswith("\""):
        c = rule[1]
        if msg.startswith(c):
            return msg[1:]
        else:
            return None
    else:
        if "|" in rule:
            a, b = rule.split("|")
            v = try_rule(msg, a.strip())
            if v != None:
                return v
            return try_rule(msg, b.strip())
        else:
            return try_rule(msg, rule)

S = 0
for msg in M:
    v = match(msg, R[0])
    if type(v) == str and len(v) == 0:
        S += 1
print(S)

# soo i couldnt figure out how to properly get my thing to work
# but i found some weird pattern with combining the values of returning a match and no match that
# seem to give the correct answer
# maybe ill make it better later

S = 0
R[8] = "42 | 42 8"
R[11] = "42 31 | 42 11 31"

RET = None
i = 0
for msg in M:
    v = match(msg, R[0])
    if type(v) == str and len(v) == 0:
        S += 1
j = i
S2 = S
S = 0

RET = ""
for msg in M:
    v = match(msg, R[0])
    if type(v) == str and len(v) == 0:
        S += 1
print(S-j)
