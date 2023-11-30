import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]

S = 0
ct = 0
for l in F:
    for w in l.split():
        a,b=util.scan("%s:%s", w)
        if a == "byr" or a == "iyr" or a == "eyr" or a == "hgt" or a == "hcl" or a == "ecl" or a == "pid":
            ct+=1
    if l == "":
        if ct == 7:
            S += 1
        ct = 0
if ct == 7:
    S += 1
ct = 0
print(S)

S = 0
ct = 0
for l in F:
    for w in l.split():
        a,b=util.scan("%s:%s", w)
        if a == "byr":
            if int(b) >= 1920 and int(b) <= 2002:
                ct+=1
        if a == "iyr":
            if int(b) >= 2010 and int(b) <= 2020:
                ct+=1
        if a == "eyr":
            if int(b) >= 2020 and int(b) <= 2030:
                ct += 1
        if a=="hgt":
            l = b[:-2]
            d = b[-2:]
            if d == "cm":
                if int(l) >= 150 and int(l) <= 193:
                    ct += 1
            if d == "in":
                if int(l) >= 59 and int(l) <= 76:
                    ct += 1
        if a == "hcl":
            if b[0] == "#":
                bad = False
                for i in range(6):
                    if b[i+1] not in "abcdef0123456789":
                        bad = True
                        break
                if not bad:
                    ct += 1
        if a == "ecl":
            if b in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
                ct += 1
        if a == "pid":
            if len(b) == 9 and b.isdigit():
                ct += 1
    if l == "":
        if ct == 7:
            S += 1
        ct = 0
if ct == 7:
    S += 1
ct = 0
print(S)
