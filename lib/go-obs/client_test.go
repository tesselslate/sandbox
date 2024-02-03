package go_obs_test

import (
	"testing"

	obs "github.com/tesselslate/sandbox/lib/go-obs"
)

func connect(t *testing.T) *obs.Client {
	c := obs.Client{}
	needsAuth, _, err := c.Connect("localhost:4440")
	if err != nil {
		t.Error(err)
	}
	if !needsAuth {
		return &c
	}
	if needsAuth {
		err = c.Login("password")
		if err != nil {
			t.Error(err)
		}
	}
	return &c
}

func TestConnect(t *testing.T) {
	connect(t)
}

func TestStop(t *testing.T) {
	o := connect(t)
	o.Close()
}
