import ul

F = ul.input()

def area(border, border_len):
    return int(ul.shoelace(border)) + border_len//2 + 1

border1, border2 = [(0,0)], [(0,0)]
len1, len2 = 0, 0
p1, p2 = (0, 0), (0, 0)
for l in F:
    dir, n, x = ul.scan("%s %d (#%s)", l)

    d = ul.dirs_rc(dir)[0]
    p1 = (p1[0] + d[0]*n, p1[1] + d[1]*n)
    border1.append(p1)
    len1 += n

    d = ul.dirs_rc("RDLU"[int(x[-1])])[0]
    n = int(x[:5], 16)
    p2 = (p2[0] + d[0]*n, p2[1] + d[1]*n)
    border2.append(p2)
    len2 += n
print(area(border1, len1))
print(area(border2, len2))
