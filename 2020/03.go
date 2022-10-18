package main

import (
	"fmt"
	"strings"
)

type TreeMap struct {
	Width  int
	Height int
	Matrix [][]bool
}

func (t *TreeMap) Slope(a, b int) int {
	count := 0
	x, y := 0, 0
	for y < t.Height {
		if t.Matrix[y][x%t.Width] {
			count += 1
		}
		x += a
		y += b
	}
	return count
}

func day03(input string) {
	rows := strings.Split(input, "\n")
	width := len(rows[0])
	height := len(rows)
	matrix := make([][]bool, 0)
	for _, line := range rows {
		row := make([]bool, 0)
		for _, char := range line {
			row = append(row, char == '#')
		}
		matrix = append(matrix, row)
	}
	treeMap := TreeMap{width, height, matrix}
	day03a(treeMap)
	day03b(treeMap)
}

func day03a(input TreeMap) {
	fmt.Println("part 1:", input.Slope(3, 1))
}

func day03b(input TreeMap) {
	count := 1
	slopes := [][2]int{
		{1, 1},
		{3, 1},
		{5, 1},
		{7, 1},
		{1, 2},
	}
	for _, v := range slopes {
		count *= input.Slope(v[0], v[1])
	}
	fmt.Println("part 2:", count)
}
