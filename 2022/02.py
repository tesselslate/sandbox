F = [l.strip() for l in open("inputs/02")]

sum = 0
for l in F:
    a = l[0]
    b = l[2]
    sum += (ord(b) - ord('X')) + 1
    if (ord(a) - ord('A')) == (ord(b) - ord('X')):
        sum += 3
    elif a == 'A' and b == 'Y':
        sum += 6
    elif a == 'B' and b == 'Z':
        sum += 6
    elif a == 'C' and b == 'X':
        sum += 6
print(sum)

sum = 0
for l in F:
    a = ord(l[0]) - ord('A')
    b = l[2]
    piece = None
    if b == 'X':
        piece = (a-1) % 3
    elif b == 'Y':
        piece = a
        sum += 3
    else:
        piece = (a+1)%3
        sum += 6
    sum += piece + 1
print(sum)
