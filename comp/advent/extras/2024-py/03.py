print(
    (lambda F:
        sum(
            (lambda I:
                int(I[0]) * int(I[1])
                if len(I) == 2 and I[0].isdigit() and I[1].isdigit() else 0
            )
            (F[i+4:F.index(")", i)].split(",")) for i in range(len(F)) if F[i:].startswith("mul(") and ")" in F[i:]
        )
    )
    (open("inputs/03").read())
)

print(
    (lambda F:
        sum(
            (lambda H:
                sum(
                    (lambda I:
                        int(I[0]) * int(I[1])
                        if len(I) == 2 and I[0].isdigit() and I[1].isdigit() else 0
                    )
                    (H[i+4:H.index(")", i)].split(",")) for i in range(len(H)) if H[i:].startswith("mul(") and ")" in H[i:]
                )
            )
            (G.split("don't()")[0]) for G in F.split("do()")[1:]
        )
    )
    ("do()" + open("inputs/03").read())
)
