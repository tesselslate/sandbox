package main_test

import (
	"crypto/rand"
	"encoding/binary"
	"testing"
	"unsafe"
)

const N_marshalU32 = 8

// makeRandomU32 creates a uint32 slice containing `n` random 32 bit integers.
func makeRandomU32(n int) []uint32 {
	b := make([]uint32, n)
	bptr := unsafe.Slice((*byte)(unsafe.Pointer(&b[0])), n*4)
	if _, err := rand.Read(bptr); err != nil {
		panic(err)
	}
	return b
}

func BenchmarkBinaryMarshalUint32(b *testing.B) {
	data := makeRandomU32(N_marshalU32)
	buf := make([]byte, N_marshalU32*4)
	_ = data[7]
	_ = buf[N_marshalU32*4-1]

	for i := 0; i < b.N; i += 1 {
		binary.NativeEndian.PutUint32(buf[0:4], data[0])
		binary.NativeEndian.PutUint32(buf[4:8], data[1])
		binary.NativeEndian.PutUint32(buf[8:12], data[2])
		binary.NativeEndian.PutUint32(buf[12:16], data[3])
		binary.NativeEndian.PutUint32(buf[16:20], data[4])
		binary.NativeEndian.PutUint32(buf[20:24], data[5])
		binary.NativeEndian.PutUint32(buf[24:28], data[6])
		binary.NativeEndian.PutUint32(buf[28:32], data[7])
	}
}

func BenchmarkUnsafeMarshalUint32(b *testing.B) {
	data := makeRandomU32(N_marshalU32)
	buf := make([]byte, N_marshalU32*4)
    _ = data[7]

	for i := 0; i < b.N; i += 1 {
		*(*uint32)(unsafe.Pointer(&buf[0])) = data[0]
		*(*uint32)(unsafe.Pointer(&buf[4])) = data[1]
		*(*uint32)(unsafe.Pointer(&buf[8])) = data[2]
		*(*uint32)(unsafe.Pointer(&buf[12])) = data[3]
		*(*uint32)(unsafe.Pointer(&buf[16])) = data[4]
		*(*uint32)(unsafe.Pointer(&buf[20])) = data[5]
		*(*uint32)(unsafe.Pointer(&buf[24])) = data[6]
		*(*uint32)(unsafe.Pointer(&buf[28])) = data[7]
	}
}
