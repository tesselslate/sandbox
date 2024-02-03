package main

type JsonProtocol struct {
	Typedefs []JsonTypedef            `json:"typedefs"`
	Events   map[string][]JsonEvent   `json:"events"`
	Requests map[string][]JsonRequest `json:"requests"`
}

type JsonProperty struct {
	Type string `json:"type"`
	Name string `json:"name"`
	Docs string `json:"description"`
}

type JsonTypedef struct {
	Definition []JsonProperty `json:"typedefs"`
	Properties []JsonProperty `json:"properties"`
}

type JsonEvent struct {
	Name    string         `json:"name"`
	Docs    string         `json:"description"`
	Returns []JsonProperty `json:"returns"`
}

type JsonRequest struct {
	Name       string         `json:"name"`
	Docs       string         `json:"description"`
	Returns    []JsonProperty `json:"returns"`
	Parameters []JsonProperty `json:"params"`
	Deprecated string         `json:"deprecated"`
}
