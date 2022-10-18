package main

import (
	"fmt"
	"strconv"
	"strings"
)

type Password struct {
	A    int
	B    int
	Char rune
	Pw   string
}

func (p *Password) ValidateRange() bool {
	count := 0
	for _, c := range p.Pw {
		if c == p.Char {
			count += 1
		}
	}
	return count >= p.A && count <= p.B
}

func (p *Password) ValidatePosition() bool {
	b := byte(p.Char)
	first := p.Pw[p.A-1] == b
	second := p.Pw[p.B-1] == b
	return (first || second) && (first != second)
}

func day02(input string) {
	passwords := make([]Password, 0)
	for _, v := range strings.Split(input, "\n") {
		words := strings.Split(v, " ")
		nums := strings.Split(words[0], "-")
		a, err := strconv.Atoi(nums[0])
		assert(err)
		b, err := strconv.Atoi(nums[1])
		assert(err)
		char := words[1][0]
		password := words[2]
		pw := Password{a, b, rune(char), password}
		passwords = append(passwords, pw)
	}
	day02a(passwords)
	day02b(passwords)
}

func day02a(input []Password) {
	valid := 0
	for _, pw := range input {
		if pw.ValidateRange() {
			valid += 1
		}
	}
	fmt.Println("part 1:", valid)
}

func day02b(input []Password) {
	valid := 0
	for _, pw := range input {
		if pw.ValidatePosition() {
			valid += 1
		}
	}
	fmt.Println("part 2:", valid)
}
