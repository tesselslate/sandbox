package main

import (
	"bytes"
	"fmt"
)

func writeRequests(reqs []Request) {
	buf := bytes.Buffer{}
	buf.WriteString(GO_OBS_PACKAGE)
	buf.WriteString(`import(
        "encoding/json"

        "github.com/google/uuid"
    )
    `)

	typebuf := bytes.Buffer{}

	for _, r := range reqs {
		// Write request type.
		buf.WriteString(wrapComment(r.Docs))
		if r.Deprecated != "" {
			buf.WriteString("//\n// Deprecated:\n")
			buf.WriteString(wrapComment(r.Deprecated))
		}
		buf.WriteString(fmt.Sprintf("type %sRequest struct {\n", r.Name))
		buf.WriteString("reqData\n")
		for _, p := range r.Parameters {
			var typeStr string
			if _, ok := p.Type.(StructType); ok {
				typeStr = r.Name + p.Name
				if p.Type.Array() {
					typeStr = "[]" + typeStr
				}
				typebuf.WriteString(fmt.Sprintf("type %s%s ", r.Name, p.Name))
				typebuf.WriteString(p.Type.String())
				typebuf.WriteString("\n\n")
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

		// Write new request function.
		buf.WriteString(fmt.Sprintf("func (c *Client) %s(", r.Name))
		for _, p := range r.Parameters {
			var typeStr string
			if _, ok := p.Type.(StructType); ok {
				typeStr = r.Name + p.Name
				if p.Type.Array() {
					typeStr = "[]" + typeStr
				}
			} else {
				typeStr = p.Type.String()
			}
			buf.WriteString(fmt.Sprintf("%s %s,", p.Name, typeStr))
		}
		buf.WriteString(fmt.Sprintf(") (*%sResponse, error) {", r.Name))
		buf.WriteString(fmt.Sprintf(`
            uuid := uuid.NewString()
            errch := make(chan error)
            defer close(errch)
            req := %sRequest {
                reqData: reqData{
                    MessageId: uuid,
                    RequestType: "%s",
                },
        `, r.Name, r.Name))
		for _, p := range r.Parameters {
			buf.WriteString(fmt.Sprintf("%s: %s,\n", p.Name, p.Name))
		}
		buf.WriteString("}\n")
		buf.WriteString(fmt.Sprintf(`
            jdata, err := json.Marshal(&req)
            if err != nil {
                return nil, err
            }
            recvch := c.send(jdata, uuid, errch)
            defer close(recvch)
            select {
            case val := <-recvch:
                res := &%sResponse{}
                err = json.Unmarshal(val, res)
                if err != nil {
                    return nil, err
                }
                return res, nil
            case err := <-errch:
                return nil, err
            }
        }
        `, r.Name))

		// Write response type.
		buf.WriteString(fmt.Sprintf("type %sResponse struct {\n", r.Name))
		buf.WriteString("resData\n")
		for _, p := range r.Returns {
			typeStr := p.Type.String()
			if p, ok := p.Type.(StructType); ok {
				if p.Array() {
					typeStr = "[]" + typeStr
				}
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
	}
	buf.Write(typebuf.Bytes())
	fmtWrite("./gen_requests.go", buf)
}
