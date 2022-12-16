package main

import (
	"fmt"
	"strconv"
	"strings"
)

type Passport map[string]string

func (p Passport) HasFields() bool {
	keys := []string{"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
	for _, key := range keys {
		if _, ok := p[key]; !ok {
			return false
		}
	}
	return true
}

func (p Passport) Valid() bool {
	if !p.HasFields() {
		return false
	}

	byr, err := strconv.Atoi(p["byr"])
	assert(err)
	if byr < 1920 || byr > 2002 {
		return false
	}

	iyr, err := strconv.Atoi(p["iyr"])
	assert(err)
	if iyr < 2010 || iyr > 2020 {
		return false
	}

	eyr, err := strconv.Atoi(p["eyr"])
	assert(err)
	if eyr < 2020 || eyr > 2030 {
		return false
	}

	hgt := p["hgt"]
	isCm := strings.HasSuffix(hgt, "cm")
	isIn := strings.HasSuffix(hgt, "in")
	if !isIn && !isCm {
		return false
	}
	hgtNum, err := strconv.Atoi(hgt[:len(hgt)-2])
	assert(err)
	if isCm && (hgtNum < 150 || hgtNum > 193) {
		return false
	} else if isIn && (hgtNum < 59 || hgtNum > 76) {
		return false
	}

	hcl := p["hcl"]
	if hcl[0] != '#' {
		return false
	}
	for i := 1; i < 7; i += 1 {
		c := hcl[i]
		isNum := c >= '0' && c <= '9'
		isAl := c >= 'a' && c <= 'f'
		if !isNum && !isAl {
			return false
		}
	}

	validColors := []string{"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
	found := false
	for _, v := range validColors {
		if v == p["ecl"] {
			found = true
			break
		}
	}
	if !found {
		return false
	}

	_, err = strconv.Atoi(p["pid"])
	if err != nil {
		return false
	}
	if len(p["pid"]) != 9 {
		return false
	}
	return true
}

func day04(input string) {
	passports := make([]Passport, 0)
	passport := make(Passport)
	for _, line := range strings.Split(input, "\n") {
		if line == "" {
			passports = append(passports, passport)
			passport = make(Passport)
			continue
		}
		for _, pair := range strings.Split(line, " ") {
			vals := strings.Split(pair, ":")
			passport[vals[0]] = vals[1]
		}
	}
	passports = append(passports, passport)
	day04a(passports)
	day04b(passports)
}

func day04a(input []Passport) {
	sum := 0
	for _, passport := range input {
		if passport.HasFields() {
			sum += 1
		}
	}
	fmt.Println("part 1:", sum)
}

func day04b(input []Passport) {
	sum := 0
	for _, passport := range input {
		if passport.Valid() {
			sum += 1
		}
	}
	fmt.Println("part 2:", sum)
}
