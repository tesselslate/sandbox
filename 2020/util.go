package main

import (
	"strconv"
	"strings"
)

func NumSlice(input string) []int {
	out := make([]int, 0)
	for _, v := range strings.Split(input, "\n") {
		if v == "" {
			continue
		}
		num, err := strconv.Atoi(v)
		assert(err)
		out = append(out, num)
	}
	return out
}
