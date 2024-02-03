package common_test

import (
	"os"
	"reflect"
	"testing"

	"github.com/google/uuid"
	"github.com/tesselslate/sandbox/bin/taskman/common"
)

var testData = common.Tasks{
	Boards: []common.Board{
		{
			Name:  "Test0",
			Items: make([]common.Item, 0),
			Id:    uuid.New(),
		},
		{
			Name: "Test1",
			Items: []common.Item{
				{
					Name:  "Item0",
					State: 0,
					Id:    uuid.New(),
				},
			},
			Id: uuid.New(),
		},
	},
}

func TestTasksJson(t *testing.T) {
	tmpdir, err := os.MkdirTemp("/tmp", "taskman-test")
	if err != nil {
		t.Error(err)
	}
	defer os.RemoveAll(tmpdir)
	err = common.WriteTasksJson(testData, tmpdir+"/.json")
	if err != nil {
		t.Error(err)
	}
	boards, err := common.ReadTasksJson(tmpdir + "/.json")
	if err != nil {
		t.Error(err)
	}
	if !reflect.DeepEqual(boards, testData) {
		t.Error("comparison failed")
	}
}

func TestTasks(t *testing.T) {
	tasks := testData
	orig := make([]common.Board, len(tasks.Boards))
	copy(orig, tasks.Boards)
	tasks.AddBoard("TestBoard0")
	index := -1
	for i, v := range tasks.Boards {
		if v.Name == "TestBoard0" {
			index = i
			break
		}
	}
	if index == -1 {
		t.Error("add failed")
	}
	tasks.DelBoard(index)
	for _, v := range tasks.Boards {
		if v.Name == "TestBoard0" {
			t.Error("delete failed")
		}
	}
	if !reflect.DeepEqual(orig, tasks.Boards) {
		t.Error("changed")
	}
	tasks.AddBoard("TestBoard1")
	var uuid uuid.UUID
	found := false
	for _, v := range tasks.Boards {
		if v.Name == "TestBoard1" {
			uuid = v.Id
			found = true
			break
		}
	}
	if !found {
		t.Error("add 2 failed")
	}
	tasks.DelBoardById(uuid)
	for _, v := range tasks.Boards {
		if v.Name == "TestBoard1" {
			t.Error("delete 2 failed")
		}
	}
	if !reflect.DeepEqual(orig, tasks.Boards) {
		t.Error("changed")
	}
}

func TestBoard(t *testing.T) {
	tasks := testData
	board := tasks.Boards[0]
	orig := make([]common.Item, len(board.Items))
	copy(orig, board.Items)
	board.AddItem("TestItem0")
	index := -1
	for i, v := range board.Items {
		if v.Name == "TestItem0" {
			index = i
			break
		}
	}
	if index == -1 {
		t.Error("add failed")
	}
	board.DelItem(index)
	for _, v := range board.Items {
		if v.Name == "TestItem0" {
			t.Error("delete failed")
		}
	}
	if !reflect.DeepEqual(orig, board.Items) {
		t.Error("changed")
	}
	board.AddItem("TestItem1")
	var uuid uuid.UUID
	found := false
	for _, v := range board.Items {
		if v.Name == "TestItem1" {
			uuid = v.Id
			found = true
			break
		}
	}
	if !found {
		t.Error("add 2 failed")
	}
	board.DelItemById(uuid)
	for _, v := range tasks.Boards {
		if v.Name == "TestItem1" {
			t.Error("delete 2 failed")
		}
	}
	if !reflect.DeepEqual(orig, board.Items) {
		t.Error("changed")
	}
}
