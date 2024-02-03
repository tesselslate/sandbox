package main

import (
	"bytes"
	"fmt"
	"go/format"
	"os"
	"strings"
	"unicode"
)

func writeBindings(p Protocol) {
	writeTypedefs(p.Typedefs)
	writeEvents(p.Events)
	writeRequests(p.Requests)
}

func checkDir(err error) {
	if err == nil || strings.Contains(err.Error(), "file exists") {
		return
	}
	die(err)
}

func fmtWrite(name string, b bytes.Buffer) {
	src, err := format.Source(b.Bytes())
	if err != nil {
		fmt.Println(b.String())
		panic(err)
	}
	check(os.WriteFile(name, src, FILE_PERMS))
}

func camelPascal(i string) string {
	out := []byte{}
	word := []byte{}

	if unicode.IsUpper(rune(i[0])) {
		return i
	}

	for _, c := range i {
		if unicode.IsUpper(c) || c == '-' || c == '_' {
			word[0] = byte(unicode.ToUpper(rune(word[0])))
			out = append(out, word...)
			word = []byte{}
		}

		if c != '-' && c != '_' {
			word = append(word, byte(c))
		}
	}

	word[0] = byte(unicode.ToUpper(rune(word[0])))
	out = append(out, word...)
	return string(out)
}

func wrapComment(c string) string {
	if c == "" {
		return ""
	}

	words := strings.Split(strings.ReplaceAll(c, "\n", " "), " ")
	out := []string{}

	line := "//"
	for _, w := range words {
		if len(line)+len(w) > 79 {
			out = append(out, line)
			line = "//"
		}

		line += " " + w
	}

	if line != "//" {
		out = append(out, line)
	}

	return strings.Join(out, "\n") + "\n"
}
