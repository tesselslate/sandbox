package main

import (
	"bytes"
	"fmt"
)

func writeTypedefs(defs []Typedef) {
	buf := bytes.Buffer{}
	buf.WriteString(GO_OBS_PACKAGE)

	for _, t := range defs {
		buf.WriteString(wrapComment(t.Docs))
		buf.WriteString(fmt.Sprintf("type %s struct {\n", t.Name))
		for _, p := range t.Properties {
			str := fmt.Sprintf(
				"%s%s %s\n",
				wrapComment(p.Docs),
				p.Name,
				p.Type.String(),
			)
			buf.WriteString(str)
		}
		buf.WriteString("}\n\n")
	}

	fmtWrite("./gen_types.go", buf)
}
