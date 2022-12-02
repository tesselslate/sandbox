F = [l.strip() for l in open("inputs/03")]

claims = [[0]*1000 for i in range(1000)]
for l in F:
    words = l.split(" ")
    I = words[2].strip(":").split(",")
    x, y = int(I[0]), int(I[1])
    I = words[3].split("x")
    w, h = int(I[0]), int(I[1])
    for i in range(x, x+w):
        for j in range(y, y+h):
            claims[i][j] += 1
sum = 0
for i in range(1000):
    for j in range(1000):
        if claims[i][j] > 1:
            sum += 1
print(sum)

for l in F:
    words = l.split(" ")
    I = words[2].strip(":").split(",")
    x, y = int(I[0]), int(I[1])
    I = words[3].split("x")
    w, h = int(I[0]), int(I[1])
    good = True
    for i in range(x, x+w):
        for j in range(y, y+h):
            if claims[i][j] > 1:
                good = False
    if good:
        print(l)
        quit()
