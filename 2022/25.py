from sys import argv

F = [l.strip() for l in open(argv[1])]
D = {
        '0': 0,
        '1': 1,
        '2': 2,
        '-': -1,
        '=': -2
}

S = 0
for l in F:
    for i in range(-len(l), 0):
        S += D[l[i]] * (5 ** (-i-1))

print(S)
# i converted mine by hand (2-==10===-12=2-1=-=0)
# did not like this problem at all
