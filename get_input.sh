#!/usr/bin/bash

mkdir -p $1/inputs
filename="$1/inputs/$(printf %02d $2)"

curl -A "github.com/woofdoggo (woofwoofdoggo@protonmail.com : read infrequently)" \
    -H "Cookie: session=$AOC_TOKEN" \
    https://adventofcode.com/$1/day/$2/input \
    --output $filename

# remove trailing newline
truncate -s -1 $filename
