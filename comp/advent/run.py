#!/usr/bin/python

from datetime import date
from enum import IntEnum
from subprocess import PIPE
from time import ctime, time
import os, re, subprocess, sys, tempfile


class Mode(IntEnum):
    INPUT = 0
    PASTE = 1
    STORE = 2
    TESTS = 3
    TESTL = 4
    ALL = 5


day = None
mode = Mode.INPUT
for arg in sys.argv[1:]:
    if arg.isdigit():
        if day is not None:
            print("Multiple days specified. Terminating")
            exit(1)
        day = int(arg)
    else:
        match arg:
            case "p":
                mode = Mode.PASTE
            case "s":
                mode = Mode.STORE
            case "t":
                mode = Mode.TESTS
            case "tl":
                mode = Mode.TESTL
            case "all":
                mode = Mode.ALL
            case _:
                print("Unknown mode:", arg)

if day is None:
    day = date.today().day
padded_day = str(day).zfill(2)


def run_solution(input_file, solution_name=padded_day, output=True):
    if output:
        print(f"Started at: {ctime()}")
        print()
        print("\x1b[1;32m  -- stdout\x1b[0m")

    process = subprocess.Popen(
        ["pypy3", f"{solution_name}.py"],
        stdout=sys.stdout if output else PIPE,
        stdin=PIPE,
        stderr=PIPE,
    )

    with open(input_file, "r") as file:
        start = time()
        _, stderr = process.communicate(input=bytes(file.read(), "utf8"))
        stop = time()

        if output:
            print("\x1b[1;32m  --\x1b[0m\n")
            if stderr:
                stderr = stderr.decode("utf8")
                print(
                    f"\x1b[1;31m  -- stderr\x1b[0m\x1b[31m\n{stderr}\x1b[1;31m  --\x1b[0m\n"
                )
            print(f"  took {(stop-start):.3f} sec\n")

        return not bool(stderr)


def get_tests():
    return list(sorted([name for name in os.listdir() if name.startswith("test")]))


def new_testfile():
    tests = get_tests()

    n = len(tests) + 1
    if tests:
        assert int(tests[-1].removeprefix("test")) == n - 1
    return f"test{n}"


match mode:
    case Mode.INPUT:
        print(f"Running {day} (input)")

        run_solution(f"inputs/{padded_day}")

    case Mode.PASTE:
        print(f"Running {day} (clipboard)")

        wl_paste = subprocess.Popen(["wl-paste"], stdout=PIPE)
        stdout, stderr = wl_paste.communicate()
        assert not stderr

        filename = tempfile.mktemp()
        assert filename.startswith("/tmp")

        stdout = stdout.decode("utf8")
        with open(filename, "w") as file:
            file.write(stdout)
        print(f"\n\x1b[1;36m  -- INPUT\x1b[0m\n{stdout}\x1b[1;36m  --\x1b[0m\n")
        run_solution(filename)
        os.remove(filename)

    case Mode.STORE:
        test_name = new_testfile()
        print(f"Storing clipboard to {test_name}")

        wl_paste = subprocess.Popen(["wl-paste"], stdout=PIPE)
        stdout, stderr = wl_paste.communicate()
        assert not stderr

        stdout = stdout.decode("utf8")
        with open(test_name, "w") as file:
            file.write(stdout)
        print(f"\n\x1b[1;36m  -- INPUT\x1b[0m\n{stdout}\x1b[1;36m  --\x1b[0m\n")
        print(f"  pasted {len(stdout.splitlines())} lines to {test_name}\n")

    case Mode.TESTS:
        print(f"Running {day} (all tests)\n")

        tests = get_tests()
        if not tests:
            print("No tests to run.")
            exit(0)

        results = []
        start = time()
        print(
            "\x1b[1;36m  ---------------------------------------------------------\x1b[0m\n"
        )
        for test in tests:
            print(f"Running input:", test)
            results.append(run_solution(test))
            print(
                "\x1b[1;36m  ---------------------------------------------------------\x1b[0m\n"
            )
        stop = time()

        if all(results):
            print(
                f"\x1b[1;32m  OK   ({len(results)} / {len(results)}, took {(stop-start):.3f} sec)\n"
            )
        else:
            print(
                f"\x1b[1;31m  FAIL ({results.count(True)} / {len(results)} passed, took {(stop-start):.3f} sec)"
            )
            for i, result in enumerate(results):
                print(
                    f"\x1b{'[1;32m  OK  ' if result else '[1;31m  FAIL'} \x1b[0mTest {i+1}"
                )

    case Mode.TESTL:
        tests = get_tests()
        if not tests:
            print("No tests")
            exit(1)
        test_name = list(sorted(tests))[-1]
        print(f"Running {day} (latest test: {test_name})")
        run_solution(test_name)

    case Mode.ALL:
        solutions = list(
            sorted([name for name in os.listdir() if re.match(r"(\d+).py", name)])
        )

        times = []
        ok = []
        start = time()
        for solution in solutions:
            day = solution.split(".")[0]
            sol_start = time()
            ok.append(
                run_solution(
                    f"inputs/{day.zfill(2)}", solution_name=day.zfill(2), output=False
                )
            )
            sol_stop = time()
            times.append(sol_stop - sol_start)
        stop = time()

        sys.stdout = sys.__stdout__

        avg = sum(times) / len(times)
        min, max = min(times), max(times)

        print(f"\x1b[1;36m  TOTAL: \x1b[0m{(stop-start):.3f} sec")
        print(f"\x1b[1;36m  AVG:   \x1b[0m{avg:.3f} sec")
        print(f"\x1b[1;36m  MIN:   \x1b[0m{min:.3f} sec (day {times.index(min)+1})")
        print(f"\x1b[1;36m  MAX:   \x1b[0m{max:.3f} sec (day {times.index(max)+1})")
        for i, x in enumerate(zip(ok, times)):
            (ok, time) = x
            if ok:
                print(f"\x1b[1;32m  PASS   {str(i+1).zfill(2)}  {time:.3f} sec")
            else:
                print(f"\x1b[1;31m  FAIL   {str(i+1).zfill(2)}")

    case _:
        assert False
