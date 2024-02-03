// Package tui implements the terminal client for taskman.
package tui

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/gdamore/tcell/v2"
	"github.com/google/uuid"
	"github.com/tesselslate/sandbox/bin/taskman/common"
)

// App contains all of the application state and code for managing the UI.
type App struct {
	path  string
	tasks common.Tasks

	currentBoard  *common.Board
	cursorIndex   int
	statusMessage string
	statusType    int
	width, height int

	past               []Action
	future             []Action
	mode               int
	currentInput       string
	currentInputPrompt string
	inputCallback      int
	searchQuery        string
	pleaseQuit         bool
	normalBuf          string
}

const (
	modeNormal int = iota
	modeInput

	inputCommand
	inputDeleteBoard
	inputDeleteItem
	inputNewBoard
	inputNewItem
	inputRenameBoard
	inputRenameItem
	inputSearch

	statusError
	statusInfo
)

// NewApp creates a new App.
func NewApp(path string) (App, error) {
	tasks, err := common.ReadTasksJson(path)
	if err != nil {
		return App{}, err
	}
	return App{
		path:   path,
		tasks:  tasks,
		past:   make([]Action, 0),
		future: make([]Action, 0),
		mode:   modeNormal,
	}, nil
}

// Run runs the app.
func (a *App) Run() error {
	screen, err := tcell.NewScreen()
	if err != nil {
		return err
	}
	if err := screen.Init(); err != nil {
		return err
	}
	defer screen.Fini()
	a.width, a.height = screen.Size()
	acceptForceQuit := false

	// Run the main loop.
	for {
		if a.pleaseQuit {
			err := common.WriteTasksJson(a.tasks, a.path)
			if !acceptForceQuit && err != nil {
				a.setStatus(statusError, "Failed to write tasks: %s", err)
				acceptForceQuit = true
			} else {
				return nil
			}
		}
		evt := screen.PollEvent()

		switch evt := evt.(type) {
		case *tcell.EventResize:
			a.width, a.height = screen.Size()
			screen.Sync()
		case *tcell.EventKey:
			// Process Ctrl+C events for quitting.
			if evt.Key() == tcell.KeyCtrlC {
				if a.mode == modeNormal {
					err := common.WriteTasksJson(a.tasks, a.path)
					if !acceptForceQuit && err != nil {
						a.setStatus(statusError, "Failed to write tasks: %s", err)
						acceptForceQuit = true
						break
					}
					return nil
				} else {
					a.mode = modeNormal
					break
				}
			}
			acceptForceQuit = false

			// Process any other key events.
			switch a.mode {
			case modeNormal:
				a.handleNormal(evt)
			case modeInput:
				a.handleInput(evt)
			}
		}

		// Redraw the UI.
		screen.Clear()
		boardsWidth := 0
		for _, v := range a.tasks.Boards {
			if len(v.Name) > boardsWidth {
				boardsWidth = len(v.Name)
			}
		}
		for i, v := range a.tasks.Boards {
			style := tcell.StyleDefault.Bold(true)
			if a.currentBoard == nil && i == a.cursorIndex {
				style = style.Background(tcell.ColorBlue).Foreground(tcell.ColorBlack)
			} else {
				style = style.Foreground(tcell.ColorBlue)
			}
			a.drawText(screen, 0, i, style, padRight(v.Name, boardsWidth))
		}
		if len(a.tasks.Boards) == 0 {
			a.drawText(
				screen,
				0,
				0,
				tcell.StyleDefault.Background(tcell.ColorWhite).Foreground(tcell.ColorBlack),
				"empty",
			)
		} else {
			board := a.currentBoard
			if board == nil {
				board = &a.tasks.Boards[a.cursorIndex]
			}
			if board != nil {
				if len(board.Items) == 0 {
					a.drawText(
						screen,
						boardsWidth+1,
						0,
						tcell.StyleDefault.Background(tcell.ColorWhite).Foreground(tcell.ColorBlack),
						"empty",
					)
				} else {
					for i, v := range board.Items {
						style := tcell.StyleDefault
						var fg tcell.Color
						switch v.State {
						case common.StateTodo:
							fg = tcell.ColorWhite
						case common.StateWip:
							fg = tcell.ColorOrange
						case common.StateDone:
							fg = tcell.ColorGreen
						}
						if a.currentBoard != nil && i == a.cursorIndex {
							style = style.Background(fg).Foreground(tcell.ColorBlack)
						} else {
							style = style.Foreground(fg)
						}
						a.drawText(screen, boardsWidth+1, i, style, padRight(v.Name, a.width-boardsWidth))
					}
				}
			}
		}
		if a.statusMessage != "" {
			style := tcell.StyleDefault
			if a.statusType == statusError {
				style = style.Foreground(tcell.ColorRed)
			}
			a.drawText(screen, 0, a.height-1, style, a.statusMessage)
		}
		if a.mode == modeInput {
			a.drawText(screen, 0, a.height-1, tcell.StyleDefault, a.currentInputPrompt)
			a.drawText(screen, len(a.currentInputPrompt), a.height-1, tcell.StyleDefault, a.currentInput)
			screen.ShowCursor(len(a.currentInputPrompt)+len(a.currentInput), a.height-1)
		} else {
			a.drawText(screen, a.width-10, a.height-1, tcell.StyleDefault, a.normalBuf)
			screen.HideCursor()
		}
		screen.Show()
	}
}

