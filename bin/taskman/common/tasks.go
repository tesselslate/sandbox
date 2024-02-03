package common

import (
	"encoding/json"
	"os"

	"github.com/google/uuid"
)

type Tasks struct {
	Boards []Board
}

type Board struct {
	Name  string
	Items []Item
	Id    uuid.UUID
}

type Item struct {
	Name  string
	State int
	Id    uuid.UUID
}

const (
	StateTodo int = iota
	StateWip
	StateDone
)

// ReadTasksJson reads a Tasks object from a JSON file on disk.
func ReadTasksJson(path string) (Tasks, error) {
	contents, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return Tasks{}, nil
		}
		return Tasks{}, err
	}
	tasks := Tasks{}
	err = json.Unmarshal(contents, &tasks)
	return tasks, err
}

// WriteTasksJson writes a Tasks object to a JSON file on disk.
func WriteTasksJson(tasks Tasks, path string) error {
	raw, err := json.Marshal(tasks)
	if err != nil {
		return err
	}
	return os.WriteFile(path, raw, 0644)
}

// AddBoard creates a new board with the given name.
func (t *Tasks) AddBoard(name string) {
	t.Boards = append(t.Boards, Board{
		Name:  name,
		Items: make([]Item, 0),
		Id:    uuid.New(),
	})
}

// DelBoard deletes the board at the given index.
func (t *Tasks) DelBoard(index int) {
	t.Boards = DeleteItem(t.Boards, index)
}

// DelBoardById deletes the board with the given ID.
func (t *Tasks) DelBoardById(uuid uuid.UUID) {
	idx := -1
	for i, v := range t.Boards {
		if v.Id == uuid {
			idx = i
			break
		}
	}
	t.Boards = DeleteItem(t.Boards, idx)
}

// AddItem creates a new item with the given name.
func (b *Board) AddItem(name string) {
	b.Items = append(b.Items, Item{
		Name:  name,
		State: StateTodo,
		Id:    uuid.New(),
	})
}

// DelItem deletes the item at the given index.
func (b *Board) DelItem(index int) {
	b.Items = DeleteItem(b.Items, index)
}

// DelItemById deletes the item with the given ID.
func (b *Board) DelItemById(uuid uuid.UUID) {
	idx := -1
	for i, v := range b.Items {
		if v.Id == uuid {
			idx = i
			break
		}
	}
	b.Items = DeleteItem(b.Items, idx)
}
