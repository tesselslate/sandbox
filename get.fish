#!/usr/bin/fish

if test -z "$argv[1]"
    set aoc_day (date +%d)
    echo "No day provided, defaulting to $aoc_day"
else
    set aoc_day $argv[1]
end
set zday (printf %02d $aoc_day)

set year (basename $PWD)
if test "$year" = "advent"
    set year (date +%Y)
end

echo "$year/$aoc_day ($zday)"

mkdir -p inputs
curl -A "github.com/tesselslate" \
    -H "Cookie: session=$AOC_TOKEN" \
    "https://adventofcode.com/$year/day/$aoc_day/input" \
    --output inputs/$zday

truncate -s -1 inputs/$zday
