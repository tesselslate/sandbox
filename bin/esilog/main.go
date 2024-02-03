package main

import (
	"bufio"
	"errors"
	"fmt"
	"io"
	"os"
	"os/signal"
	"regexp"
	"strconv"
	"syscall"
	"time"

	"github.com/fsnotify/fsnotify"
)

const LOG = "/mnt/ssd/mc/instances/ESI/.minecraft/logs/latest.log"

var tradeRegexp = regexp.MustCompile(`\[[0-9]{2}:[0-9]{2}:[0-9]{2}\] \[Render thread\/INFO\]: \[CHAT\] Trade (\d*) minecraft:(.*) (\d*)b`)
var noteRegexp = regexp.MustCompile(`\[[0-9]{2}:[0-9]{2}:[0-9]{2}\] \[Render thread\/INFO\]: \[CHAT\] \<woofdoggo_\> (.*)`)

var styleGreen = NewStyle().Foreground(BrightGreen)
var styleYellow = NewStyle().Foreground(BrightYellow)
var stylePurple = NewStyle().Foreground(BrightMagenta)
var styleOrange = NewStyle().Foreground(BrightRed)

func main() {
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		panic(err)
	}
	defer watcher.Close()
	watcher.Add(LOG)
	file, err := os.Open(LOG)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	reader := bufio.NewReader(file)

	fmt.Print("\x1b[?25l\x1b[?1049h")
	defer fmt.Print("\x1b[?25h\x1b[?1049l")
	lines := make(chan string, 16384)
	go process(lines)

	signals := make(chan os.Signal, 1)
	signal.Notify(signals, syscall.SIGINT)

	for {
		line, err := readLine(reader)
		if err != nil || line == "" {
			break
		}
		lines <- line
	}

	for {
		select {
		case event, ok := <-watcher.Events:
			if !ok {
				return
			}
			if event.Has(fsnotify.Write) {
				read(reader, lines)
			}
		case _, ok := <-watcher.Errors:
			if !ok {
				return
			}
		case <-signals:
			return
		}
	}
}

func read(reader *bufio.Reader, output chan<- string) {
	for {
		line, err := readLine(reader)
		if err != nil {
			return
		}
		if line == "" {
			return
		}
		output <- line
	}
}

func readLine(reader *bufio.Reader) (string, error) {
	buf, err := reader.ReadBytes('\n')
	switch err {
	case nil:
		return string(buf), nil
	case io.EOF:
		if len(buf) == 0 {
			return "", nil
		}

		timeout := time.Millisecond
		for tries := 0; tries < 5; tries += 1 {
			time.Sleep(timeout)
			timeout *= 2

			remainder, err := reader.ReadBytes('\n')
			buf = append(buf, remainder...)
			switch err {
			case io.EOF:
				continue
			case nil:
				return string(buf), nil
			default:
				return "", err
			}
		}
		return "", errors.New("read failed (5 tries)")
	default:
		return "", err
	}
}

type trade struct {
	item  string
	count int
}

func process(input <-chan string) {
	var trades []trade
	var notes []string
	for line := range input {
		matches := tradeRegexp.FindAllStringSubmatch(line, -1)
		if matches != nil {
			item := matches[0][2]
			count, err := strconv.Atoi(matches[0][3])
			if err != nil {
				panic(err)
			}

			trades = append(trades, trade{item, count})
			render(trades, notes)
			continue
		}
		matches = noteRegexp.FindAllStringSubmatch(line, -1)
		if matches != nil {
			note := matches[0][1]
			if note == "RESET" {
                trades = nil
                notes = nil
			} else {
				notes = append(notes, note)
			}
			render(trades, notes)
			continue
		}
	}
}

func render(trades []trade, notes []string) {
	fmt.Print("\x1b[2J")
	styleYellow.RenderAt("Ingots", 0, 0)
	styleGreen.RenderAt("Pearls", 8, 0)
	stylePurple.RenderAt("Explosives", 16, 0)
	styleOrange.RenderAt("Potions", 48, 0)
	for i := 1; i <= 18; i += 1 {
		if i > len(trades) {
			break
		}
		NewStyle().RenderAt(strconv.Itoa(i), 0, i)
		renderTrades(i, trades[0:i])
	}

	styleYellow.RenderAt("Blocks", 0, 20)
	styleGreen.RenderAt("Pearls", 8, 20)
	stylePurple.RenderAt("Explosives", 16, 20)
	styleOrange.RenderAt("Potions", 48, 20)
	for i := 9; i <= 144; i += 9 {
		if i > len(trades) {
			break
		}
		j := i / 9
		NewStyle().RenderAt(strconv.Itoa(j), 0, j+20)
		renderTrades(j+20, trades[0:i])
	}

	styleYellow.RenderAt("Notes", 0, 38)
	for i, note := range notes {
		NewStyle().RenderAt(note, 0, i+39)
	}
}

func renderTrades(y int, trades []trade) {
	var pearls, strings, glowstone, crying, potions int
	for _, trade := range trades {
		switch trade.item {
		case "ender_pearl":
			pearls += trade.count
		case "string":
			strings += trade.count
		case "glowstone_dust":
			glowstone += trade.count
		case "crying_obsidian":
			crying += trade.count
		case "potion", "splash_potion":
			potions += trade.count
		}
	}

	beds := strings / 12
	anchors := min(crying/6, glowstone/16)
	styleGreen.RenderAt(strconv.Itoa(pearls), 8, y)

	x := 16
	renderPart := func(str string, style Style) {
		style.RenderAt(str, x, y)
		x += len(str)
	}
	renderPart(strconv.Itoa(beds), NewStyle())
	renderPart("+", NewStyle().Foreground(Gray))
	renderPart(strconv.Itoa(anchors), styleYellow)
	renderPart(" = ", NewStyle())
	renderPart(strconv.Itoa(beds+anchors), stylePurple.Bold())
	renderPart(", (", NewStyle())
	renderPart(strconv.Itoa(strings), NewStyle())
	renderPart("/", NewStyle().Foreground(Gray))
	renderPart(strconv.Itoa(glowstone), styleYellow)
	renderPart("/", NewStyle().Foreground(Gray))
	renderPart(strconv.Itoa(crying), stylePurple)
	renderPart(")", NewStyle())

	styleOrange.RenderAt(strconv.Itoa(potions), 48, y)
}
