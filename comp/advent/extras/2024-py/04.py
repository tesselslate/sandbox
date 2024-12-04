print(
    (lambda F:
        (lambda G: sum(
            (1 if all(G(r+d[0]*i, c+d[1]*i) == ch for i, ch in enumerate("XMAS")) else 0)
            for d in [(-1,0),(1,0),(0,-1),(0,1),(1,1),(1,-1),(-1,1),(-1,-1)] for c in range(len(F)) for r in range(len(F))
        ))
        (lambda r, c: F[r][c] if r >= 0 and c >= 0 and r < len(F) and c < len(F) else '.')
    )
    (open("inputs/04").read().split("\n"))
)

print(
    (lambda F, S:
        sum([
            (lambda A, G:
                sum(map(
                    lambda x: 0,
                    (
                        A(r+d[0], c+d[1], 1 if all(G(r+d[0]*i, c+d[1]*i) == ch for i, ch in enumerate("MAS")) else 0)
                        for d in [(1,1),(1,-1),(-1,1),(-1,-1)] for c in range(len(F)) for r in range(len(F))
                    )
                ))
            )
            (
                lambda r, c, i: (S.__setitem__((r,c), i) if (r,c) not in S else S.__setitem__((r,c), S[(r,c)] + i)),
                lambda r, c: F[r][c] if r >= 0 and c >= 0 and r < len(F) and c < len(F) else '.'
            ),
            sum(1 for v in S.values() if v == 2)
        ])
    )
    (open("inputs/04").read().split("\n"), {})
)
