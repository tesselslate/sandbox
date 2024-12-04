print(
    (lambda F:
        sum(
            (lambda S: S <= {1, 2, 3} or S <= {-1, -2, -3})
            ({(a - b) for a, b in zip(l[:-1], l[1:])})
            for l in F
        )
    )
    ([[*map(int, l.split())] for l in open("inputs/02").read().split("\n")])
)

print(
    (lambda F:
        sum(
            any(
                (lambda L:
                    (lambda S: S <= {1, 2, 3} or S <= {-1, -2, -3})
                    ({(a - b) for a, b in zip(L[:-1], L[1:])})
                )
                ([l[i] for i in range(len(l)) if i != j]) for j in range(len(l))
            ) for l in F
        )
    )
    ([[*map(int, l.split())] for l in open("inputs/02").read().split("\n")])
)
