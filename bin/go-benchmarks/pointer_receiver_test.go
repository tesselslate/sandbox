package main_test

import "testing"

type (
	T struct{}
	F func() *T
)

//go:noinline
func makeF() F {
	x := T{}
	f := func() *T {
		return &x
	}
	return f
}

func BenchmarkRecvFunc(b *testing.B) {
	f := makeF()
	for i := 0; i < b.N; i += 1 {
		_ = f()
	}
}

func BenchmarkRecvPtr(b *testing.B) {
	x := &T{}
	for i := 0; i < b.N; i += 1 {
		_ = x
	}
}
