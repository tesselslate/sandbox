#!/usr/bin/fish

if test -n $argv[1]
    set aoc_day $argv[1]
else
    set aoc_day (date +%d)
end
set zday (printf %02d $aoc_day)
echo "Day $aoc_day ($zday)"

mkdir -p inputs
curl -A "github.com/tesselslate" \
    -H "Cookie: session=$AOC_TOKEN" \
    "https://adventofcode.com/$(basename $PWD)/day/$aoc_day/input" \
    --output inputs/$zday

truncate -s -1 inputs/$zday
