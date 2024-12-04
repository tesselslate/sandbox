print(
    (lambda F: sum(abs(a-b) for a, b in zip(sorted(F[::2]), sorted(F[1::2]))))
    ([*map(int, open("inputs/01").read().split())])
)

print(
    (lambda F: sum(a * sum(1 if x == a else 0 for x in F[1::2]) for a in F[::2]))
    ([*map(int, open("inputs/01").read().split())])
)
