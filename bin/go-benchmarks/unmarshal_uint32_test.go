package main_test

import (
	"crypto/rand"
	"encoding/binary"
	"testing"
	"unsafe"
)

const N_unmarshalU32 = 8

// makeRandom creates a byte slice containing `n` random 32 bit integers.
func makeRandom(n int) []byte {
	b := make([]byte, n*4)
	_, err := rand.Read(b)
	if err != nil {
		panic(err)
	}
	return b
}

func BenchmarkBinaryUnmarshalUint32(b *testing.B) {
	data := makeRandom(N_unmarshalU32)
	_ = data[N_unmarshalU32*4-1]

	for i := 0; i < b.N; i += 1 {
		_ = binary.NativeEndian.Uint32(data[:])
		_ = binary.NativeEndian.Uint32(data[4:8])
		_ = binary.NativeEndian.Uint32(data[8:12])
		_ = binary.NativeEndian.Uint32(data[12:16])
		_ = binary.NativeEndian.Uint32(data[16:20])
		_ = binary.NativeEndian.Uint32(data[20:24])
		_ = binary.NativeEndian.Uint32(data[24:28])
		_ = binary.NativeEndian.Uint32(data[28:32])
	}
}

func BenchmarkUnsafeUnmarshalUint32(b *testing.B) {
	data := makeRandom(N_unmarshalU32)
	_ = data[N_unmarshalU32*4-1]
	for i := 0; i < b.N; i += 1 {
		_ = *(*uint32)(unsafe.Pointer(&data[0]))
		_ = *(*uint32)(unsafe.Pointer(&data[4]))
		_ = *(*uint32)(unsafe.Pointer(&data[8]))
		_ = *(*uint32)(unsafe.Pointer(&data[12]))
		_ = *(*uint32)(unsafe.Pointer(&data[16]))
		_ = *(*uint32)(unsafe.Pointer(&data[20]))
		_ = *(*uint32)(unsafe.Pointer(&data[24]))
		_ = *(*uint32)(unsafe.Pointer(&data[28]))
	}
}
