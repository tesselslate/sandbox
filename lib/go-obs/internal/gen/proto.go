package main

type Protocol struct {
	Typedefs []Typedef
	Events   []Event
	Requests []Request
}

type Typedef struct {
	Name       string
	Docs       string
	Properties []Property
}

type Event struct {
	Name    string
	Docs    string
	Returns []Property
}

type Request struct {
	Name       string
	Docs       string
	Deprecated string
	Parameters []Property
	Returns    []Property
}

type Property struct {
	Name    string
	Docs    string
	Type    Type
	JsonTag string
}
