#!/usr/bin/bash

mkdir -p $1/inputs
for i in $(seq 1 2); do
    filename="$1/inputs/$(printf %02d $i)"
    curl -H "Cookie: $2" https://adventofcode.com/$1/day/$i/input --output $filename
    # remove trailing newline
    truncate -s -1 $filename
done
