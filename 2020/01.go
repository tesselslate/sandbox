package main

import "fmt"

func day01(input string) {
	day01a(input)
	day01b(input)
}

func day01a(inputStr string) {
	input := NumSlice(inputStr)
	for i, x := range input {
		for j, y := range input {
			if i == j {
				continue
			}
			if x+y == 2020 {
				fmt.Println("part 1:", x*y)
				return
			}
		}
	}
}

func day01b(inputStr string) {
	input := NumSlice(inputStr)
	for i, x := range input {
		for j, y := range input {
			for k, z := range input {
				if i == j || j == k || i == k {
					continue
				}
				if x+y+z == 2020 {
					fmt.Println("part 2:", x*y*z)
					return
				}
			}
		}
	}
}
