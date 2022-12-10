import collections
from sys import argv

F = [l.strip() for l in open(argv[1])]

cd = []
fs = {}

def get_dir(dir):
    c = fs
    for d in dir:
        c = c[d]
    return c

i = 0
while i < len(F):
    l = F[i]
    if l[0] == '$':
        cmd = l.split(" ")[1:]
        if cmd[0] == "ls":
            i += 1
            while i < len(F) and F[i][0] != '$':
                line = F[i]
                words = line.split(" ")
                if words[0] == "dir":
                    get_dir(cd)[words[1]] = {}
                else:
                    get_dir(cd)[words[1]] = int(words[0])
                i += 1
            continue
        elif cmd[0] == "cd":
            if cmd[1] == '/':
                cd = []
            elif cmd[1] == '..':
                cd.pop()
            else:
                cd.append(cmd[1])
    i += 1

S = 0
T = 0
def recurse(d):
    global S, T
    s = 0
    for v in d.values():
        if type(v) == int:
            s += v
            T += v
        else:
            s += recurse(v)
    if s <= 100000:
        S += s
    return s
recurse(fs)
print(S)

deletable = {}
def recurse2(d, cd="/"):
    s = 0
    for k, v in d.items():
        if type(v) == int:
            s += v
        else:
            s += recurse2(v, cd+k+"/")
    if T - s <= 40000000:
        deletable[cd] = s
    return s
recurse2(fs)
print(deletable[min(deletable, key=deletable.get)]) # type: ignore