func (a *App) handleNormal(evt *tcell.EventKey) {
	switch evt.Key() {
	case tcell.KeyCtrlR:
		num := 1
		if len(a.normalBuf) > 0 {
			count, err := strconv.Atoi(a.normalBuf)
			if err != nil {
				num = count
			}
		}
		for i := 0; i < num; i++ {
			a.redoAction()
		}
		return
	case tcell.KeyBackspace, tcell.KeyBackspace2, tcell.KeyEscape:
		a.normalBuf = ""
		return
	}
	switch evt.Rune() {
	case 'a':
		if a.currentBoard != nil {
			a.startInput("Item name: ", "", inputNewItem)
		} else {
			a.startInput("Board name: ", "", inputNewBoard)
		}
	case 'c':
		if a.currentBoard != nil {
			if len(a.currentBoard.Items) != 0 {
				a.startInput("Item name: ", a.currentBoard.Items[a.cursorIndex].Name, inputRenameItem)
			} else {
				a.setStatus(statusError, "No item")
			}
		} else {
			if len(a.tasks.Boards) != 0 {
				a.startInput("Board name: ", a.tasks.Boards[a.cursorIndex].Name, inputRenameBoard)
			} else {
				a.setStatus(statusError, "No board")
			}
		}
	case 'd':
		if a.currentBoard != nil {
			if len(a.currentBoard.Items) != 0 {
				a.startInput("Delete? (Y/N) ", "", inputDeleteItem)
			} else {
				a.setStatus(statusError, "No item")
			}
		} else {
			if len(a.tasks.Boards) != 0 {
				a.startInput("Delete? (Y/N) ", "", inputDeleteBoard)
			} else {
				a.setStatus(statusError, "No board")
			}
		}
	case 'g':
		a.cursorIndex = 0
	case 'G':
		num := -1
		if len(a.normalBuf) > 0 {
			count, err := strconv.Atoi(a.normalBuf)
			if err == nil {
				num = count - 1
			}
		}
		max := 0
		if a.currentBoard != nil {
			max = len(a.currentBoard.Items) - 1
		} else {
			max = len(a.tasks.Boards) - 1
		}
		if num == -1 || num > max {
			num = max
		}
		a.cursorIndex = num
	case 'h':
		if a.currentBoard == nil {
			break
		}
		index := 0
		for i, v := range a.tasks.Boards {
			if v.Id == a.currentBoard.Id {
				index = i
				break
			}
		}
		a.currentBoard = nil
		a.cursorIndex = index
	case 'j':
		num := 1
		if len(a.normalBuf) > 0 {
			count, err := strconv.Atoi(a.normalBuf)
			if err == nil {
				num = count
			}
		}
		for i := 0; i < num; i += 1 {
			if a.currentBoard != nil {
				if a.cursorIndex < len(a.currentBoard.Items)-1 {
					a.cursorIndex += 1
				}
			} else {
				if a.cursorIndex < len(a.tasks.Boards)-1 {
					a.cursorIndex += 1
				}
			}
		}
	case 'k':
		num := 1
		if len(a.normalBuf) > 0 {
			count, err := strconv.Atoi(a.normalBuf)
			if err == nil {
				num = count
			}
		}
		for i := 0; i < num; i += 1 {
			if a.cursorIndex != 0 {
				a.cursorIndex -= 1
			}
		}
	case 'l':
		if a.currentBoard != nil {
			break
		}
		if len(a.tasks.Boards) != 0 {
			a.currentBoard = &a.tasks.Boards[a.cursorIndex]
			a.cursorIndex = 0
		}
	case 'J':
		if a.currentBoard != nil {
			if a.cursorIndex == len(a.currentBoard.Items)-1 {
				break
			}
			a.doAction(&MoveItemAction{
				Old:        a.cursorIndex,
				New:        a.cursorIndex + 1,
				BoardIndex: a.getBoardIndex(a.currentBoard.Id),
			})
		} else {
			if a.cursorIndex == len(a.tasks.Boards)-1 {
				break
			}
			a.doAction(&MoveBoardAction{
				Old: a.cursorIndex,
				New: a.cursorIndex + 1,
			})
		}
	case 'K':
		if a.currentBoard != nil {
			if a.cursorIndex == 0 {
				break
			}
			a.doAction(&MoveItemAction{
				Old:        a.cursorIndex,
				New:        a.cursorIndex - 1,
				BoardIndex: a.getBoardIndex(a.currentBoard.Id),
			})
		} else {
			if a.cursorIndex == 0 {
				break
			}
			a.doAction(&MoveBoardAction{
				Old: a.cursorIndex,
				New: a.cursorIndex - 1,
			})
		}
	case 'u':
		num := 1
		if len(a.normalBuf) > 0 {
			count, err := strconv.Atoi(a.normalBuf)
			if err != nil {
				num = count
			}
		}
		for i := 0; i < num; i += 1 {
			a.undoAction()
		}
	case ' ':
		if a.currentBoard == nil {
			break
		}
		state := a.currentBoard.Items[a.cursorIndex].State
		state = (state + 1) % (common.StateDone + 1)
		a.doAction(&StateAction{
			Uuid:       a.currentBoard.Items[a.cursorIndex].Id,
			BoardIndex: a.getBoardIndex(a.currentBoard.Id),
			State:      state,
			OldState:   a.currentBoard.Items[a.cursorIndex].State,
		})
	case ':':
		a.startInput(":", "", inputCommand)
	case '/':
		a.startInput("/", "", inputSearch)
	case 'n':
		a.nextSearchMatch()
	default:
		a.normalBuf += string(evt.Rune())
		return
	}
	a.normalBuf = ""
}

