print(
    (lambda R, P:
        (lambda R, P:
            sum(p[len(p)//2] for p in P if all((a,b) in R for a, b in zip(p[:-1], p[1:])))
        )
        ([tuple(int(x) for x in l.split("|")) for l in R], [tuple(int(x) for x in l.split(",")) for l in P])
    )
    (*[[l for l in xs.split("\n") if l != ""] for xs in open("inputs/05").read().split("\n\n")])
)

print(
    (lambda R, P:
        (lambda R, P:
            sum(
                (lambda: list(sorted(p, key=type(
                    "rulesort",
                    (int,object),
                    {
                        "__lt__": lambda self, other: (int(self), int(other)) in R
                    }
                ))))
                ()[len(p)//2]
                for p in P if not all((a,b) in R for a, b in zip(p[:-1], p[1:]))
            )
        )
        ([tuple(int(x) for x in l.split("|")) for l in R], [tuple(int(x) for x in l.split(",")) for l in P])
    )
    (*[[l for l in xs.split("\n") if l != ""] for xs in open("inputs/05").read().split("\n\n")])
)
