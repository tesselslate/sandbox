from sys import argv

F = [l.strip() for l in open(argv[1])][0]
S = 0

for i in range(len(F) - 4 + 1):
    c = F[i:i+4]
    if len(set(c)) == 4:
        print(i+4)
        break

for i in range(len(F) - 14 + 1):
    c = F[i:i+14]
    if len(set(c)) == 14:
        print(i+14)
        break
