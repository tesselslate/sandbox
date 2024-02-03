package go_obs

type eventData struct {
	UpdateType     string `json:"update-type"`
	StreamTimecode string `json:"stream-timecode"`
	RecTimecode    string `json:"rec-timecode"`
}

type reqData struct {
	RequestType string `json:"request-type"`
	MessageId   string `json:"message-id"`
}

type resData struct {
	MessageId string `json:"message-id"`
	Status    string `json:"status"`
	Error     string `json:"error"`
}
