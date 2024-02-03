package common_test

import (
	"fmt"
	"testing"

	"github.com/tesselslate/sandbox/bin/taskman/common"
)

func TestDeleteItem(t *testing.T) {
	tests := []struct {
		count, del int
	}{
		{1, 0},
		{2, 0},
		{2, 1},
		{3, 1},
		{3, 2},
	}
	for _, test := range tests {
		name := fmt.Sprintf("%d-%d", test.count, test.del)
		t.Run(name, func(t *testing.T) {
			arr := make([]int, test.count)
			for i := range arr {
				arr[i] = i
			}
			arr = common.DeleteItem(arr, test.del)
			for i, v := range arr {
				expected := i
				if v >= test.del {
					expected += 1
				}
				if v != expected {
					t.Errorf("failed index %d (%d) %+v", i, expected, arr)
				}
			}
		})
	}
}

func TestInsertItem(t *testing.T) {
	tests := []struct {
		count, add int
	}{
		{1, 0},
		{2, 0},
		{2, 1},
		{3, 1},
		{3, 2},
	}
	for _, test := range tests {
		name := fmt.Sprintf("%d-%d", test.count, test.add)
		t.Run(name, func(t *testing.T) {
			arr := make([]int, test.count)
			for i := range arr {
				arr[i] = i
			}
			arr = common.InsertItem(arr, 10, test.add)
			for i, v := range arr {
				expected := i
				if i == test.add {
					expected = 10
				} else if i > test.add {
					expected -= 1
				}
				if v != expected {
					t.Errorf("failed index %d (%d) %+v", i, expected, arr)
				}
			}
		})
	}
}
