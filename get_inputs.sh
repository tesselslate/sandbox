#!/usr/bin/bash

mkdir -p $1/inputs
for i in $(seq 1 25); do
    curl -H "Cookie: $2" https://adventofcode.com/$1/day/$i/input --output $1/inputs/$i
    truncate -s -1 $1/inputs/$i # remove trailing newline
done
