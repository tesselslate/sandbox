package main

import (
	"sort"
	"strings"
)

var typeMapping = map[string]string{
	"number":  "float64",
	"double":  "float64",
	"float":   "float32",
	"int":     "int",
	"integer": "int",
	"string":  "string",
	"boolean": "bool",
	"bool":    "bool",
	"object":  "interface{}",
}

// Function convert converts a JsonProtocol object into an instance of
// the more easily usable Protocol type.
func convert(j *JsonProtocol) Protocol {
	proto := Protocol{
		Typedefs: make([]Typedef, len(j.Typedefs)),
		Events:   []Event{},
		Requests: []Request{},
	}

	for i, v := range j.Typedefs {
		proto.Typedefs[i] = convertTypedef(v)
	}

	for _, v := range j.Events {
		for _, e := range v {
			proto.Events = append(proto.Events, convertEvent(e))
		}
	}
	sort.Slice(proto.Events, func(a, b int) bool {
		return proto.Events[a].Name < proto.Events[b].Name
	})

	for _, v := range j.Requests {
		for _, r := range v {
			proto.Requests = append(proto.Requests, convertRequest(r))
		}
	}
	sort.Slice(proto.Requests, func(a, b int) bool {
		return proto.Requests[a].Name < proto.Requests[b].Name
	})

	return proto
}

func convertTypedef(t JsonTypedef) Typedef {
	def := t.Definition[0]
	out := Typedef{
		Name:       def.Name,
		Docs:       def.Docs,
		Properties: make([]Property, len(t.Properties)),
	}
	out.Properties = convertProperties(t.Properties)
	return out
}

func convertEvent(e JsonEvent) Event {
	out := Event{
		Name:    e.Name,
		Docs:    e.Docs,
		Returns: make([]Property, len(e.Returns)),
	}
	out.Returns = convertProperties(e.Returns)
	return out
}

func convertRequest(r JsonRequest) Request {
	out := Request{
		Name:       r.Name,
		Docs:       r.Docs,
		Deprecated: r.Deprecated,
		Parameters: make([]Property, len(r.Parameters)),
		Returns:    make([]Property, len(r.Returns)),
	}
	out.Parameters = convertProperties(r.Parameters)
	out.Returns = convertProperties(r.Returns)
	return out
}

