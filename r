#!/usr/bin/fish

# TODO: fix for manual day number
set aoc_day (date +%d)
set aoc_day (printf %02d $aoc_day)
echo "Day $aoc_day"

# p = paste and run
# s = store clipboard into test file
# t = run all test files
# tl = run latest test file
# default = run input

switch $argv[1]
    case "p"
        set aoc_file (mktemp)
        wl-paste | tee $aoc_file > /dev/null
        pypy3 $aoc_day.py $aoc_file
        rm $aoc_file
    case "s"
        set aoc_index 0
        while true
            set aoc_index (math $aoc_index + 1)
            if not test -e test$aoc_index
                echo "Storing in test $aoc_index"
                wl-paste | tee test$aoc_index > /dev/null
                exit 0
            end
        end
    case "t"
        for f in test*:
            echo "Running test $aoc_index"
            pypy3 ./$aoc_day.py $f
            echo
        end
    case "tl"
        set aoc_test_file (command ls -1 | grep test | tail -n 1)
        if test -n "$aoc_test_file"
            echo "Running test $aoc_index"
            pypy3 ./$aoc_day.py $aoc_test_file
        else
            echo "No test file found"
        end
    case "*"
        echo "Running input"
        pypy3 ./$aoc_day.py inputs/$aoc_day
end
