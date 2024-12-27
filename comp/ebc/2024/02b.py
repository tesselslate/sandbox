import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.double_linefeed(ul.input())

target = F[0][0].split(":")[1].split(",")
words = F[1]

S = 0
for words in words:
    n = 0
    s = set()
    for i in range(len(words)+1):
        for word in target:
            if i < len(words) and words[i:].startswith(word):
                for j in range(len(word)):
                    s.add(i+j)
            if words[:i].endswith("".join(reversed(word))):
                for j in range(len(word)):
                    s.add(i-j-1)
    n = len(s)
    print(n,s,words)
    S += n

print(S)