func convertProperties(props []JsonProperty) []Property {
	out := []Property{}

	// Check for embedded struct types.
	embeds := make(map[string]StructType)
	for _, v := range props {
		if strings.ContainsRune(v.Name, '.') {
			parts := strings.Split(v.Name, ".")

			// HACK: Handle the **single case** in the entire protocol of
			// doubly-nested anonymous structs. Thanks, OBS websocket
			// developers! (:
			if len(parts) == 4 {
				if parts[0] != "types" || parts[2] != "caps" {
					die("new doubly nested type")
				}
				continue
			}

			if len(parts) == 3 && parts[0] == "types" && parts[2] == "caps" {
				t := embeds[parts[0]]
				t.children = append(t.children, Property{
					Name:    "Caps",
					JsonTag: "caps",
					Docs:    "Source type capabilities",
					Type: StructType{
						[]Property{
							{
								Name:    "IsAsync",
								JsonTag: "isAsync",
								Docs:    "True if source of this type provide frames asynchronously",
								Type: BasicType{
									name: "bool",
								},
							},
							{
								Name:    "HasVideo",
								JsonTag: "hasVideo",
								Docs:    "True if sources of this type provide video",
								Type: BasicType{
									name: "bool",
								},
							},
							{
								Name:    "HasAudio",
								JsonTag: "hasAudio",
								Docs:    "True if sources of this type provide audio",
								Type: BasicType{
									name: "bool",
								},
							},
							{
								Name:    "CanInteract",
								JsonTag: "canInteract",
								Docs:    "True if interaction with this sources of this type is possible",
								Type: BasicType{
									name: "bool",
								},
							},
							{
								Name:    "IsComposite",
								JsonTag: "isComposite",
								Docs:    "True if sources of this type composite one or more sub-sources",
								Type: BasicType{
									name: "bool",
								},
							},
							{
								Name:    "DoNotDuplicate",
								JsonTag: "doNotDuplicate",
								Docs:    "True if sources of this type should not be fully duplicated",
								Type: BasicType{
									name: "bool",
								},
							},
							{
								Name:    "DoNotSelfMonitor",
								JsonTag: "doNotSelfMonitor",
								Docs:    "True if sources of this type may cause a feedback loop if it's audio is monitored and shouldn't be",
								Type: BasicType{
									name: "bool",
								},
							},
						},
						false,
						false,
					},
				})
				embeds[parts[0]] = t
				continue
			}

			// Check if this is an *array* of anonymous structs.
			isArray := len(parts) >= 3

			var t StructType
			if val, ok := embeds[parts[0]]; ok {
				t = val
			} else {
				t = StructType{
					[]Property{},
					false,
					isArray,
				}
			}

			part := parts[len(parts)-1]
			ct := convertType(v.Type)
			var jt string
			if ct.optional {
				jt = part + ",omitempty"
			} else {
				jt = part
			}

			newProp := Property{
				Name:    camelPascal(part),
				JsonTag: jt,
				Docs:    v.Docs,
				Type:    ct,
			}

			t.children = append(t.children, newProp)
			embeds[parts[0]] = t
		}
	}

	// Convert properties.
	// HACK: This loop contains a hackfix for one of several wonderful quirks
	// in the OBS websocket protocol definition. Anonymous structs may or may
	// not include an initial definition, so we have to check if we must write
	// them when looping over every single one of their members as well.
	written := make(map[string]struct{})
	for _, v := range props {
		// Skip members of embedded types.
		if strings.ContainsRune(v.Name, '.') {
			parts := strings.Split(v.Name, ".")
			if _, ok := written[parts[0]]; !ok {
				var jt string
				if embeds[parts[0]].Optional() {
					jt = parts[0] + ",omitmepty"
				} else {
					jt = parts[0]
				}
				out = append(out, Property{
					Name:    camelPascal(parts[0]),
					JsonTag: jt,
					Docs:    v.Docs,
					Type:    embeds[parts[0]],
				})
				written[parts[0]] = struct{}{}
			}
			continue
		}

		// Check if embedded struct type.
		if s, ok := embeds[v.Name]; ok {
			if _, ok := written[v.Name]; !ok {
				var jt string
				if embeds[v.Name].Optional() {
					jt = v.Name + ",omitmepty"
				} else {
					jt = v.Name
				}
				out = append(out, Property{
					Name:    camelPascal(v.Name),
					JsonTag: jt,
					Docs:    v.Docs,
					Type:    s,
				})
				written[v.Name] = struct{}{}
			}
			continue
		}

		ct := convertType(v.Type)
		var jt string
		if ct.optional {
			jt = v.Name + ",omitempty"
		} else {
			jt = v.Name
		}
		out = append(out, Property{
			Name:    camelPascal(v.Name),
			JsonTag: jt,
			Docs:    v.Docs,
			Type:    convertType(v.Type),
		})
	}

	return out
}

func convertType(typ string) BasicType {
	t := strings.ToLower(typ)

	// Determine what kind of type was given.
	isOptional := strings.Contains(t, "(optional)")
	isArray := strings.ContainsRune(t, '<')

	var coreType string

	// If the type is not optional and not an array, we can check the
	// type mapping table directly.
	if !isOptional && !isArray {
		if val, ok := typeMapping[t]; ok {
			coreType = val
		} else {
			coreType = camelPascal(typ)
		}
	}

	if isArray {
		openBrace := strings.IndexRune(t, '<')
		closeBrace := strings.IndexRune(t, '>')
		coreType = camelPascal(typ[openBrace+1 : closeBrace])
	} else if isOptional {
		substr := t[:strings.IndexRune(t, ' ')]
		if val, ok := typeMapping[substr]; ok {
			coreType = val
		} else {
			coreType = camelPascal(typ)
		}
	}

	return BasicType{
		name:     coreType,
		optional: isOptional,
		array:    isArray,
	}
}
