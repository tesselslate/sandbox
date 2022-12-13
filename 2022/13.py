from sys import argv

F = [l.strip() for l in open(argv[1])]

I = []
for i in range(0,len(F), 3):
    I.append([eval(F[i]), eval(F[i+1])])

def compare(x):
    a = x[0]
    b = x[1]
    al = len(a) == 0
    bl = len(b) == 0
    if al and not bl:
        return True
    elif bl and not al:
        return False
    elif al and bl:
        return None
    while a:
        av = a[0]
        bv = b[0]
        if type(av) == int and type(bv) == int:
            if av < bv:
                return True
            elif av > bv:
                return False
        elif type(av) == list and type(bv) == list:
            v = compare([av, bv])
            if v == True or v == False: return v
        else:
            avl = type(av) == list
            if avl:
                bv = [bv]
            else:
                av = [av]
            v = compare([av, bv])
            if v == True or v == False: return v
        al = len(a) == 1
        bl = len(b) == 1
        if al and not bl:
            return True
        elif bl and not al:
            return False
        elif al and bl:
            return None
        a = a[1:]
        b = b[1:]

S = 0
for i in range(len(I)):
    if compare(I[i]):
        S += i + 1
print(S)

I = [eval(x) for x in F if x != ""]
I.append([[2]])
I.append([[6]])

for i in range(len(I)):
    s = True
    for j in range(len(I) - i - 1):
        if not compare([I[j], I[j+1]]):
            I[j], I[j+1] = I[j+1], I[j]
            s = False
    if s:
        break
A, B = 0, 0
for i, v in enumerate(I):
    if v == [[2]]:
        A = i + 1
    elif v == [[6]]:
        B = i + 1
print(A*B)
