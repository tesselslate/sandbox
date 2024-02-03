package main

import (
	"fmt"
	"os"

	"github.com/tesselslate/sandbox/bin/taskman/tui"
)

func main() {
	// Get the tasks file path.
	doc, exists := os.LookupEnv("XDG_DOCUMENTS_DIR")
	if !exists {
		home, err := os.UserHomeDir()
		if err != nil {
			fmt.Println("Failed to get documents directory:", err)
			os.Exit(1)
		}
		doc = home + "/Documents"
	}

	// Run taskman.
	app, err := tui.NewApp(doc + "/.todo")
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	err = app.Run()
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
