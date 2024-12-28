print(
    (lambda F:
        (lambda G, P, D:
            len({
                (lambda G, P, D, N:
                    (
                        (P.__setitem__(0, N[0]) or P.__setitem__(1, N[1]) or N)
                        if G[N] != "#" else
                        (D.__setitem__(2, D[0]) or D.__setitem__(0, D[1]) or D.__setitem__(1, -D[2]) or None)
                    )
                    if N in G else None
                )
                (G, P, D, (P[0] + D[0], P[1] + D[1])) for i in range(100000)
            } - {None})
        )
        (
            {(r,c): F[r][c] for r in range(len(F)) for c in range(len(F[0]))},

            (lambda STL: [STL, F[STL].index("^")])
            ([i for (i,l) in enumerate(F) if "^" in l][0]),

            [-1, 0, None],
        )
    )
    (open("inputs/06").read().split("\n"))
)

print(
    (lambda F:
        (lambda G, P, D:
            (lambda G, P, D:
                sum(
                    (lambda G, P, D, O:
                        (lambda V:
                            any(V.count(x) > 1 for x in V if V.count(x) > 1)
                        )
                        ([
                            (lambda G, P, D, N, O:
                                (
                                    (P.__setitem__(0, N[0]) or P.__setitem__(1, N[1]) or (tuple(N), tuple(D)))
                                    if G[N] != "#" and N != O else
                                    (D.__setitem__(2, D[0]) or D.__setitem__(0, D[1]) or D.__setitem__(1, -D[2]) or (tuple(P), tuple(D)))
                                )
                                if N in G else None
                            )
                            (G, P, D, (P[0] + D[0], P[1] + D[1]), O)
                            for i in range(100000)
                        ])
                    )
                    (
                        G,
                        [P[0], P[1]],
                        [D[0], D[1], D[2]],
                        (r, c)
                    )
                    for (r,c) in
                    {
                        (lambda G, P, D, N:
                            (
                                (P.__setitem__(0, N[0]) or P.__setitem__(1, N[1]) or N)
                                if G[N] != "#" else
                                (D.__setitem__(2, D[0]) or D.__setitem__(0, D[1]) or D.__setitem__(1, -D[2]) or None)
                            )
                            if N in G else None
                        )
                        (
                            G,
                            [P[0], P[1]],
                            [D[0], D[1], D[2]],
                            (P[0] + D[0], P[1] + D[1])
                        )
                        for i in range(100000)
                    } - {None, tuple(P)}
                )
            )
            (G, P, D)
        )
        (
            {(r,c): F[r][c] for r in range(len(F)) for c in range(len(F[0]))},

            (lambda STL: [STL, F[STL].index("^")])
            ([i for (i,l) in enumerate(F) if "^" in l][0]),

            [-1, 0, None],
        )
    )
    (open("inputs/06").read().split("\n"))
)

# print(
#     (lambda F:
#         (lambda G, P, D:
#             (lambda G, P, D:
#                 len({
#                     (r,c)
#                     for (r,c) in
#                     ({
#                         (lambda G, P, D, V, N:
#                             (
#                                 (P.__setitem__(0, N[0]) or P.__setitem__(1, N[1]) or N)
#                                 if G[N] != "#" else
#                                 (D.__setitem__(2, D[0]) or D.__setitem__(0, D[1]) or D.__setitem__(1, -D[2]) or None)
#                             )
#                             if N in G else None
#                         )
#                         (G, [P[0], P[1]], [D[0], D[1], D[2]], set(), (P[0] + D[0], P[1] + D[1]))
#                         for i in range(100000)
#                     } - {None})
#                     if
#                     (lambda G, P, D, r, c:
#                         tuple(P) != (r,c) and
#                         (lambda X: any(X.count(x) > 1 for x in X))
#                         ([
#                             (lambda G, P, D, V, N:
#                                 (
#                                     (P.__setitem__(0, N[0]) or P.__setitem__(1, N[1]) or (tuple(N), tuple(D)))
#                                     if G[N] != "#" and N != (r,c) else
#                                     (D.__setitem__(2, D[0]) or D.__setitem__(0, D[1]) or D.__setitem__(1, -D[2]) or (tuple(P), tuple(D)))
#                                 )
#                                 if N in G else None
#                             )
#                             (G, [P[0], P[1]], [D[0], D[1], D[2]], set(), (P[0] + D[0], P[1] + D[1])) for i in range(100000)
#                         ])
#                     )
#                     (G, P, D, r, c)
#                 })
#             )
#             (G,P,D)
#         )
#         (
#             {(r,c): F[r][c] for r in range(len(F)) for c in range(len(F[0]))},
#
#             (lambda STL: [STL, F[STL].index("^")])
#             ([i for (i,l) in enumerate(F) if "^" in l][0]),
#
#             [-1, 0, None],
#         )
#     )
#     (open("inputs/06").read().split("\n"))
# )
