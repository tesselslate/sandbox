package go_obs

import (
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"errors"
	"sync"

	"github.com/gorilla/websocket"
)

// Client maintains and manages a connection to OBS.
type Client struct {
	connected     bool
	auth          *GetAuthRequiredResponse
	conn          *websocket.Conn
	url           string
	errMap        map[string]chan error
	recvMap       map[string]chan []byte
	eventHandlers map[string]func(any)
	mx            sync.Mutex
	stop          chan struct{}
}

// Function Authenticate will authenticate with OBS using the provided password.
func (c *Client) Login(password string) error {
	if !c.connected {
		return errors.New("client not connected")
	}
	if c.auth == nil {
		return errors.New("no auth response")
	}
	saltpwd := password + c.auth.Salt
	salthash := sha256.Sum256([]byte(saltpwd))
	secret := base64.StdEncoding.EncodeToString(salthash[:])
	sec := secret + c.auth.Challenge
	sechash := sha256.Sum256([]byte(sec))
	secRes := base64.StdEncoding.EncodeToString(sechash[:])
	_, err := c.Authenticate(secRes)
	if err != nil {
		return err
	}
	return nil
}

// Function Connect attempts to connect to an OBS instance at the given
// address.
func (c *Client) Connect(address string) (bool, chan error, error) {
	c.url = address
	c.errMap = make(map[string]chan error)
	c.recvMap = make(map[string]chan []byte)
	c.stop = make(chan struct{})

	conn, _, err := websocket.DefaultDialer.Dial("ws://"+c.url, nil)
	if err != nil {
		return false, nil, err
	}
	errch := c.poll()
	c.conn = conn
	c.connected = true
	res, err := c.GetAuthRequired()
	if err != nil {
		conn.Close()
		return false, errch, err
	}
	if res.AuthRequired {
		c.auth = res
	}
	return res.AuthRequired, errch, nil
}

// Function Close closes the Client's connection.
func (c *Client) Close() error {
	if !c.connected {
		return errors.New("not connected")
	}
	c.stop <- struct{}{}
	return nil
}

// Function GetHandler returns the handler for the given event type, if
// it exists.
func (c *Client) GetHandler(eventType string) func(any) {
	return c.eventHandlers[eventType]
}

// Function SetHandler sets the handler for the given event type.
func (c *Client) SetHandler(eventType string, handler func(any)) {
	c.eventHandlers[eventType] = handler
}

func (c *Client) poll() chan error {
	errch := make(chan error)
	go func() {
		defer func() {
			c.mx.Lock()
			defer c.mx.Unlock()
			c.conn.Close()
			c.connected = false
		}()

		for {
			_, data, err := c.conn.ReadMessage()
			if err != nil {
				errch <- err
				return
			}
			m := make(map[string]interface{})
			err = json.Unmarshal(data, &m)
			if err != nil {
				errch <- err
				return
			}

			// - If the JSON message has the `message-id` property, then
			//   it is a request response.
			// -  If the JSON message has the `update-type` property, then
			//    it is an event.
			// -  If it has neither, it is an error occurring as a result of
			//    a previous request.
			if id, ok := m["message-id"]; ok {
				if status, ok := m["status"]; ok {
					if status == "error" {
						errMsg := m["error"]
						c.mx.Lock()
						c.errMap[id.(string)] <- errors.New(errMsg.(string))
						c.mx.Unlock()
					} else {
						c.mx.Lock()
						c.recvMap[id.(string)] <- data
						c.mx.Unlock()
					}
				} else {
					errch <- errors.New("no status")
					return
				}
				c.mx.Lock()
				delete(c.errMap, id.(string))
				delete(c.recvMap, id.(string))
				c.mx.Unlock()
			} else {
				if err, ok := m["error"]; ok {
					errch <- errors.New(err.(string))
				} else {
					eventType := m["update-type"].(string)
					if handler, ok := c.eventHandlers[eventType]; ok {
						event := eventConverters[eventType](data)
						if event != nil {
							handler(event)
						}
					}
				}
			}

			select {
			case <-c.stop:
				return
			default:
				continue
			}
		}
	}()
	return errch
}

func (c *Client) send(data []byte, id string, errch chan error) chan []byte {
	resch := make(chan []byte)
	if !c.connected {
		errch <- errors.New("client not connected")
		return resch
	}
	go func() {
		c.mx.Lock()
		defer c.mx.Unlock()
		c.errMap[id] = errch
		c.recvMap[id] = resch
		err := c.conn.WriteMessage(websocket.TextMessage, data)
		if err != nil {
			errch <- err
			delete(c.errMap, id)
			delete(c.recvMap, id)
		}
	}()
	return resch
}
