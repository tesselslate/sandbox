//go:build ignore

package main

import (
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	args := os.Args[1:]
	for i, arg := range args {
		// Skip -- command line separator
		if arg == "--" {
			continue
		}

		abs, err := filepath.Abs(arg)
		if err != nil {
			fmt.Println("Get abs path:", err)
			return
		}
		sym, err := filepath.EvalSymlinks(arg)
		if err != nil {
			fmt.Println("Resolve links:", err)
			return
		}
		absym, err := filepath.EvalSymlinks(abs)
		if err != nil {
			fmt.Println("Resolve links (absolute):", err)
			return
		}

		fmt.Printf("==== Arg %d: %q\n", i, arg)
		fmt.Println("filepath.Clean:        ", filepath.Clean(arg))
		fmt.Println("filepath.Abs:          ", abs)
		fmt.Println("filepath.EvalSymlinks: ", sym)
		fmt.Println("abs + symlinks:        ", absym)
	}
}