func (a *App) handleInput(evt *tcell.EventKey) {
	switch evt.Key() {
	case tcell.KeyBackspace, tcell.KeyBackspace2:
		if len(a.currentInput) != 0 {
			a.currentInput = a.currentInput[:len(a.currentInput)-1]
		}
	case tcell.KeyEnter:
		a.mode = modeNormal
		switch a.inputCallback {
		case inputCommand:
			switch a.currentInput {
			case "w", "write":
				err := common.WriteTasksJson(a.tasks, a.path)
				if err != nil {
					a.setStatus(statusError, "Failed to save: %s", err)
				} else {
					a.setStatus(statusInfo, "Saved")
				}
			case "wq", "q":
				a.pleaseQuit = true
			}
		case inputDeleteBoard:
			if a.currentInput == "y" || a.currentInput == "Y" {
				a.doAction(&DeleteBoardAction{
					Board: a.tasks.Boards[a.cursorIndex],
					Index: a.cursorIndex,
				})
			}
		case inputDeleteItem:
			if a.currentInput == "y" || a.currentInput == "Y" {
				a.doAction(&DeleteItemAction{
					Item:       a.currentBoard.Items[a.cursorIndex],
					Index:      a.cursorIndex,
					BoardIndex: a.getBoardIndex(a.currentBoard.Id),
				})
			}
		case inputNewBoard:
			a.doAction(&NewBoardAction{
				Name: a.currentInput,
			})
		case inputNewItem:
			a.doAction(&NewItemAction{
				Name:       a.currentInput,
				BoardIndex: a.getBoardIndex(a.currentBoard.Id),
			})
		case inputRenameBoard:
			a.doAction(&RenameAction{
				Uuid:    a.tasks.Boards[a.cursorIndex].Id,
				NewName: a.currentInput,
				OldName: a.tasks.Boards[a.cursorIndex].Name,
			})
		case inputRenameItem:
			a.doAction(&RenameAction{
				Uuid:    a.currentBoard.Items[a.cursorIndex].Id,
				NewName: a.currentInput,
				OldName: a.currentBoard.Items[a.cursorIndex].Name,
			})
		case inputSearch:
			a.searchQuery = a.currentInput
			a.nextSearchMatch()
		}
	case tcell.KeyEscape:
		a.mode = modeNormal
	default:
		a.currentInput += string(evt.Rune())
	}
}

