package tui

import (
	"github.com/google/uuid"
	"github.com/tesselslate/sandbox/bin/taskman/common"
)

// Action represents a single user action which can take place
// or be undone.
type Action interface {
	Do(*App)
	Undo(*App)
}

type DeleteBoardAction struct {
	Board common.Board
	Index int
}

type DeleteItemAction struct {
	Item       common.Item
	BoardIndex int
	Index      int
}

type MoveBoardAction struct {
	Old int
	New int
}

type MoveItemAction struct {
	Old        int
	New        int
	BoardIndex int
}

type NewBoardAction struct {
	Uuid uuid.UUID
	Name string
}

type NewItemAction struct {
	Uuid       uuid.UUID
	Name       string
	BoardIndex int
}

type RenameAction struct {
	Uuid    uuid.UUID
	NewName string
	OldName string
}

type StateAction struct {
	Uuid       uuid.UUID
	BoardIndex int
	State      int
	OldState   int
}

func (action *DeleteBoardAction) Do(app *App) {
	app.tasks.Boards = common.DeleteItem(app.tasks.Boards, action.Index)
	app.setStatus(statusInfo, "Deleted board")
	app.currentBoard = nil
	app.cursorIndex = action.Index
	app.moveCursorInbounds()
}

func (action *DeleteBoardAction) Undo(app *App) {
	app.tasks.Boards = common.InsertItem(app.tasks.Boards, action.Board, action.Index)
	app.currentBoard = nil
	app.cursorIndex = action.Index
}

func (action *DeleteItemAction) Do(app *App) {
	app.tasks.Boards[action.BoardIndex].Items = common.DeleteItem(app.tasks.Boards[action.BoardIndex].Items, action.Index)
	app.setStatus(statusInfo, "Deleted item")
	app.currentBoard = &app.tasks.Boards[action.BoardIndex]
	app.cursorIndex = action.Index
	app.moveCursorInbounds()
}

func (action *DeleteItemAction) Undo(app *App) {
	app.tasks.Boards[action.BoardIndex].Items = common.InsertItem(app.tasks.Boards[action.BoardIndex].Items, action.Item, action.Index)
	app.currentBoard = &app.tasks.Boards[action.BoardIndex]
	app.cursorIndex = action.Index
}

func (action *MoveBoardAction) Do(app *App) {
	app.tasks.Boards[action.Old], app.tasks.Boards[action.New] = app.tasks.Boards[action.New], app.tasks.Boards[action.Old]
	app.currentBoard = nil
	app.cursorIndex = action.New
}

func (action *MoveBoardAction) Undo(app *App) {
	app.tasks.Boards[action.Old], app.tasks.Boards[action.New] = app.tasks.Boards[action.New], app.tasks.Boards[action.Old]
	app.currentBoard = nil
	app.cursorIndex = action.Old
}

func (action *MoveItemAction) Do(app *App) {
	board := &app.tasks.Boards[action.BoardIndex]
	board.Items[action.Old], board.Items[action.New] = board.Items[action.New], board.Items[action.Old]
	app.currentBoard = &app.tasks.Boards[action.BoardIndex]
	app.cursorIndex = action.New
}

func (action *MoveItemAction) Undo(app *App) {
	board := &app.tasks.Boards[action.BoardIndex]
	board.Items[action.Old], board.Items[action.New] = board.Items[action.New], board.Items[action.Old]
	app.currentBoard = &app.tasks.Boards[action.BoardIndex]
	app.cursorIndex = action.Old
}

func (action *NewBoardAction) Do(app *App) {
	app.tasks.AddBoard(action.Name)
	app.cursorIndex = len(app.tasks.Boards) - 1
	action.Uuid = app.tasks.Boards[len(app.tasks.Boards)-1].Id
}

func (action *NewBoardAction) Undo(app *App) {
	app.tasks.DelBoardById(action.Uuid)
	if app.currentBoard != nil && app.currentBoard.Id == action.Uuid {
		app.currentBoard = nil
	}
	app.moveCursorInbounds()
}

func (action *NewItemAction) Do(app *App) {
	app.tasks.Boards[action.BoardIndex].AddItem(action.Name)
	action.Uuid = app.tasks.Boards[action.BoardIndex].Items[len(app.tasks.Boards[action.BoardIndex].Items)-1].Id
	app.cursorIndex = len(app.tasks.Boards[action.BoardIndex].Items) - 1
	app.currentBoard = &app.tasks.Boards[action.BoardIndex]
}

func (action *NewItemAction) Undo(app *App) {
	app.tasks.Boards[action.BoardIndex].DelItemById(action.Uuid)
	app.moveCursorInbounds()
}

func (action *RenameAction) Do(app *App) {
	for i1, b := range app.tasks.Boards {
		if b.Id == action.Uuid {
			app.tasks.Boards[i1].Name = action.NewName
			return
		}
		for i2, i := range b.Items {
			if i.Id == action.Uuid {
				app.tasks.Boards[i1].Items[i2].Name = action.NewName
				return
			}
		}
	}
}

func (action *RenameAction) Undo(app *App) {
	for i1, b := range app.tasks.Boards {
		if b.Id == action.Uuid {
			app.tasks.Boards[i1].Name = action.OldName
			return
		}
		for i2, i := range b.Items {
			if i.Id == action.Uuid {
				app.tasks.Boards[i1].Items[i2].Name = action.OldName
				return
			}
		}
	}
}

func (action *StateAction) Do(app *App) {
	for i, v := range app.tasks.Boards[action.BoardIndex].Items {
		if v.Id == action.Uuid {
			app.tasks.Boards[action.BoardIndex].Items[i].State = action.State
			return
		}
	}
}

func (action *StateAction) Undo(app *App) {
	for i, v := range app.tasks.Boards[action.BoardIndex].Items {
		if v.Id == action.Uuid {
			app.tasks.Boards[action.BoardIndex].Items[i].State = action.OldState
			return
		}
	}
}
