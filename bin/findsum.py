import functools, sys

if len(sys.argv) < 3:
    print("findsum.py [TARGET] [NUMBERS...]")
    exit(1)

target = int(sys.argv[1])
numbers = sorted(int(x) for x in sys.argv[2:])

best_solution = None

@functools.cache
def dfs(target, used):
    global best_solution

    if best_solution and used.bit_count() > len(best_solution):
        return

    if target == 0:
        used_numbers = [
            numbers[i] for i in range(used.bit_length())
            if used & (1 << i)
        ]

        best_solution = tuple(sorted(used_numbers))
        return

    for i in range(len(numbers)):
        if numbers[i] > target:
            continue

        mask = 1 << i
        if mask & used:
            continue

        dfs(target - numbers[i], used | mask)

dfs(target, 0)

if best_solution:
    print(" ".join(str(x) for x in best_solution))
else:
    print("No solution")
