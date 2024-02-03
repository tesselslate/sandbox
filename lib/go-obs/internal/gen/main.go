package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
)

const FILE_PERMS = 0644
const GO_OBS_PACKAGE = "package go_obs\n\n"

func main() {
	// Read protocol definition JSON.
	if len(os.Args) < 2 {
		die("Need a path to protocol definitions.")
	}

	path := os.Args[1]
	contents, err := ioutil.ReadFile(path)
	check(err)

	jProto := &JsonProtocol{}
	check(json.Unmarshal(contents, jProto))

	// Convert JSON protocol definitions into a more usable form.
	proto := convert(jProto)

	// Generate protocol bindings.
	writeBindings(proto)
}

// Function check exits the program if the provided error is not nil.
func check(err error) {
	if err != nil {
		die(err)
	}
}

// Function die exits the program with the given error message.
func die(msg ...any) {
	if len(msg) == 1 {
		panic(fmt.Sprint(msg[0]))
	}

	switch v := msg[0].(type) {
	case string:
		panic(fmt.Sprintf(v, msg...))
	default:
		panic(fmt.Sprintf("die received type %T", msg[0]))
	}
}
