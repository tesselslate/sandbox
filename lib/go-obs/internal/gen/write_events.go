package main

import (
	"bytes"
	"fmt"
)

func writeEvents(events []Event) {
	buf := bytes.Buffer{}
	buf.WriteString(GO_OBS_PACKAGE)
	buf.WriteString("import \"encoding/json\"\n\n")
	convBuf := bytes.Buffer{}
	convBuf.WriteString("var eventConverters = map[string]func([]byte) any {\n")

	for _, e := range events {
		buf.WriteString(wrapComment(e.Docs))
		buf.WriteString(fmt.Sprintf("type %sEvent struct {\n", e.Name))
		buf.WriteString("eventData\n")
		for _, p := range e.Returns {
			var typeStr string
			if _, ok := p.Type.(StructType); ok {
				typeStr = p.Type.String()
				if p.Type.Array() {
					typeStr = "[]" + typeStr
				}
			} else {
				typeStr = p.Type.String()
			}
			str := fmt.Sprintf(
				"%s%s %s `json:\"%s\"`\n",
				wrapComment(p.Docs),
				p.Name,
				typeStr,
				p.JsonTag,
			)
			buf.WriteString(str)
		}
		buf.WriteString("}\n\n")
		convBuf.WriteString(fmt.Sprintf(
			`"%s": func(data []byte) any {
            evt := &%sEvent{}
            err := json.Unmarshal(data, evt)
            if err != nil {
                return nil
            }
            return evt
        },
        `, e.Name, e.Name))
	}
	convBuf.WriteRune('}')
	buf.Write(convBuf.Bytes())
	fmtWrite("./gen_events.go", buf)
}