func (a *App) getBoardIndex(id uuid.UUID) int {
	for i, v := range a.tasks.Boards {
		if v.Id == id {
			return i
		}
	}
	return -1
}

func (a *App) nextSearchMatch() {
	if a.searchQuery == "" {
		return
	}
	index := a.cursorIndex + 1
	if a.currentBoard != nil {
		if len(a.currentBoard.Items) != 0 {
			for index != a.cursorIndex {
				if index == len(a.currentBoard.Items) {
					index = 0
				}
				if strings.Contains(strings.ToLower(a.currentBoard.Items[index].Name), strings.ToLower(a.searchQuery)) {
					a.cursorIndex = index
					return
				}
				index += 1
			}
		}
		a.setStatus(statusError, "No match found")
	} else {
		if len(a.tasks.Boards) != 0 {
			for index != a.cursorIndex {
				if index == len(a.tasks.Boards) {
					index = 0
				}
				if strings.Contains(strings.ToLower(a.tasks.Boards[index].Name), strings.ToLower(a.searchQuery)) {
					a.cursorIndex = index
					return
				}
				index += 1
			}
		}
		a.setStatus(statusError, "No match found")
	}
}

func (a *App) doAction(action Action) {
	action.Do(a)
	a.past = append(a.past, action)
	a.future = make([]Action, 0)
}

func (a *App) undoAction() {
	if len(a.past) > 0 {
		action := a.past[len(a.past)-1]
		a.past = a.past[:len(a.past)-1]
		action.Undo(a)
		a.future = append(a.future, action)
	} else {
		a.setStatus(statusError, "Nothing to undo")
	}
}

func (a *App) redoAction() {
	if len(a.future) > 0 {
		action := a.future[len(a.future)-1]
		a.future = a.future[:len(a.future)-1]
		action.Do(a)
		a.past = append(a.past, action)
	} else {
		a.setStatus(statusError, "Nothing to redo")
	}
}

func (a *App) startInput(prompt string, input string, mode int) {
	a.statusMessage = ""
	a.currentInputPrompt = prompt
	a.currentInput = input
	a.mode = modeInput
	a.inputCallback = mode
}

func (a *App) drawText(s tcell.Screen, x, y int, style tcell.Style, text string) {
	for _, c := range text {
		s.SetContent(x, y, c, nil, style)
		x += 1
		if x >= a.width {
			return
		}
	}
}

func (a *App) setStatus(statusType int, message string, args ...any) {
	a.statusType = statusType
	a.statusMessage = fmt.Sprintf(message, args...)
}

func (a *App) moveCursorInbounds() {
	max := 0
	if a.currentBoard != nil {
		max = len(a.currentBoard.Items)
	} else {
		max = len(a.tasks.Boards)
	}
	if a.cursorIndex > max-1 {
		a.cursorIndex = max - 1
	}
	if a.cursorIndex == -1 {
		a.cursorIndex = 0
	}
}

func padRight(str string, strlen int) string {
	if len(str) >= strlen {
		return str
	}
	return str + strings.Repeat(" ", strlen-len(str))
}
