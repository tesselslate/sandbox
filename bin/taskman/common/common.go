// Package common implements common functionality used by other packages.
package common

// DeleteItem deletes the item at the given index of the slice.
func DeleteItem[T any](arr []T, idx int) []T {
	return append(arr[:idx], arr[idx+1:]...)
}

// InsertItem inserts the given item at the given index of the slice.
func InsertItem[T any](arr []T, item T, idx int) []T {
	arr = append(arr[:idx+1], arr[idx:]...)
	arr[idx] = item
	return arr
}
