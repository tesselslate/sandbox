F = [l.strip() for l in open("inputs/04")]
F.sort()

minutes = dict()
sleeping = dict()
guard = 0
lastmin = 0

for l in F:
    minute = int(l.split(" ")[1].strip("]").split(":")[1])
    if "begins" in l:
        guard = int(l.split(" ")[3].strip("#"))
    elif "falls" in l:
        lastmin = minute
    elif "wakes" in l:
        if guard in sleeping:
            for i in range(lastmin, minute):
                if i in minutes[guard]:
                    minutes[guard][i] += 1
                else:
                    minutes[guard][i] = 1
            sleeping[guard] += minute - lastmin
        else:
            minutes[guard] = dict()
            for i in range(lastmin, minute):
                minutes[guard][i] = 1
            sleeping[guard] = minute - lastmin
k = list(sleeping.keys())
v = list(sleeping.values())
sleepiest = k[v.index(max(v))]
k = list(minutes[sleepiest].keys())
v = list(minutes[sleepiest].values())
maxmin = k[v.index(max(v))]
print(sleepiest,maxmin)
print(sleepiest*maxmin)

maximum = (0,0,0)
for idx, guard in minutes.items():
    for k, v in guard.items():
        if v > maximum[0]:
            maximum = (v,idx,k)
print(maximum[2]*maximum[1])
