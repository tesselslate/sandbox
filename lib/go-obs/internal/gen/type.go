package main

import "fmt"

type Type interface {
	fmt.Stringer
	Optional() bool
	Array() bool
}

type BasicType struct {
	name     string
	optional bool
	array    bool
}

func (t BasicType) String() string {
	var n string
	if t.array {
		n = "[]" + t.name
	} else {
		n = t.name
	}

	if t.optional {
		if !t.array && t.name != "string" && t.name != "interface{}" {
			return "*" + n
		}
	}
	return n
}

func (t BasicType) Optional() bool {
	return t.optional
}

func (t BasicType) Array() bool {
	return t.array
}

type StructType struct {
	children []Property
	optional bool
	array    bool
}

func (t StructType) String() string {
	out := "struct {\n"
	for _, p := range t.children {
		out += fmt.Sprintf(
			"%s%s %s `json:\"%s\"`\n",
			wrapComment(p.Docs),
			p.Name,
			p.Type.String(),
			p.JsonTag,
		)
	}
	out += "}"
	return out
}

func (t StructType) Optional() bool {
	return t.optional
}

func (t StructType) Array() bool {
	return t.array
}
