//go:build ignore

package main

//go:noinline
func makeMap() map[string]bool {
	return make(map[string]bool)
}

func main() {
	m := makeMap()
	if !m["1"] {
		m["1"] = false
	}

	m2 := make(map[string]bool)
	if !m2["1"] {
		m2["1"] = false
	}

	println(len(m), len(m2))
}
