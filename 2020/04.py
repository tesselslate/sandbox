import functools, math, re, string, sys, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

if len(sys.argv) > 1:
    F = open(sys.argv[1])
else:
    F = sys.stdin.readlines()
    if not F[-1].strip():
        del F[-1]

F = [l.strip() for l in F]
F = ul.double_linefeed(F)

S = 0

for p in F:
    n = 0
    for l in p:
        w = l.split()
        for x in w:
            a, b = x.split(":")
            if a in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]: n += 1
    if n == 7:
        S += 1
print(S)

S = 0
for p in F:
    n = 0
    for l in p:
        w = l.split()
        for x in w:
            a, b = x.split(":")
            match a:
                case "byr":
                    if 1920 <= int(b) <= 2002: n += 1
                case "iyr":
                    if 2010 <= int(b) <= 2020: n += 1
                case "eyr":
                    if 2020 <= int(b) <= 2030: n += 1
                case "hgt":
                    x = b[-2:]
                    y = b[:-2]
                    if x == "in":
                        if 59 <= int(y) <= 76:
                            n += 1
                    if x == "cm":
                        if 150 <= int(y) <= 193:
                            n += 1
                case "hcl":
                    if b[0] == "#":
                        if set(b[1:]) & set("1234567890abcdef") == set(b[1:]):
                            n += 1
                case "ecl":
                    if b in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
                        n += 1
                case "pid":
                    if b.isdigit() and len(b) == 9:
                        n += 1
    if n == 7:
        S += 1
print(S)
