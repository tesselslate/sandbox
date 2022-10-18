package main

import (
	"os"
	"strconv"
)

var days = []func(string){
	day01,
	day02,
    day03,
}

func assert(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	if len(os.Args) < 2 {
		os.Exit(1)
	}
	challenge, err := strconv.Atoi(os.Args[1])
	assert(err)
	if challenge < 1 || challenge > 25 {
		os.Exit(1)
	}
	content, err := os.ReadFile("./inputs/" + os.Args[1])
	assert(err)
	days[challenge-1](string(content))
}
