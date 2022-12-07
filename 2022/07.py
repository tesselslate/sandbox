from sys import argv

F = [l.strip() for l in open(argv[1])]
S = 0

cd = []
fs = {}

i = -1
while i < len(F):
    i += 1
    l = F[i]
    words = l.split(" ")
    if words[0] == '$' and words[1] == 'cd':
        dir = words[2]
        if dir == '/':
            cd = []
        elif dir == '..':
            cd.pop()
        else:
            cd.append(dir)
        continue
    if words[0] == '$' and words[1] == 'ls':
        i += 1
        entries = {}
        while i < len(F):
            l = F[i]
            if F[i][0] == '$':
                i -= 1
                break
            i += 1
            words = l.split(" ")
            if words[0] == 'dir':
                entries[words[1]] = {}
            else:
                entries[words[1]] = int(words[0])
        c = fs
        for dir in cd:
            c = c[dir]
        for k, v in entries.items():
            c[k] = v

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
U = 70000000 - T

deletable = {}
def recurse2(cd, d):
    global U
    s = 0
    for k,v in d.items():
        if type(v) == int:
            s += v
        else:
            s += recurse2(cd + k + "/", v)
    if s + U >= 30000000:
        deletable[cd] = s
    return s
recurse2("/", fs)
print(deletable[min(deletable, key=deletable.get)])
