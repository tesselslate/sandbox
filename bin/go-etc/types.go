//go:build ignore

package main

import "unsafe"

// Nil-able types
var (
	_ *int           = nil
	_ unsafe.Pointer = nil

	_ func() int  = nil
	_ chan int    = nil
	_ []int       = nil
	_ map[int]int = nil
	_ interface{} = nil
)

type (
	T struct{}

	Pointer *T
	Func    func() *T
	Chan    chan T
	Slice   []T
	Map     map[struct{}]T
)

// Invalid
// func (Pointer) F() {}

// Valid
func (Func) F()  {}
func (Chan) F()  {}
func (Slice) F() {}
func (Map) F()   {}
