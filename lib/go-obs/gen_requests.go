package go_obs

import (
	"encoding/json"

	"github.com/google/uuid"
)

// Add a new filter to a source. Available source types along with their
// settings properties are available from `GetSourceTypesList`.
type AddFilterToSourceRequest struct {
	reqData
	// Name of the source on which the filter is added
	SourceName string `json:"sourceName"`
	// Name of the new filter
	FilterName string `json:"filterName"`
	// Filter type
	FilterType string `json:"filterType"`
	// Filter settings
	FilterSettings interface{} `json:"filterSettings"`
}

func (c *Client) AddFilterToSource(SourceName string, FilterName string, FilterType string, FilterSettings interface{}) (*AddFilterToSourceResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := AddFilterToSourceRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "AddFilterToSource",
		},
		SourceName:     SourceName,
		FilterName:     FilterName,
		FilterType:     FilterType,
		FilterSettings: FilterSettings,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &AddFilterToSourceResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type AddFilterToSourceResponse struct {
	resData
}

// Creates a scene item in a scene. In other words, this is how you add a source
// into a scene.
type AddSceneItemRequest struct {
	reqData
	// Name of the scene to create the scene item in
	SceneName string `json:"sceneName"`
	// Name of the source to be added
	SourceName string `json:"sourceName"`
	// Whether to make the sceneitem visible on creation or not. Default `true`
	SetVisible *bool `json:"setVisible,omitempty"`
}

func (c *Client) AddSceneItem(SceneName string, SourceName string, SetVisible *bool) (*AddSceneItemResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := AddSceneItemRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "AddSceneItem",
		},
		SceneName:  SceneName,
		SourceName: SourceName,
		SetVisible: SetVisible,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &AddSceneItemResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type AddSceneItemResponse struct {
	resData
	// Numerical ID of the created scene item
	ItemId int `json:"itemId"`
}

// Attempt to authenticate the client to the server.
type AuthenticateRequest struct {
	reqData
	// Response to the auth challenge (see "Authentication" for more information).
	Auth string `json:"auth"`
}

func (c *Client) Authenticate(Auth string) (*AuthenticateResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := AuthenticateRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "Authenticate",
		},
		Auth: Auth,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &AuthenticateResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type AuthenticateResponse struct {
	resData
}

// Broadcast custom message to all connected WebSocket clients
type BroadcastCustomMessageRequest struct {
	reqData
	// Identifier to be choosen by the client
	Realm string `json:"realm"`
	// User-defined data
	Data interface{} `json:"data"`
}

func (c *Client) BroadcastCustomMessage(Realm string, Data interface{}) (*BroadcastCustomMessageResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := BroadcastCustomMessageRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "BroadcastCustomMessage",
		},
		Realm: Realm,
		Data:  Data,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &BroadcastCustomMessageResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type BroadcastCustomMessageResponse struct {
	resData
}

// Create a new scene scene.
type CreateSceneRequest struct {
	reqData
	// Name of the scene to create.
	SceneName string `json:"sceneName"`
}

func (c *Client) CreateScene(SceneName string) (*CreateSceneResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := CreateSceneRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "CreateScene",
		},
		SceneName: SceneName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &CreateSceneResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type CreateSceneResponse struct {
	resData
}

// Create a source and add it as a sceneitem to a scene.
type CreateSourceRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
	// Source kind, Eg. `vlc_source`.
	SourceKind string `json:"sourceKind"`
	// Scene to add the new source to.
	SceneName string `json:"sceneName"`
	// Source settings data.
	SourceSettings interface{} `json:"sourceSettings,omitempty"`
	// Set the created SceneItem as visible or not. Defaults to true
	SetVisible *bool `json:"setVisible,omitempty"`
}

func (c *Client) CreateSource(SourceName string, SourceKind string, SceneName string, SourceSettings interface{}, SetVisible *bool) (*CreateSourceResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := CreateSourceRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "CreateSource",
		},
		SourceName:     SourceName,
		SourceKind:     SourceKind,
		SceneName:      SceneName,
		SourceSettings: SourceSettings,
		SetVisible:     SetVisible,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &CreateSourceResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type CreateSourceResponse struct {
	resData
	// ID of the SceneItem in the scene.
	ItemId int `json:"itemId"`
}

// Deletes a scene item.
type DeleteSceneItemRequest struct {
	reqData
	// Name of the scene the scene item belongs to. Defaults to the current scene.
	Scene string `json:"scene,omitempty"`
	// Scene item to delete (required)
	Item DeleteSceneItemItem `json:"item"`
}

func (c *Client) DeleteSceneItem(Scene string, Item DeleteSceneItemItem) (*DeleteSceneItemResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := DeleteSceneItemRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "DeleteSceneItem",
		},
		Scene: Scene,
		Item:  Item,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &DeleteSceneItemResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type DeleteSceneItemResponse struct {
	resData
}

// Disables Studio Mode.
type DisableStudioModeRequest struct {
	reqData
}

func (c *Client) DisableStudioMode() (*DisableStudioModeResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := DisableStudioModeRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "DisableStudioMode",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &DisableStudioModeResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type DisableStudioModeResponse struct {
	resData
}

// Duplicates a scene item.
type DuplicateSceneItemRequest struct {
	reqData
	// Name of the scene to copy the item from. Defaults to the current scene.
	FromScene string `json:"fromScene,omitempty"`
	// Name of the scene to create the item in. Defaults to the current scene.
	ToScene string `json:"toScene,omitempty"`
	// Scene Item to duplicate from the source scene (required)
	Item DuplicateSceneItemItem `json:"item"`
}

func (c *Client) DuplicateSceneItem(FromScene string, ToScene string, Item DuplicateSceneItemItem) (*DuplicateSceneItemResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := DuplicateSceneItemRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "DuplicateSceneItem",
		},
		FromScene: FromScene,
		ToScene:   ToScene,
		Item:      Item,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &DuplicateSceneItemResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type DuplicateSceneItemResponse struct {
	resData
	// Name of the scene where the new item was created
	Scene string `json:"scene"`
	// New item info
	Item struct {
		// New item ID
		Id int `json:"id"`
		// New item name
		Name string `json:"name"`
	} `json:"item"`
}

// Enables Studio Mode.
type EnableStudioModeRequest struct {
	reqData
}

func (c *Client) EnableStudioMode() (*EnableStudioModeResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := EnableStudioModeRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "EnableStudioMode",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &EnableStudioModeResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type EnableStudioModeResponse struct {
	resData
}

// Executes a list of requests sequentially (one-by-one on the same thread).
type ExecuteBatchRequest struct {
	reqData
	// Array of requests to perform. Executed in order.
	Requests []ExecuteBatchRequests `json:"requests"`
	// Stop processing batch requests if one returns a failure.
	AbortOnFail *bool `json:"abortOnFail,omitempty"`
}

func (c *Client) ExecuteBatch(Requests []ExecuteBatchRequests, AbortOnFail *bool) (*ExecuteBatchResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := ExecuteBatchRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "ExecuteBatch",
		},
		Requests:    Requests,
		AbortOnFail: AbortOnFail,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &ExecuteBatchResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type ExecuteBatchResponse struct {
	resData
	// Batch requests results, ordered sequentially.
	Results []struct {
		// ID of the individual request which was originally provided by the client.
		MessageId string `json:"message-id"`
		// Status response as string. Either `ok` or `error`.
		Status string `json:"status"`
		// Error message accompanying an `error` status.
		Error string `json:"error,omitempty"`
	} `json:"results"`
}

// Get the audio's active status of a specified source.
type GetAudioActiveRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
}

func (c *Client) GetAudioActive(SourceName string) (*GetAudioActiveResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetAudioActiveRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetAudioActive",
		},
		SourceName: SourceName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetAudioActiveResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetAudioActiveResponse struct {
	resData
	// Audio active status of the source.
	AudioActive bool `json:"audioActive"`
}

// Get the audio monitoring type of the specified source.
type GetAudioMonitorTypeRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
}

func (c *Client) GetAudioMonitorType(SourceName string) (*GetAudioMonitorTypeResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetAudioMonitorTypeRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetAudioMonitorType",
		},
		SourceName: SourceName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetAudioMonitorTypeResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetAudioMonitorTypeResponse struct {
	resData
	// The monitor type in use. Options: `none`, `monitorOnly`, `monitorAndOutput`.
	MonitorType string `json:"monitorType"`
}

// Gets whether an audio track is active for a source.
type GetAudioTracksRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
}

func (c *Client) GetAudioTracks(SourceName string) (*GetAudioTracksResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetAudioTracksRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetAudioTracks",
		},
		SourceName: SourceName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetAudioTracksResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetAudioTracksResponse struct {
	resData
	Track1 bool `json:"track1"`
	Track2 bool `json:"track2"`
	Track3 bool `json:"track3"`
	Track4 bool `json:"track4"`
	Track5 bool `json:"track5"`
	Track6 bool `json:"track6"`
}

// Tells the client if authentication is required. If so, returns authentication
// parameters `challenge` and `salt` (see "Authentication" for more
// information).
type GetAuthRequiredRequest struct {
	reqData
}

func (c *Client) GetAuthRequired() (*GetAuthRequiredResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetAuthRequiredRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetAuthRequired",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetAuthRequiredResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetAuthRequiredResponse struct {
	resData
	// Indicates whether authentication is required.
	AuthRequired bool   `json:"authRequired"`
	Challenge    string `json:"challenge,omitempty"`
	Salt         string `json:"salt,omitempty"`
}

// Get current properties for a Browser Source.
//
// Deprecated:
// Since 4.8.0. Prefer the use of GetSourceSettings. Will be removed in v5.0.0
type GetBrowserSourcePropertiesRequest struct {
	reqData
	// Source name.
	Source string `json:"source"`
}

func (c *Client) GetBrowserSourceProperties(Source string) (*GetBrowserSourcePropertiesResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetBrowserSourcePropertiesRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetBrowserSourceProperties",
		},
		Source: Source,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetBrowserSourcePropertiesResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetBrowserSourcePropertiesResponse struct {
	resData
	// Source name.
	Source string `json:"source"`
	// Indicates that a local file is in use.
	IsLocalFile bool `json:"is_local_file"`
	// file path.
	LocalFile string `json:"local_file"`
	// Url.
	Url string `json:"url"`
	// CSS to inject.
	Css string `json:"css"`
	// Width.
	Width int `json:"width"`
	// Height.
	Height int `json:"height"`
	// Framerate.
	Fps int `json:"fps"`
	// Indicates whether the source should be shutdown when not visible.
	Shutdown bool `json:"shutdown"`
}

// Get the name of the current profile.
type GetCurrentProfileRequest struct {
	reqData
}

func (c *Client) GetCurrentProfile() (*GetCurrentProfileResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetCurrentProfileRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetCurrentProfile",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetCurrentProfileResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetCurrentProfileResponse struct {
	resData
	// Name of the currently active profile.
	ProfileName string `json:"profile-name"`
}

// Get the current scene's name and source items.
type GetCurrentSceneRequest struct {
	reqData
}

func (c *Client) GetCurrentScene() (*GetCurrentSceneResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetCurrentSceneRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetCurrentScene",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetCurrentSceneResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetCurrentSceneResponse struct {
	resData
	// Name of the currently active scene.
	Name string `json:"name"`
	// Ordered list of the current scene's source items.
	Sources []SceneItem `json:"sources"`
}

// Get the name of the current scene collection.
type GetCurrentSceneCollectionRequest struct {
	reqData
}

func (c *Client) GetCurrentSceneCollection() (*GetCurrentSceneCollectionResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetCurrentSceneCollectionRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetCurrentSceneCollection",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetCurrentSceneCollectionResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetCurrentSceneCollectionResponse struct {
	resData
	// Name of the currently active scene collection.
	ScName string `json:"sc-name"`
}

// Get the name of the currently selected transition in the frontend's dropdown
// menu.
type GetCurrentTransitionRequest struct {
	reqData
}

func (c *Client) GetCurrentTransition() (*GetCurrentTransitionResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetCurrentTransitionRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetCurrentTransition",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetCurrentTransitionResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetCurrentTransitionResponse struct {
	resData
	// Name of the selected transition.
	Name string `json:"name"`
	// Transition duration (in milliseconds) if supported by the transition.
	Duration *int `json:"duration,omitempty"`
}

// Get the filename formatting string
type GetFilenameFormattingRequest struct {
	reqData
}

func (c *Client) GetFilenameFormatting() (*GetFilenameFormattingResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetFilenameFormattingRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetFilenameFormatting",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetFilenameFormattingResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetFilenameFormattingResponse struct {
	resData
	// Current filename formatting string.
	FilenameFormatting string `json:"filename-formatting"`
}

// Get the length of media in milliseconds. Supports ffmpeg and vlc media
// sources (as of OBS v25.0.8) Note: For some reason, for the first 5 or so
// seconds that the media is playing, the total duration can be off by upwards
// of 50ms.
type GetMediaDurationRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
}

func (c *Client) GetMediaDuration(SourceName string) (*GetMediaDurationResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetMediaDurationRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetMediaDuration",
		},
		SourceName: SourceName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetMediaDurationResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetMediaDurationResponse struct {
	resData
	// The total length of media in milliseconds..
	MediaDuration int `json:"mediaDuration"`
}

// List the media state of all media sources (vlc and media source)
type GetMediaSourcesListRequest struct {
	reqData
}

func (c *Client) GetMediaSourcesList() (*GetMediaSourcesListResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetMediaSourcesListRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetMediaSourcesList",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetMediaSourcesListResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetMediaSourcesListResponse struct {
	resData
	// Array of sources
	MediaSources []struct {
		// Unique source name
		SourceName string `json:"sourceName"`
		// Unique source internal type (a.k.a `ffmpeg_source` or `vlc_source`)
		SourceKind string `json:"sourceKind"`
		// The current state of media for that source. States: `none`, `playing`,
		// `opening`, `buffering`, `paused`, `stopped`, `ended`, `error`, `unknown`
		MediaState string `json:"mediaState"`
	} `json:"mediaSources"`
}

// Get the current playing state of a media source. Supports ffmpeg and vlc
// media sources (as of OBS v25.0.8)
type GetMediaStateRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
}

func (c *Client) GetMediaState(SourceName string) (*GetMediaStateResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetMediaStateRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetMediaState",
		},
		SourceName: SourceName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetMediaStateResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetMediaStateResponse struct {
	resData
	// The media state of the provided source. States: `none`, `playing`, `opening`,
	// `buffering`, `paused`, `stopped`, `ended`, `error`, `unknown`
	MediaState string `json:"mediaState"`
}

// Get the current timestamp of media in milliseconds. Supports ffmpeg and vlc
// media sources (as of OBS v25.0.8)
type GetMediaTimeRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
}

func (c *Client) GetMediaTime(SourceName string) (*GetMediaTimeResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetMediaTimeRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetMediaTime",
		},
		SourceName: SourceName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetMediaTimeResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetMediaTimeResponse struct {
	resData
	// The time in milliseconds since the start of the media.
	Timestamp int `json:"timestamp"`
}

// Get the mute status of a specified source.
type GetMuteRequest struct {
	reqData
	// Source name.
	Source string `json:"source"`
}

func (c *Client) GetMute(Source string) (*GetMuteResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetMuteRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetMute",
		},
		Source: Source,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetMuteResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetMuteResponse struct {
	resData
	// Source name.
	Name string `json:"name"`
	// Mute status of the source.
	Muted bool `json:"muted"`
}

// Get information about a single output
type GetOutputInfoRequest struct {
	reqData
	// Output name
	OutputName string `json:"outputName"`
}

func (c *Client) GetOutputInfo(OutputName string) (*GetOutputInfoResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetOutputInfoRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetOutputInfo",
		},
		OutputName: OutputName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetOutputInfoResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetOutputInfoResponse struct {
	resData
	// Output info
	OutputInfo Output `json:"outputInfo"`
}

// Get the name of the currently previewed scene and its list of sources. Will
// return an `error` if Studio Mode is not enabled.
type GetPreviewSceneRequest struct {
	reqData
}

func (c *Client) GetPreviewScene() (*GetPreviewSceneResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetPreviewSceneRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetPreviewScene",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetPreviewSceneResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetPreviewSceneResponse struct {
	resData
	// The name of the active preview scene.
	Name    string      `json:"name"`
	Sources []SceneItem `json:"sources"`
}

// Get the path of  the current recording folder.
type GetRecordingFolderRequest struct {
	reqData
}

func (c *Client) GetRecordingFolder() (*GetRecordingFolderResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetRecordingFolderRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetRecordingFolder",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetRecordingFolderResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetRecordingFolderResponse struct {
	resData
	// Path of the recording folder.
	RecFolder string `json:"rec-folder"`
}

// Get current recording status.
type GetRecordingStatusRequest struct {
	reqData
}

func (c *Client) GetRecordingStatus() (*GetRecordingStatusResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetRecordingStatusRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetRecordingStatus",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetRecordingStatusResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetRecordingStatusResponse struct {
	resData
	// Current recording status.
	IsRecording bool `json:"isRecording"`
	// Whether the recording is paused or not.
	IsRecordingPaused bool `json:"isRecordingPaused"`
	// Time elapsed since recording started (only present if currently recording).
	RecordTimecode string `json:"recordTimecode,omitempty"`
	// Absolute path to the recording file (only present if currently recording).
	RecordingFilename string `json:"recordingFilename,omitempty"`
}

// Get the status of the OBS replay buffer.
type GetReplayBufferStatusRequest struct {
	reqData
}

func (c *Client) GetReplayBufferStatus() (*GetReplayBufferStatusResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetReplayBufferStatusRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetReplayBufferStatus",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetReplayBufferStatusResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetReplayBufferStatusResponse struct {
	resData
	// Current recording status.
	IsReplayBufferActive bool `json:"isReplayBufferActive"`
}

// Get a list of all scene items in a scene.
type GetSceneItemListRequest struct {
	reqData
	// Name of the scene to get the list of scene items from. Defaults to the
	// current scene if not specified.
	SceneName string `json:"sceneName,omitempty"`
}

func (c *Client) GetSceneItemList(SceneName string) (*GetSceneItemListResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetSceneItemListRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetSceneItemList",
		},
		SceneName: SceneName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetSceneItemListResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetSceneItemListResponse struct {
	resData
	// Name of the requested (or current) scene
	SceneName string `json:"sceneName"`
	// Array of scene items
	SceneItems []struct {
		// Unique item id of the source item
		ItemId int `json:"itemId"`
		// ID if the scene item's source. For example `vlc_source` or `image_source`
		SourceKind string `json:"sourceKind"`
		// Name of the scene item's source
		SourceName string `json:"sourceName"`
		// Type of the scene item's source. Either `input`, `group`, or `scene`
		SourceType string `json:"sourceType"`
	} `json:"sceneItems"`
}

// Gets the scene specific properties of the specified source item. Coordinates
// are relative to the item's parent (the scene or group it belongs to).
type GetSceneItemPropertiesRequest struct {
	reqData
	// Name of the scene the scene item belongs to. Defaults to the current scene.
	SceneName string `json:"scene-name,omitempty"`
	// Scene Item name (if this field is a string) or specification (if it is an
	// object).
	Item GetSceneItemPropertiesItem `json:"item"`
}

func (c *Client) GetSceneItemProperties(SceneName string, Item GetSceneItemPropertiesItem) (*GetSceneItemPropertiesResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetSceneItemPropertiesRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetSceneItemProperties",
		},
		SceneName: SceneName,
		Item:      Item,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetSceneItemPropertiesResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetSceneItemPropertiesResponse struct {
	resData
	// Scene Item name.
	Name string `json:"name"`
	// Scene Item ID.
	ItemId int `json:"itemId"`
	// The x position of the source from the left.
	Position struct {
		// The x position of the source from the left.
		X float64 `json:"x"`
		// The y position of the source from the top.
		Y float64 `json:"y"`
		// The point on the source that the item is manipulated from. The sum of 1=Left
		// or 2=Right, and 4=Top or 8=Bottom, or omit to center on that axis.
		Alignment int `json:"alignment"`
	} `json:"position"`
	// The clockwise rotation of the item in degrees around the point of alignment.
	Rotation float64 `json:"rotation"`
	// The x-scale factor of the source.
	Scale struct {
		// The x-scale factor of the source.
		X float64 `json:"x"`
		// The y-scale factor of the source.
		Y float64 `json:"y"`
		// The scale filter of the source. Can be "OBS_SCALE_DISABLE",
		// "OBS_SCALE_POINT", "OBS_SCALE_BICUBIC", "OBS_SCALE_BILINEAR",
		// "OBS_SCALE_LANCZOS" or "OBS_SCALE_AREA".
		Filter string `json:"filter"`
	} `json:"scale"`
	// The number of pixels cropped off the top of the source before scaling.
	Crop struct {
		// The number of pixels cropped off the top of the source before scaling.
		Top int `json:"top"`
		// The number of pixels cropped off the right of the source before scaling.
		Right int `json:"right"`
		// The number of pixels cropped off the bottom of the source before scaling.
		Bottom int `json:"bottom"`
		// The number of pixels cropped off the left of the source before scaling.
		Left int `json:"left"`
	} `json:"crop"`
	// If the source is visible.
	Visible bool `json:"visible"`
	// If the source is muted.
	Muted bool `json:"muted"`
	// If the source's transform is locked.
	Locked bool `json:"locked"`
	// Type of bounding box. Can be "OBS_BOUNDS_STRETCH", "OBS_BOUNDS_SCALE_INNER",
	// "OBS_BOUNDS_SCALE_OUTER", "OBS_BOUNDS_SCALE_TO_WIDTH",
	// "OBS_BOUNDS_SCALE_TO_HEIGHT", "OBS_BOUNDS_MAX_ONLY" or "OBS_BOUNDS_NONE".
	Bounds struct {
		// Type of bounding box. Can be "OBS_BOUNDS_STRETCH", "OBS_BOUNDS_SCALE_INNER",
		// "OBS_BOUNDS_SCALE_OUTER", "OBS_BOUNDS_SCALE_TO_WIDTH",
		// "OBS_BOUNDS_SCALE_TO_HEIGHT", "OBS_BOUNDS_MAX_ONLY" or "OBS_BOUNDS_NONE".
		Type string `json:"type"`
		// Alignment of the bounding box.
		Alignment int `json:"alignment"`
		// Width of the bounding box.
		X float64 `json:"x"`
		// Height of the bounding box.
		Y float64 `json:"y"`
	} `json:"bounds"`
	// Base width (without scaling) of the source
	SourceWidth int `json:"sourceWidth"`
	// Base source (without scaling) of the source
	SourceHeight int `json:"sourceHeight"`
	// Scene item width (base source width multiplied by the horizontal scaling
	// factor)
	Width float64 `json:"width"`
	// Scene item height (base source height multiplied by the vertical scaling
	// factor)
	Height float64 `json:"height"`
	// Name of the item's parent (if this item belongs to a group)
	ParentGroupName string `json:"parentGroupName,omitempty"`
	// List of children (if this item is a group)
	GroupChildren []SceneItemTransform `json:"groupChildren,omitempty"`
}

// Get a list of scenes in the currently active profile.
type GetSceneListRequest struct {
	reqData
}

func (c *Client) GetSceneList() (*GetSceneListResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetSceneListRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetSceneList",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetSceneListResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetSceneListResponse struct {
	resData
	// Name of the currently active scene.
	CurrentScene string `json:"current-scene"`
	// Ordered list of the current profile's scenes (See
	// [GetCurrentScene](#getcurrentscene) for more information).
	Scenes []Scene `json:"scenes"`
}

// Get the current scene transition override.
type GetSceneTransitionOverrideRequest struct {
	reqData
	// Name of the scene to switch to.
	SceneName string `json:"sceneName"`
}

func (c *Client) GetSceneTransitionOverride(SceneName string) (*GetSceneTransitionOverrideResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetSceneTransitionOverrideRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetSceneTransitionOverride",
		},
		SceneName: SceneName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetSceneTransitionOverrideResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetSceneTransitionOverrideResponse struct {
	resData
	// Name of the current overriding transition. Empty string if no override is
	// set.
	TransitionName string `json:"transitionName"`
	// Transition duration. `-1` if no override is set.
	TransitionDuration int `json:"transitionDuration"`
}

// Get the source's active status of a specified source (if it is showing in the
// final mix).
type GetSourceActiveRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
}

func (c *Client) GetSourceActive(SourceName string) (*GetSourceActiveResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetSourceActiveRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetSourceActive",
		},
		SourceName: SourceName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetSourceActiveResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetSourceActiveResponse struct {
	resData
	// Source active status of the source.
	SourceActive bool `json:"sourceActive"`
}

// Get the default settings for a given source type.
type GetSourceDefaultSettingsRequest struct {
	reqData
	// Source kind. Also called "source id" in libobs terminology.
	SourceKind string `json:"sourceKind"`
}

func (c *Client) GetSourceDefaultSettings(SourceKind string) (*GetSourceDefaultSettingsResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetSourceDefaultSettingsRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetSourceDefaultSettings",
		},
		SourceKind: SourceKind,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetSourceDefaultSettingsResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetSourceDefaultSettingsResponse struct {
	resData
	// Source kind. Same value as the `sourceKind` parameter.
	SourceKind string `json:"sourceKind"`
	// Settings object for source.
	DefaultSettings interface{} `json:"defaultSettings"`
}

// List filters applied to a source
type GetSourceFilterInfoRequest struct {
	reqData
	// Source name
	SourceName string `json:"sourceName"`
	// Source filter name
	FilterName string `json:"filterName"`
}

func (c *Client) GetSourceFilterInfo(SourceName string, FilterName string) (*GetSourceFilterInfoResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetSourceFilterInfoRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetSourceFilterInfo",
		},
		SourceName: SourceName,
		FilterName: FilterName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetSourceFilterInfoResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetSourceFilterInfoResponse struct {
	resData
	// Filter status (enabled or not)
	Enabled bool `json:"enabled"`
	// Filter type
	Type string `json:"type"`
	// Filter name
	Name string `json:"name"`
	// Filter settings
	Settings interface{} `json:"settings"`
}

// List filters applied to a source
type GetSourceFiltersRequest struct {
	reqData
	// Source name
	SourceName string `json:"sourceName"`
}

func (c *Client) GetSourceFilters(SourceName string) (*GetSourceFiltersResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetSourceFiltersRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetSourceFilters",
		},
		SourceName: SourceName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetSourceFiltersResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetSourceFiltersResponse struct {
	resData
	// List of filters for the specified source
	Filters []struct {
		// Filter status (enabled or not)
		Enabled bool `json:"enabled"`
		// Filter type
		Type string `json:"type"`
		// Filter name
		Name string `json:"name"`
		// Filter settings
		Settings interface{} `json:"settings"`
	} `json:"filters"`
}

// Get settings of the specified source
type GetSourceSettingsRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
	// Type of the specified source. Useful for type-checking if you expect a
	// specific settings schema.
	SourceType string `json:"sourceType,omitempty"`
}

func (c *Client) GetSourceSettings(SourceName string, SourceType string) (*GetSourceSettingsResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetSourceSettingsRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetSourceSettings",
		},
		SourceName: SourceName,
		SourceType: SourceType,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetSourceSettingsResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetSourceSettingsResponse struct {
	resData
	// Source name
	SourceName string `json:"sourceName"`
	// Type of the specified source
	SourceType string `json:"sourceType"`
	// Source settings (varies between source types, may require some probing
	// around).
	SourceSettings interface{} `json:"sourceSettings"`
}

// Get a list of all available sources types
type GetSourceTypesListRequest struct {
	reqData
}

func (c *Client) GetSourceTypesList() (*GetSourceTypesListResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetSourceTypesListRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetSourceTypesList",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetSourceTypesListResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetSourceTypesListResponse struct {
	resData
	// Array of source types
	Types []struct {
		// Non-unique internal source type ID
		TypeId string `json:"typeId"`
		// Display name of the source type
		DisplayName string `json:"displayName"`
		// Type. Value is one of the following: "input", "filter", "transition" or
		// "other"
		Type string `json:"type"`
		// Default settings of this source type
		DefaultSettings interface{} `json:"defaultSettings"`
		// Source type capabilities
		Caps struct {
			// True if source of this type provide frames asynchronously
			IsAsync bool `json:"isAsync"`
			// True if sources of this type provide video
			HasVideo bool `json:"hasVideo"`
			// True if sources of this type provide audio
			HasAudio bool `json:"hasAudio"`
			// True if interaction with this sources of this type is possible
			CanInteract bool `json:"canInteract"`
			// True if sources of this type composite one or more sub-sources
			IsComposite bool `json:"isComposite"`
			// True if sources of this type should not be fully duplicated
			DoNotDuplicate bool `json:"doNotDuplicate"`
			// True if sources of this type may cause a feedback loop if it's audio is
			// monitored and shouldn't be
			DoNotSelfMonitor bool `json:"doNotSelfMonitor"`
		} `json:"caps"`
	} `json:"types"`
}

// List all sources available in the running OBS instance
type GetSourcesListRequest struct {
	reqData
}

func (c *Client) GetSourcesList() (*GetSourcesListResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetSourcesListRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetSourcesList",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetSourcesListResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetSourcesListResponse struct {
	resData
	// Array of sources
	Sources []struct {
		// Unique source name
		Name string `json:"name"`
		// Non-unique source internal type (a.k.a kind)
		TypeId string `json:"typeId"`
		// Source type. Value is one of the following: "input", "filter", "transition",
		// "scene" or "unknown"
		Type string `json:"type"`
	} `json:"sources"`
}

// Get configured special sources like Desktop Audio and Mic/Aux sources.
type GetSpecialSourcesRequest struct {
	reqData
}

func (c *Client) GetSpecialSources() (*GetSpecialSourcesResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetSpecialSourcesRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetSpecialSources",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetSpecialSourcesResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetSpecialSourcesResponse struct {
	resData
	// Name of the first Desktop Audio capture source.
	Desktop1 string `json:"desktop-1,omitempty"`
	// Name of the second Desktop Audio capture source.
	Desktop2 string `json:"desktop-2,omitempty"`
	// Name of the first Mic/Aux input source.
	Mic1 string `json:"mic-1,omitempty"`
	// Name of the second Mic/Aux input source.
	Mic2 string `json:"mic-2,omitempty"`
	// NAme of the third Mic/Aux input source.
	Mic3 string `json:"mic-3,omitempty"`
}

// Get OBS stats (almost the same info as provided in OBS' stats window)
type GetStatsRequest struct {
	reqData
}

func (c *Client) GetStats() (*GetStatsResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetStatsRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetStats",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetStatsResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetStatsResponse struct {
	resData
	// [OBS stats](#obsstats)
	Stats OBSStats `json:"stats"`
}

// Get the current streaming server settings.
type GetStreamSettingsRequest struct {
	reqData
}

func (c *Client) GetStreamSettings() (*GetStreamSettingsResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetStreamSettingsRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetStreamSettings",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetStreamSettingsResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetStreamSettingsResponse struct {
	resData
	// The type of streaming service configuration. Possible values: 'rtmp_custom'
	// or 'rtmp_common'.
	Type string `json:"type"`
	// Stream settings object.
	Settings struct {
		// The publish URL.
		Server string `json:"server"`
		// The publish key of the stream.
		Key string `json:"key"`
		// Indicates whether authentication should be used when connecting to the
		// streaming server.
		UseAuth bool `json:"use_auth"`
		// The username to use when accessing the streaming server. Only present if
		// `use_auth` is `true`.
		Username string `json:"username"`
		// The password to use when accessing the streaming server. Only present if
		// `use_auth` is `true`.
		Password string `json:"password"`
	} `json:"settings"`
}

// Get current streaming and recording status.
type GetStreamingStatusRequest struct {
	reqData
}

func (c *Client) GetStreamingStatus() (*GetStreamingStatusResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetStreamingStatusRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetStreamingStatus",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetStreamingStatusResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetStreamingStatusResponse struct {
	resData
	// Current streaming status.
	Streaming bool `json:"streaming"`
	// Current recording status.
	Recording bool `json:"recording"`
	// If recording is paused.
	RecordingPaused bool `json:"recording-paused"`
	// Current virtual cam status.
	Virtualcam bool `json:"virtualcam"`
	// Always false. Retrocompatibility with OBSRemote.
	PreviewOnly bool `json:"preview-only"`
	// Time elapsed since streaming started (only present if currently streaming).
	StreamTimecode string `json:"stream-timecode,omitempty"`
	// Time elapsed since recording started (only present if currently recording).
	RecTimecode string `json:"rec-timecode,omitempty"`
	// Time elapsed since virtual cam started (only present if virtual cam currently
	// active).
	VirtualcamTimecode string `json:"virtualcam-timecode,omitempty"`
}

// Indicates if Studio Mode is currently enabled.
type GetStudioModeStatusRequest struct {
	reqData
}

func (c *Client) GetStudioModeStatus() (*GetStudioModeStatusResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetStudioModeStatusRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetStudioModeStatus",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetStudioModeStatusResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetStudioModeStatusResponse struct {
	resData
	// Indicates if Studio Mode is enabled.
	StudioMode bool `json:"studio-mode"`
}

// Get the audio sync offset of a specified source.
type GetSyncOffsetRequest struct {
	reqData
	// Source name.
	Source string `json:"source"`
}

func (c *Client) GetSyncOffset(Source string) (*GetSyncOffsetResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetSyncOffsetRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetSyncOffset",
		},
		Source: Source,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetSyncOffsetResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetSyncOffsetResponse struct {
	resData
	// Source name.
	Name string `json:"name"`
	// The audio sync offset (in nanoseconds).
	Offset int `json:"offset"`
}

// Get the current properties of a Text Freetype 2 source.
type GetTextFreetype2PropertiesRequest struct {
	reqData
	// Source name.
	Source string `json:"source"`
}

func (c *Client) GetTextFreetype2Properties(Source string) (*GetTextFreetype2PropertiesResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetTextFreetype2PropertiesRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetTextFreetype2Properties",
		},
		Source: Source,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetTextFreetype2PropertiesResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetTextFreetype2PropertiesResponse struct {
	resData
	// Source name
	Source string `json:"source"`
	// Gradient top color.
	Color1 int `json:"color1"`
	// Gradient bottom color.
	Color2 int `json:"color2"`
	// Custom width (0 to disable).
	CustomWidth int `json:"custom_width"`
	// Drop shadow.
	DropShadow bool `json:"drop_shadow"`
	// Holds data for the font. Ex: `"font": { "face": "Arial", "flags": 0, "size":
	// 150, "style": "" }`
	Font struct {
		// Font face.
		Face string `json:"face"`
		// Font text styling flag. `Bold=1, Italic=2, Bold Italic=3, Underline=5,
		// Strikeout=8`
		Flags int `json:"flags"`
		// Font text size.
		Size int `json:"size"`
		// Font Style (unknown function).
		Style string `json:"style"`
	} `json:"font"`
	// Read text from the specified file.
	FromFile bool `json:"from_file"`
	// Chat log.
	LogMode bool `json:"log_mode"`
	// Outline.
	Outline bool `json:"outline"`
	// Text content to be displayed.
	Text string `json:"text"`
	// File path.
	TextFile string `json:"text_file"`
	// Word wrap.
	WordWrap bool `json:"word_wrap"`
}

// Get the current properties of a Text GDI Plus source.
type GetTextGDIPlusPropertiesRequest struct {
	reqData
	// Source name.
	Source string `json:"source"`
}

func (c *Client) GetTextGDIPlusProperties(Source string) (*GetTextGDIPlusPropertiesResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetTextGDIPlusPropertiesRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetTextGDIPlusProperties",
		},
		Source: Source,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetTextGDIPlusPropertiesResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetTextGDIPlusPropertiesResponse struct {
	resData
	// Source name.
	Source string `json:"source"`
	// Text Alignment ("left", "center", "right").
	Align string `json:"align"`
	// Background color.
	BkColor int `json:"bk_color"`
	// Background opacity (0-100).
	BkOpacity int `json:"bk_opacity"`
	// Chat log.
	Chatlog bool `json:"chatlog"`
	// Chat log lines.
	ChatlogLines int `json:"chatlog_lines"`
	// Text color.
	Color int `json:"color"`
	// Extents wrap.
	Extents bool `json:"extents"`
	// Extents cx.
	ExtentsCx int `json:"extents_cx"`
	// Extents cy.
	ExtentsCy int `json:"extents_cy"`
	// File path name.
	File string `json:"file"`
	// Read text from the specified file.
	ReadFromFile bool `json:"read_from_file"`
	// Holds data for the font. Ex: `"font": { "face": "Arial", "flags": 0, "size":
	// 150, "style": "" }`
	Font struct {
		// Font face.
		Face string `json:"face"`
		// Font text styling flag. `Bold=1, Italic=2, Bold Italic=3, Underline=5,
		// Strikeout=8`
		Flags int `json:"flags"`
		// Font text size.
		Size int `json:"size"`
		// Font Style (unknown function).
		Style string `json:"style"`
	} `json:"font"`
	// Gradient enabled.
	Gradient bool `json:"gradient"`
	// Gradient color.
	GradientColor int `json:"gradient_color"`
	// Gradient direction.
	GradientDir float32 `json:"gradient_dir"`
	// Gradient opacity (0-100).
	GradientOpacity int `json:"gradient_opacity"`
	// Outline.
	Outline bool `json:"outline"`
	// Outline color.
	OutlineColor int `json:"outline_color"`
	// Outline size.
	OutlineSize int `json:"outline_size"`
	// Outline opacity (0-100).
	OutlineOpacity int `json:"outline_opacity"`
	// Text content to be displayed.
	Text string `json:"text"`
	// Text vertical alignment ("top", "center", "bottom").
	Valign string `json:"valign"`
	// Vertical text enabled.
	Vertical bool `json:"vertical"`
}

// Get the duration of the currently selected transition if supported.
type GetTransitionDurationRequest struct {
	reqData
}

func (c *Client) GetTransitionDuration() (*GetTransitionDurationResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetTransitionDurationRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetTransitionDuration",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetTransitionDurationResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetTransitionDurationResponse struct {
	resData
	// Duration of the current transition (in milliseconds).
	TransitionDuration int `json:"transition-duration"`
}

// List of all transitions available in the frontend's dropdown menu.
type GetTransitionListRequest struct {
	reqData
}

func (c *Client) GetTransitionList() (*GetTransitionListResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetTransitionListRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetTransitionList",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetTransitionListResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetTransitionListResponse struct {
	resData
	// Name of the currently active transition.
	CurrentTransition string `json:"current-transition"`
	// List of transitions.
	Transitions []struct {
		// Name of the transition.
		Name string `json:"name"`
	} `json:"transitions"`
}

// Get the position of the current transition.
type GetTransitionPositionRequest struct {
	reqData
}

func (c *Client) GetTransitionPosition() (*GetTransitionPositionResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetTransitionPositionRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetTransitionPosition",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetTransitionPositionResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetTransitionPositionResponse struct {
	resData
	// current transition position. This value will be between 0.0 and 1.0. Note:
	// Transition returns 1.0 when not active.
	Position float64 `json:"position"`
}

// Get the current settings of a transition
type GetTransitionSettingsRequest struct {
	reqData
	// Transition name
	TransitionName string `json:"transitionName"`
}

func (c *Client) GetTransitionSettings(TransitionName string) (*GetTransitionSettingsResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetTransitionSettingsRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetTransitionSettings",
		},
		TransitionName: TransitionName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetTransitionSettingsResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetTransitionSettingsResponse struct {
	resData
	// Current transition settings
	TransitionSettings interface{} `json:"transitionSettings"`
}

// Returns the latest version of the plugin and the API.
type GetVersionRequest struct {
	reqData
}

func (c *Client) GetVersion() (*GetVersionResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetVersionRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetVersion",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetVersionResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetVersionResponse struct {
	resData
	// OBSRemote compatible API version. Fixed to 1.1 for retrocompatibility.
	Version float64 `json:"version"`
	// obs-websocket plugin version.
	ObsWebsocketVersion string `json:"obs-websocket-version"`
	// OBS Studio program version.
	ObsStudioVersion string `json:"obs-studio-version"`
	// List of available request types, formatted as a comma-separated list string
	// (e.g. : "Method1,Method2,Method3").
	AvailableRequests string `json:"available-requests"`
	// List of supported formats for features that use image export (like the
	// TakeSourceScreenshot request type) formatted as a comma-separated list string
	SupportedImageExportFormats string `json:"supported-image-export-formats"`
}

// Get basic OBS video information
type GetVideoInfoRequest struct {
	reqData
}

func (c *Client) GetVideoInfo() (*GetVideoInfoResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetVideoInfoRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetVideoInfo",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetVideoInfoResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetVideoInfoResponse struct {
	resData
	// Base (canvas) width
	BaseWidth int `json:"baseWidth"`
	// Base (canvas) height
	BaseHeight int `json:"baseHeight"`
	// Output width
	OutputWidth int `json:"outputWidth"`
	// Output height
	OutputHeight int `json:"outputHeight"`
	// Scaling method used if output size differs from base size
	ScaleType string `json:"scaleType"`
	// Frames rendered per second
	Fps float64 `json:"fps"`
	// Video color format
	VideoFormat string `json:"videoFormat"`
	// Color space for YUV
	ColorSpace string `json:"colorSpace"`
	// Color range (full or partial)
	ColorRange string `json:"colorRange"`
}

// Get current virtual cam status.
type GetVirtualCamStatusRequest struct {
	reqData
}

func (c *Client) GetVirtualCamStatus() (*GetVirtualCamStatusResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetVirtualCamStatusRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetVirtualCamStatus",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetVirtualCamStatusResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetVirtualCamStatusResponse struct {
	resData
	// Current virtual camera status.
	IsVirtualCam bool `json:"isVirtualCam"`
	// Time elapsed since virtual cam started (only present if virtual cam currently
	// active).
	VirtualCamTimecode string `json:"virtualCamTimecode,omitempty"`
}

// Get the volume of the specified source. Default response uses mul format, NOT
// SLIDER PERCENTAGE.
type GetVolumeRequest struct {
	reqData
	// Source name.
	Source string `json:"source"`
	// Output volume in decibels of attenuation instead of amplitude/mul.
	UseDecibel *bool `json:"useDecibel,omitempty"`
}

func (c *Client) GetVolume(Source string, UseDecibel *bool) (*GetVolumeResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := GetVolumeRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "GetVolume",
		},
		Source:     Source,
		UseDecibel: UseDecibel,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &GetVolumeResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type GetVolumeResponse struct {
	resData
	// Source name.
	Name string `json:"name"`
	// Volume of the source. Between `0.0` and `20.0` if using mul, under `26.0` if
	// using dB.
	Volume float64 `json:"volume"`
	// Indicates whether the source is muted.
	Muted bool `json:"muted"`
}

// List existing outputs
type ListOutputsRequest struct {
	reqData
}

func (c *Client) ListOutputs() (*ListOutputsResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := ListOutputsRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "ListOutputs",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &ListOutputsResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type ListOutputsResponse struct {
	resData
	// Outputs list
	Outputs []Output `json:"outputs"`
}

// Get a list of available profiles.
type ListProfilesRequest struct {
	reqData
}

func (c *Client) ListProfiles() (*ListProfilesResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := ListProfilesRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "ListProfiles",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &ListProfilesResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type ListProfilesResponse struct {
	resData
	// List of available profiles.
	Profiles []struct {
		// Filter name
		ProfileName string `json:"profile-name"`
	} `json:"profiles"`
}

// List available scene collections
type ListSceneCollectionsRequest struct {
	reqData
}

func (c *Client) ListSceneCollections() (*ListSceneCollectionsResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := ListSceneCollectionsRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "ListSceneCollections",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &ListSceneCollectionsResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type ListSceneCollectionsResponse struct {
	resData
	// Scene collections list
	SceneCollections []ScenesCollection `json:"scene-collections"`
}

// Move a filter in the chain (relative positioning)
type MoveSourceFilterRequest struct {
	reqData
	// Name of the source to which the filter belongs
	SourceName string `json:"sourceName"`
	// Name of the filter to reorder
	FilterName string `json:"filterName"`
	// How to move the filter around in the source's filter chain. Either "up",
	// "down", "top" or "bottom".
	MovementType string `json:"movementType"`
}

func (c *Client) MoveSourceFilter(SourceName string, FilterName string, MovementType string) (*MoveSourceFilterResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := MoveSourceFilterRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "MoveSourceFilter",
		},
		SourceName:   SourceName,
		FilterName:   FilterName,
		MovementType: MovementType,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &MoveSourceFilterResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type MoveSourceFilterResponse struct {
	resData
}

// Skip to the next media item in the playlist. Supports only vlc media source
// (as of OBS v25.0.8)
type NextMediaRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
}

func (c *Client) NextMedia(SourceName string) (*NextMediaResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := NextMediaRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "NextMedia",
		},
		SourceName: SourceName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &NextMediaResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type NextMediaResponse struct {
	resData
}

// Open a projector window or create a projector on a monitor. Requires OBS
// v24.0.4 or newer.
type OpenProjectorRequest struct {
	reqData
	// Type of projector: `Preview` (default), `Source`, `Scene`, `StudioProgram`,
	// or `Multiview` (case insensitive).
	Type string `json:"type,omitempty"`
	// Monitor to open the projector on. If -1 or omitted, opens a window.
	Monitor *int `json:"monitor,omitempty"`
	// Size and position of the projector window (only if monitor is -1). Encoded in
	// Base64 using [Qt's geometry
	// encoding](https://doc.qt.io/qt-5/qwidget.html#saveGeometry). Corresponds to
	// OBS's saved projectors.
	Geometry string `json:"geometry,omitempty"`
	// Name of the source or scene to be displayed (ignored for other projector
	// types).
	Name string `json:"name,omitempty"`
}

func (c *Client) OpenProjector(Type string, Monitor *int, Geometry string, Name string) (*OpenProjectorResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := OpenProjectorRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "OpenProjector",
		},
		Type:     Type,
		Monitor:  Monitor,
		Geometry: Geometry,
		Name:     Name,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &OpenProjectorResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type OpenProjectorResponse struct {
	resData
}

// Pause the current recording. Returns an error if recording is not active or
// already paused.
type PauseRecordingRequest struct {
	reqData
}

func (c *Client) PauseRecording() (*PauseRecordingResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := PauseRecordingRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "PauseRecording",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &PauseRecordingResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type PauseRecordingResponse struct {
	resData
}

// Pause or play a media source. Supports ffmpeg and vlc media sources (as of
// OBS v25.0.8) Note :Leaving out `playPause` toggles the current pause state
type PlayPauseMediaRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
	// (optional) Whether to pause or play the source. `false` for play, `true` for
	// pause.
	PlayPause bool `json:"playPause"`
}

func (c *Client) PlayPauseMedia(SourceName string, PlayPause bool) (*PlayPauseMediaResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := PlayPauseMediaRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "PlayPauseMedia",
		},
		SourceName: SourceName,
		PlayPause:  PlayPause,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &PlayPauseMediaResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type PlayPauseMediaResponse struct {
	resData
}

// Go to the previous media item in the playlist. Supports only vlc media source
// (as of OBS v25.0.8)
type PreviousMediaRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
}

func (c *Client) PreviousMedia(SourceName string) (*PreviousMediaResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := PreviousMediaRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "PreviousMedia",
		},
		SourceName: SourceName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &PreviousMediaResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type PreviousMediaResponse struct {
	resData
}

// Refreshes the specified browser source.
type RefreshBrowserSourceRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
}

func (c *Client) RefreshBrowserSource(SourceName string) (*RefreshBrowserSourceResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := RefreshBrowserSourceRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "RefreshBrowserSource",
		},
		SourceName: SourceName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &RefreshBrowserSourceResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type RefreshBrowserSourceResponse struct {
	resData
}

// Release the T-Bar (like a user releasing their mouse button after moving it).
// *YOU MUST CALL THIS if you called `SetTBarPosition` with the `release`
// parameter set to `false`.*
type ReleaseTBarRequest struct {
	reqData
}

func (c *Client) ReleaseTBar() (*ReleaseTBarResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := ReleaseTBarRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "ReleaseTBar",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &ReleaseTBarResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type ReleaseTBarResponse struct {
	resData
}

// Remove a filter from a source
type RemoveFilterFromSourceRequest struct {
	reqData
	// Name of the source from which the specified filter is removed
	SourceName string `json:"sourceName"`
	// Name of the filter to remove
	FilterName string `json:"filterName"`
}

func (c *Client) RemoveFilterFromSource(SourceName string, FilterName string) (*RemoveFilterFromSourceResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := RemoveFilterFromSourceRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "RemoveFilterFromSource",
		},
		SourceName: SourceName,
		FilterName: FilterName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &RemoveFilterFromSourceResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type RemoveFilterFromSourceResponse struct {
	resData
}

// Remove any transition override on a scene.
type RemoveSceneTransitionOverrideRequest struct {
	reqData
	// Name of the scene to switch to.
	SceneName string `json:"sceneName"`
}

func (c *Client) RemoveSceneTransitionOverride(SceneName string) (*RemoveSceneTransitionOverrideResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := RemoveSceneTransitionOverrideRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "RemoveSceneTransitionOverride",
		},
		SceneName: SceneName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &RemoveSceneTransitionOverrideResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type RemoveSceneTransitionOverrideResponse struct {
	resData
}

// Changes the order of scene items in the requested scene.
type ReorderSceneItemsRequest struct {
	reqData
	// Name of the scene to reorder (defaults to current).
	Scene string `json:"scene,omitempty"`
	// Ordered list of objects with name and/or id specified. Id preferred due to
	// uniqueness per scene
	Items []ReorderSceneItemsItems `json:"items"`
}

func (c *Client) ReorderSceneItems(Scene string, Items []ReorderSceneItemsItems) (*ReorderSceneItemsResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := ReorderSceneItemsRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "ReorderSceneItems",
		},
		Scene: Scene,
		Items: Items,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &ReorderSceneItemsResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type ReorderSceneItemsResponse struct {
	resData
}

// Move a filter in the chain (absolute index positioning)
type ReorderSourceFilterRequest struct {
	reqData
	// Name of the source to which the filter belongs
	SourceName string `json:"sourceName"`
	// Name of the filter to reorder
	FilterName string `json:"filterName"`
	// Desired position of the filter in the chain
	NewIndex int `json:"newIndex"`
}

func (c *Client) ReorderSourceFilter(SourceName string, FilterName string, NewIndex int) (*ReorderSourceFilterResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := ReorderSourceFilterRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "ReorderSourceFilter",
		},
		SourceName: SourceName,
		FilterName: FilterName,
		NewIndex:   NewIndex,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &ReorderSourceFilterResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type ReorderSourceFilterResponse struct {
	resData
}

// Reset a scene item.
type ResetSceneItemRequest struct {
	reqData
	// Name of the scene the scene item belongs to. Defaults to the current scene.
	SceneName string `json:"scene-name,omitempty"`
	// Scene Item name (if this field is a string) or specification (if it is an
	// object).
	Item ResetSceneItemItem `json:"item"`
}

func (c *Client) ResetSceneItem(SceneName string, Item ResetSceneItemItem) (*ResetSceneItemResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := ResetSceneItemRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "ResetSceneItem",
		},
		SceneName: SceneName,
		Item:      Item,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &ResetSceneItemResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type ResetSceneItemResponse struct {
	resData
}

// Restart a media source. Supports ffmpeg and vlc media sources (as of OBS
// v25.0.8)
type RestartMediaRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
}

func (c *Client) RestartMedia(SourceName string) (*RestartMediaResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := RestartMediaRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "RestartMedia",
		},
		SourceName: SourceName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &RestartMediaResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type RestartMediaResponse struct {
	resData
}

// Resume/unpause the current recording (if paused). Returns an error if
// recording is not active or not paused.
type ResumeRecordingRequest struct {
	reqData
}

func (c *Client) ResumeRecording() (*ResumeRecordingResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := ResumeRecordingRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "ResumeRecording",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &ResumeRecordingResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type ResumeRecordingResponse struct {
	resData
}

// Flush and save the contents of the Replay Buffer to disk. This is basically
// the same as triggering the "Save Replay Buffer" hotkey. Will return an
// `error` if the Replay Buffer is not active.
type SaveReplayBufferRequest struct {
	reqData
}

func (c *Client) SaveReplayBuffer() (*SaveReplayBufferResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SaveReplayBufferRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SaveReplayBuffer",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SaveReplayBufferResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SaveReplayBufferResponse struct {
	resData
}

// Save the current streaming server settings to disk.
type SaveStreamSettingsRequest struct {
	reqData
}

func (c *Client) SaveStreamSettings() (*SaveStreamSettingsResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SaveStreamSettingsRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SaveStreamSettings",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SaveStreamSettingsResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SaveStreamSettingsResponse struct {
	resData
}

// Scrub media using a supplied offset. Supports ffmpeg and vlc media sources
// (as of OBS v25.0.8) Note: Due to processing/network delays, this request is
// not perfect. The processing rate of this request has also not been tested.
type ScrubMediaRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
	// Millisecond offset (positive or negative) to offset the current media
	// position.
	TimeOffset int `json:"timeOffset"`
}

func (c *Client) ScrubMedia(SourceName string, TimeOffset int) (*ScrubMediaResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := ScrubMediaRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "ScrubMedia",
		},
		SourceName: SourceName,
		TimeOffset: TimeOffset,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &ScrubMediaResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type ScrubMediaResponse struct {
	resData
}

// Send the provided text as embedded CEA-608 caption data.
type SendCaptionsRequest struct {
	reqData
	// Captions text
	Text string `json:"text"`
}

func (c *Client) SendCaptions(Text string) (*SendCaptionsResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SendCaptionsRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SendCaptions",
		},
		Text: Text,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SendCaptionsResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SendCaptionsResponse struct {
	resData
}

// Set the audio monitoring type of the specified source.
type SetAudioMonitorTypeRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
	// The monitor type to use. Options: `none`, `monitorOnly`, `monitorAndOutput`.
	MonitorType string `json:"monitorType"`
}

func (c *Client) SetAudioMonitorType(SourceName string, MonitorType string) (*SetAudioMonitorTypeResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetAudioMonitorTypeRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetAudioMonitorType",
		},
		SourceName:  SourceName,
		MonitorType: MonitorType,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetAudioMonitorTypeResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetAudioMonitorTypeResponse struct {
	resData
}

// Changes whether an audio track is active for a source.
type SetAudioTracksRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
	// Audio tracks 1-6.
	Track int `json:"track"`
	// Whether audio track is active or not.
	Active bool `json:"active"`
}

func (c *Client) SetAudioTracks(SourceName string, Track int, Active bool) (*SetAudioTracksResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetAudioTracksRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetAudioTracks",
		},
		SourceName: SourceName,
		Track:      Track,
		Active:     Active,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetAudioTracksResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetAudioTracksResponse struct {
	resData
}

// Set current properties for a Browser Source.
//
// Deprecated:
// Since 4.8.0. Prefer the use of SetSourceSettings. Will be removed in v5.0.0
type SetBrowserSourcePropertiesRequest struct {
	reqData
	// Name of the source.
	Source string `json:"source"`
	// Indicates that a local file is in use.
	IsLocalFile *bool `json:"is_local_file,omitempty"`
	// file path.
	LocalFile string `json:"local_file,omitempty"`
	// Url.
	Url string `json:"url,omitempty"`
	// CSS to inject.
	Css string `json:"css,omitempty"`
	// Width.
	Width *int `json:"width,omitempty"`
	// Height.
	Height *int `json:"height,omitempty"`
	// Framerate.
	Fps *int `json:"fps,omitempty"`
	// Indicates whether the source should be shutdown when not visible.
	Shutdown *bool `json:"shutdown,omitempty"`
	// Visibility of the scene item.
	Render *bool `json:"render,omitempty"`
}

func (c *Client) SetBrowserSourceProperties(Source string, IsLocalFile *bool, LocalFile string, Url string, Css string, Width *int, Height *int, Fps *int, Shutdown *bool, Render *bool) (*SetBrowserSourcePropertiesResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetBrowserSourcePropertiesRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetBrowserSourceProperties",
		},
		Source:      Source,
		IsLocalFile: IsLocalFile,
		LocalFile:   LocalFile,
		Url:         Url,
		Css:         Css,
		Width:       Width,
		Height:      Height,
		Fps:         Fps,
		Shutdown:    Shutdown,
		Render:      Render,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetBrowserSourcePropertiesResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetBrowserSourcePropertiesResponse struct {
	resData
}

// Set the currently active profile.
type SetCurrentProfileRequest struct {
	reqData
	// Name of the desired profile.
	ProfileName string `json:"profile-name"`
}

func (c *Client) SetCurrentProfile(ProfileName string) (*SetCurrentProfileResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetCurrentProfileRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetCurrentProfile",
		},
		ProfileName: ProfileName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetCurrentProfileResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetCurrentProfileResponse struct {
	resData
}

// Switch to the specified scene.
type SetCurrentSceneRequest struct {
	reqData
	// Name of the scene to switch to.
	SceneName string `json:"scene-name"`
}

func (c *Client) SetCurrentScene(SceneName string) (*SetCurrentSceneResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetCurrentSceneRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetCurrentScene",
		},
		SceneName: SceneName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetCurrentSceneResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetCurrentSceneResponse struct {
	resData
}

// Change the active scene collection.
type SetCurrentSceneCollectionRequest struct {
	reqData
	// Name of the desired scene collection.
	ScName string `json:"sc-name"`
}

func (c *Client) SetCurrentSceneCollection(ScName string) (*SetCurrentSceneCollectionResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetCurrentSceneCollectionRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetCurrentSceneCollection",
		},
		ScName: ScName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetCurrentSceneCollectionResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetCurrentSceneCollectionResponse struct {
	resData
}

// Set the active transition.
type SetCurrentTransitionRequest struct {
	reqData
	// The name of the transition.
	TransitionName string `json:"transition-name"`
}

func (c *Client) SetCurrentTransition(TransitionName string) (*SetCurrentTransitionResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetCurrentTransitionRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetCurrentTransition",
		},
		TransitionName: TransitionName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetCurrentTransitionResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetCurrentTransitionResponse struct {
	resData
}

// Set the filename formatting string
type SetFilenameFormattingRequest struct {
	reqData
	// Filename formatting string to set.
	FilenameFormatting string `json:"filename-formatting"`
}

func (c *Client) SetFilenameFormatting(FilenameFormatting string) (*SetFilenameFormattingResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetFilenameFormattingRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetFilenameFormatting",
		},
		FilenameFormatting: FilenameFormatting,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetFilenameFormattingResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetFilenameFormattingResponse struct {
	resData
}

// Enable/disable sending of the Heartbeat event
//
// Deprecated:
// Since 4.9.0. Please poll the appropriate data using requests. Will be removed
// in v5.0.0.
type SetHeartbeatRequest struct {
	reqData
	// Starts/Stops emitting heartbeat messages
	Enable bool `json:"enable"`
}

func (c *Client) SetHeartbeat(Enable bool) (*SetHeartbeatResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetHeartbeatRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetHeartbeat",
		},
		Enable: Enable,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetHeartbeatResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetHeartbeatResponse struct {
	resData
}

// Set the timestamp of a media source. Supports ffmpeg and vlc media sources
// (as of OBS v25.0.8)
type SetMediaTimeRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
	// Milliseconds to set the timestamp to.
	Timestamp int `json:"timestamp"`
}

func (c *Client) SetMediaTime(SourceName string, Timestamp int) (*SetMediaTimeResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetMediaTimeRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetMediaTime",
		},
		SourceName: SourceName,
		Timestamp:  Timestamp,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetMediaTimeResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetMediaTimeResponse struct {
	resData
}

// Sets the mute status of a specified source.
type SetMuteRequest struct {
	reqData
	// Source name.
	Source string `json:"source"`
	// Desired mute status.
	Mute bool `json:"mute"`
}

func (c *Client) SetMute(Source string, Mute bool) (*SetMuteResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetMuteRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetMute",
		},
		Source: Source,
		Mute:   Mute,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetMuteResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetMuteResponse struct {
	resData
}

// Set the active preview scene. Will return an `error` if Studio Mode is not
// enabled.
type SetPreviewSceneRequest struct {
	reqData
	// The name of the scene to preview.
	SceneName string `json:"scene-name"`
}

func (c *Client) SetPreviewScene(SceneName string) (*SetPreviewSceneResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetPreviewSceneRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetPreviewScene",
		},
		SceneName: SceneName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetPreviewSceneResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetPreviewSceneResponse struct {
	resData
}

//   Note: If `SetRecordingFolder` is called while a recording is in progress,
// the change won't be applied immediately and will be effective on the next
// recording.
type SetRecordingFolderRequest struct {
	reqData
	// Path of the recording folder.
	RecFolder string `json:"rec-folder"`
}

func (c *Client) SetRecordingFolder(RecFolder string) (*SetRecordingFolderResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetRecordingFolderRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetRecordingFolder",
		},
		RecFolder: RecFolder,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetRecordingFolderResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetRecordingFolderResponse struct {
	resData
}

// Sets the crop coordinates of the specified source item.
//
// Deprecated:
// Since 4.3.0. Prefer the use of SetSceneItemProperties.
type SetSceneItemCropRequest struct {
	reqData
	// Name of the scene the scene item belongs to. Defaults to the current scene.
	SceneName string `json:"scene-name,omitempty"`
	// Scene Item name.
	Item string `json:"item"`
	// Pixel position of the top of the source item.
	Top int `json:"top"`
	// Pixel position of the bottom of the source item.
	Bottom int `json:"bottom"`
	// Pixel position of the left of the source item.
	Left int `json:"left"`
	// Pixel position of the right of the source item.
	Right int `json:"right"`
}

func (c *Client) SetSceneItemCrop(SceneName string, Item string, Top int, Bottom int, Left int, Right int) (*SetSceneItemCropResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetSceneItemCropRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetSceneItemCrop",
		},
		SceneName: SceneName,
		Item:      Item,
		Top:       Top,
		Bottom:    Bottom,
		Left:      Left,
		Right:     Right,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetSceneItemCropResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetSceneItemCropResponse struct {
	resData
}

// Sets the coordinates of a specified source item.
//
// Deprecated:
// Since 4.3.0. Prefer the use of SetSceneItemProperties.
type SetSceneItemPositionRequest struct {
	reqData
	// Name of the scene the scene item belongs to. Defaults to the current scene.
	SceneName string `json:"scene-name,omitempty"`
	// Scene Item name.
	Item string `json:"item"`
	// X coordinate.
	X float64 `json:"x"`
	// Y coordinate.
	Y float64 `json:"y"`
}

func (c *Client) SetSceneItemPosition(SceneName string, Item string, X float64, Y float64) (*SetSceneItemPositionResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetSceneItemPositionRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetSceneItemPosition",
		},
		SceneName: SceneName,
		Item:      Item,
		X:         X,
		Y:         Y,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetSceneItemPositionResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetSceneItemPositionResponse struct {
	resData
}

// Sets the scene specific properties of a source. Unspecified properties will
// remain unchanged. Coordinates are relative to the item's parent (the scene or
// group it belongs to).
type SetSceneItemPropertiesRequest struct {
	reqData
	// Name of the scene the source item belongs to. Defaults to the current scene.
	SceneName string `json:"scene-name,omitempty"`
	// Scene Item name (if this field is a string) or specification (if it is an
	// object).
	Item SetSceneItemPropertiesItem `json:"item"`
	// The new x position of the source.
	Position SetSceneItemPropertiesPosition `json:"position"`
	// The new clockwise rotation of the item in degrees.
	Rotation *float64 `json:"rotation,omitempty"`
	// The new x scale of the item.
	Scale SetSceneItemPropertiesScale `json:"scale"`
	// The new amount of pixels cropped off the top of the source before scaling.
	Crop SetSceneItemPropertiesCrop `json:"crop"`
	// The new visibility of the source. 'true' shows source, 'false' hides source.
	Visible *bool `json:"visible,omitempty"`
	// The new locked status of the source. 'true' keeps it in its current position,
	// 'false' allows movement.
	Locked *bool `json:"locked,omitempty"`
	// The new bounds type of the source. Can be "OBS_BOUNDS_STRETCH",
	// "OBS_BOUNDS_SCALE_INNER", "OBS_BOUNDS_SCALE_OUTER",
	// "OBS_BOUNDS_SCALE_TO_WIDTH", "OBS_BOUNDS_SCALE_TO_HEIGHT",
	// "OBS_BOUNDS_MAX_ONLY" or "OBS_BOUNDS_NONE".
	Bounds SetSceneItemPropertiesBounds `json:"bounds"`
}

func (c *Client) SetSceneItemProperties(SceneName string, Item SetSceneItemPropertiesItem, Position SetSceneItemPropertiesPosition, Rotation *float64, Scale SetSceneItemPropertiesScale, Crop SetSceneItemPropertiesCrop, Visible *bool, Locked *bool, Bounds SetSceneItemPropertiesBounds) (*SetSceneItemPropertiesResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetSceneItemPropertiesRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetSceneItemProperties",
		},
		SceneName: SceneName,
		Item:      Item,
		Position:  Position,
		Rotation:  Rotation,
		Scale:     Scale,
		Crop:      Crop,
		Visible:   Visible,
		Locked:    Locked,
		Bounds:    Bounds,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetSceneItemPropertiesResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetSceneItemPropertiesResponse struct {
	resData
}

// Show or hide a specified source item in a specified scene.
type SetSceneItemRenderRequest struct {
	reqData
	// Name of the scene the scene item belongs to. Defaults to the currently active
	// scene.
	SceneName string `json:"scene-name,omitempty"`
	// Scene Item name.
	Source string `json:"source,omitempty"`
	// Scene Item id
	Item *int `json:"item,omitempty"`
	// true = shown ; false = hidden
	Render bool `json:"render"`
}

func (c *Client) SetSceneItemRender(SceneName string, Source string, Item *int, Render bool) (*SetSceneItemRenderResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetSceneItemRenderRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetSceneItemRender",
		},
		SceneName: SceneName,
		Source:    Source,
		Item:      Item,
		Render:    Render,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetSceneItemRenderResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetSceneItemRenderResponse struct {
	resData
}

// Set the transform of the specified source item.
//
// Deprecated:
// Since 4.3.0. Prefer the use of SetSceneItemProperties.
type SetSceneItemTransformRequest struct {
	reqData
	// Name of the scene the scene item belongs to. Defaults to the current scene.
	SceneName string `json:"scene-name,omitempty"`
	// Scene Item name.
	Item string `json:"item"`
	// Width scale factor.
	XScale float64 `json:"x-scale"`
	// Height scale factor.
	YScale float64 `json:"y-scale"`
	// Source item rotation (in degrees).
	Rotation float64 `json:"rotation"`
}

func (c *Client) SetSceneItemTransform(SceneName string, Item string, XScale float64, YScale float64, Rotation float64) (*SetSceneItemTransformResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetSceneItemTransformRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetSceneItemTransform",
		},
		SceneName: SceneName,
		Item:      Item,
		XScale:    XScale,
		YScale:    YScale,
		Rotation:  Rotation,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetSceneItemTransformResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetSceneItemTransformResponse struct {
	resData
}

// Set a scene to use a specific transition override.
type SetSceneTransitionOverrideRequest struct {
	reqData
	// Name of the scene to switch to.
	SceneName string `json:"sceneName"`
	// Name of the transition to use.
	TransitionName string `json:"transitionName"`
	// Duration in milliseconds of the transition if transition is not fixed.
	// Defaults to the current duration specified in the UI if there is no current
	// override and this value is not given.
	TransitionDuration *int `json:"transitionDuration,omitempty"`
}

func (c *Client) SetSceneTransitionOverride(SceneName string, TransitionName string, TransitionDuration *int) (*SetSceneTransitionOverrideResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetSceneTransitionOverrideRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetSceneTransitionOverride",
		},
		SceneName:          SceneName,
		TransitionName:     TransitionName,
		TransitionDuration: TransitionDuration,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetSceneTransitionOverrideResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetSceneTransitionOverrideResponse struct {
	resData
}

// Update settings of a filter
type SetSourceFilterSettingsRequest struct {
	reqData
	// Name of the source to which the filter belongs
	SourceName string `json:"sourceName"`
	// Name of the filter to reconfigure
	FilterName string `json:"filterName"`
	// New settings. These will be merged to the current filter settings.
	FilterSettings interface{} `json:"filterSettings"`
}

func (c *Client) SetSourceFilterSettings(SourceName string, FilterName string, FilterSettings interface{}) (*SetSourceFilterSettingsResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetSourceFilterSettingsRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetSourceFilterSettings",
		},
		SourceName:     SourceName,
		FilterName:     FilterName,
		FilterSettings: FilterSettings,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetSourceFilterSettingsResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetSourceFilterSettingsResponse struct {
	resData
}

// Change the visibility/enabled state of a filter
type SetSourceFilterVisibilityRequest struct {
	reqData
	// Source name
	SourceName string `json:"sourceName"`
	// Source filter name
	FilterName string `json:"filterName"`
	// New filter state
	FilterEnabled bool `json:"filterEnabled"`
}

func (c *Client) SetSourceFilterVisibility(SourceName string, FilterName string, FilterEnabled bool) (*SetSourceFilterVisibilityResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetSourceFilterVisibilityRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetSourceFilterVisibility",
		},
		SourceName:    SourceName,
		FilterName:    FilterName,
		FilterEnabled: FilterEnabled,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetSourceFilterVisibilityResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetSourceFilterVisibilityResponse struct {
	resData
}

//   Note: If the new name already exists as a source, obs-websocket will return
// an error.
type SetSourceNameRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
	// New source name.
	NewName string `json:"newName"`
}

func (c *Client) SetSourceName(SourceName string, NewName string) (*SetSourceNameResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetSourceNameRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetSourceName",
		},
		SourceName: SourceName,
		NewName:    NewName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetSourceNameResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetSourceNameResponse struct {
	resData
}

// Set settings of the specified source.
type SetSourceSettingsRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
	// Type of the specified source. Useful for type-checking to avoid settings a
	// set of settings incompatible with the actual source's type.
	SourceType string `json:"sourceType,omitempty"`
	// Source settings (varies between source types, may require some probing
	// around).
	SourceSettings interface{} `json:"sourceSettings"`
}

func (c *Client) SetSourceSettings(SourceName string, SourceType string, SourceSettings interface{}) (*SetSourceSettingsResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetSourceSettingsRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetSourceSettings",
		},
		SourceName:     SourceName,
		SourceType:     SourceType,
		SourceSettings: SourceSettings,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetSourceSettingsResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetSourceSettingsResponse struct {
	resData
	// Source name
	SourceName string `json:"sourceName"`
	// Type of the specified source
	SourceType string `json:"sourceType"`
	// Updated source settings
	SourceSettings interface{} `json:"sourceSettings"`
}

// Sets one or more attributes of the current streaming server settings. Any
// options not passed will remain unchanged. Returns the updated settings in
// response. If 'type' is different than the current streaming service type, all
// settings are required. Returns the full settings of the stream (the same as
// GetStreamSettings).
type SetStreamSettingsRequest struct {
	reqData
	// The type of streaming service configuration, usually `rtmp_custom` or
	// `rtmp_common`.
	Type string `json:"type"`
	// The actual settings of the stream.
	Settings SetStreamSettingsSettings `json:"settings"`
	// Persist the settings to disk.
	Save bool `json:"save"`
}

func (c *Client) SetStreamSettings(Type string, Settings SetStreamSettingsSettings, Save bool) (*SetStreamSettingsResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetStreamSettingsRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetStreamSettings",
		},
		Type:     Type,
		Settings: Settings,
		Save:     Save,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetStreamSettingsResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetStreamSettingsResponse struct {
	resData
}

// Set the audio sync offset of a specified source.
type SetSyncOffsetRequest struct {
	reqData
	// Source name.
	Source string `json:"source"`
	// The desired audio sync offset (in nanoseconds).
	Offset int `json:"offset"`
}

func (c *Client) SetSyncOffset(Source string, Offset int) (*SetSyncOffsetResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetSyncOffsetRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetSyncOffset",
		},
		Source: Source,
		Offset: Offset,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetSyncOffsetResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetSyncOffsetResponse struct {
	resData
}

//   If your code needs to perform multiple successive T-Bar moves (e.g. : in an
// animation, or in response to a user moving a T-Bar control in your User
// Interface), set `release` to false and call `ReleaseTBar` later once the
// animation/interaction is over.
type SetTBarPositionRequest struct {
	reqData
	// T-Bar position. This value must be between 0.0 and 1.0.
	Position float64 `json:"position"`
	// Whether or not the T-Bar gets released automatically after setting its new
	// position (like a user releasing their mouse button after moving the T-Bar).
	// Call `ReleaseTBar` manually if you set `release` to false. Defaults to true.
	Release *bool `json:"release,omitempty"`
}

func (c *Client) SetTBarPosition(Position float64, Release *bool) (*SetTBarPositionResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetTBarPositionRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetTBarPosition",
		},
		Position: Position,
		Release:  Release,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetTBarPositionResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetTBarPositionResponse struct {
	resData
}

// Set the current properties of a Text Freetype 2 source.
type SetTextFreetype2PropertiesRequest struct {
	reqData
	// Source name.
	Source string `json:"source"`
	// Gradient top color.
	Color1 *int `json:"color1,omitempty"`
	// Gradient bottom color.
	Color2 *int `json:"color2,omitempty"`
	// Custom width (0 to disable).
	CustomWidth *int `json:"custom_width,omitempty"`
	// Drop shadow.
	DropShadow *bool `json:"drop_shadow,omitempty"`
	// Holds data for the font. Ex: `"font": { "face": "Arial", "flags": 0, "size":
	// 150, "style": "" }`
	Font SetTextFreetype2PropertiesFont `json:"font"`
	// Read text from the specified file.
	FromFile *bool `json:"from_file,omitempty"`
	// Chat log.
	LogMode *bool `json:"log_mode,omitempty"`
	// Outline.
	Outline *bool `json:"outline,omitempty"`
	// Text content to be displayed.
	Text string `json:"text,omitempty"`
	// File path.
	TextFile string `json:"text_file,omitempty"`
	// Word wrap.
	WordWrap *bool `json:"word_wrap,omitempty"`
}

func (c *Client) SetTextFreetype2Properties(Source string, Color1 *int, Color2 *int, CustomWidth *int, DropShadow *bool, Font SetTextFreetype2PropertiesFont, FromFile *bool, LogMode *bool, Outline *bool, Text string, TextFile string, WordWrap *bool) (*SetTextFreetype2PropertiesResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetTextFreetype2PropertiesRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetTextFreetype2Properties",
		},
		Source:      Source,
		Color1:      Color1,
		Color2:      Color2,
		CustomWidth: CustomWidth,
		DropShadow:  DropShadow,
		Font:        Font,
		FromFile:    FromFile,
		LogMode:     LogMode,
		Outline:     Outline,
		Text:        Text,
		TextFile:    TextFile,
		WordWrap:    WordWrap,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetTextFreetype2PropertiesResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetTextFreetype2PropertiesResponse struct {
	resData
}

// Set the current properties of a Text GDI Plus source.
type SetTextGDIPlusPropertiesRequest struct {
	reqData
	// Name of the source.
	Source string `json:"source"`
	// Text Alignment ("left", "center", "right").
	Align string `json:"align,omitempty"`
	// Background color.
	BkColor *int `json:"bk_color,omitempty"`
	// Background opacity (0-100).
	BkOpacity *int `json:"bk_opacity,omitempty"`
	// Chat log.
	Chatlog *bool `json:"chatlog,omitempty"`
	// Chat log lines.
	ChatlogLines *int `json:"chatlog_lines,omitempty"`
	// Text color.
	Color *int `json:"color,omitempty"`
	// Extents wrap.
	Extents *bool `json:"extents,omitempty"`
	// Extents cx.
	ExtentsCx *int `json:"extents_cx,omitempty"`
	// Extents cy.
	ExtentsCy *int `json:"extents_cy,omitempty"`
	// File path name.
	File string `json:"file,omitempty"`
	// Read text from the specified file.
	ReadFromFile *bool `json:"read_from_file,omitempty"`
	// Holds data for the font. Ex: `"font": { "face": "Arial", "flags": 0, "size":
	// 150, "style": "" }`
	Font SetTextGDIPlusPropertiesFont `json:"font"`
	// Gradient enabled.
	Gradient *bool `json:"gradient,omitempty"`
	// Gradient color.
	GradientColor *int `json:"gradient_color,omitempty"`
	// Gradient direction.
	GradientDir *float32 `json:"gradient_dir,omitempty"`
	// Gradient opacity (0-100).
	GradientOpacity *int `json:"gradient_opacity,omitempty"`
	// Outline.
	Outline *bool `json:"outline,omitempty"`
	// Outline color.
	OutlineColor *int `json:"outline_color,omitempty"`
	// Outline size.
	OutlineSize *int `json:"outline_size,omitempty"`
	// Outline opacity (0-100).
	OutlineOpacity *int `json:"outline_opacity,omitempty"`
	// Text content to be displayed.
	Text string `json:"text,omitempty"`
	// Text vertical alignment ("top", "center", "bottom").
	Valign string `json:"valign,omitempty"`
	// Vertical text enabled.
	Vertical *bool `json:"vertical,omitempty"`
	// Visibility of the scene item.
	Render *bool `json:"render,omitempty"`
}

func (c *Client) SetTextGDIPlusProperties(Source string, Align string, BkColor *int, BkOpacity *int, Chatlog *bool, ChatlogLines *int, Color *int, Extents *bool, ExtentsCx *int, ExtentsCy *int, File string, ReadFromFile *bool, Font SetTextGDIPlusPropertiesFont, Gradient *bool, GradientColor *int, GradientDir *float32, GradientOpacity *int, Outline *bool, OutlineColor *int, OutlineSize *int, OutlineOpacity *int, Text string, Valign string, Vertical *bool, Render *bool) (*SetTextGDIPlusPropertiesResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetTextGDIPlusPropertiesRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetTextGDIPlusProperties",
		},
		Source:          Source,
		Align:           Align,
		BkColor:         BkColor,
		BkOpacity:       BkOpacity,
		Chatlog:         Chatlog,
		ChatlogLines:    ChatlogLines,
		Color:           Color,
		Extents:         Extents,
		ExtentsCx:       ExtentsCx,
		ExtentsCy:       ExtentsCy,
		File:            File,
		ReadFromFile:    ReadFromFile,
		Font:            Font,
		Gradient:        Gradient,
		GradientColor:   GradientColor,
		GradientDir:     GradientDir,
		GradientOpacity: GradientOpacity,
		Outline:         Outline,
		OutlineColor:    OutlineColor,
		OutlineSize:     OutlineSize,
		OutlineOpacity:  OutlineOpacity,
		Text:            Text,
		Valign:          Valign,
		Vertical:        Vertical,
		Render:          Render,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetTextGDIPlusPropertiesResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetTextGDIPlusPropertiesResponse struct {
	resData
}

// Set the duration of the currently selected transition if supported.
type SetTransitionDurationRequest struct {
	reqData
	// Desired duration of the transition (in milliseconds).
	Duration int `json:"duration"`
}

func (c *Client) SetTransitionDuration(Duration int) (*SetTransitionDurationResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetTransitionDurationRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetTransitionDuration",
		},
		Duration: Duration,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetTransitionDurationResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetTransitionDurationResponse struct {
	resData
}

// Change the current settings of a transition
type SetTransitionSettingsRequest struct {
	reqData
	// Transition name
	TransitionName string `json:"transitionName"`
	// Transition settings (they can be partial)
	TransitionSettings interface{} `json:"transitionSettings"`
}

func (c *Client) SetTransitionSettings(TransitionName string, TransitionSettings interface{}) (*SetTransitionSettingsResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetTransitionSettingsRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetTransitionSettings",
		},
		TransitionName:     TransitionName,
		TransitionSettings: TransitionSettings,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetTransitionSettingsResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetTransitionSettingsResponse struct {
	resData
	// Updated transition settings
	TransitionSettings interface{} `json:"transitionSettings"`
}

// Set the volume of the specified source. Default request format uses mul, NOT
// SLIDER PERCENTAGE.
type SetVolumeRequest struct {
	reqData
	// Source name.
	Source string `json:"source"`
	// Desired volume. Must be between `0.0` and `20.0` for mul, and under 26.0 for
	// dB. OBS will interpret dB values under -100.0 as Inf. Note: The OBS volume
	// sliders only reach a maximum of 1.0mul/0.0dB, however OBS actually supports
	// larger values.
	Volume float64 `json:"volume"`
	// Interperet `volume` data as decibels instead of amplitude/mul.
	UseDecibel *bool `json:"useDecibel,omitempty"`
}

func (c *Client) SetVolume(Source string, Volume float64, UseDecibel *bool) (*SetVolumeResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SetVolumeRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "SetVolume",
		},
		Source:     Source,
		Volume:     Volume,
		UseDecibel: UseDecibel,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SetVolumeResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SetVolumeResponse struct {
	resData
}

// Waits for the specified duration. Designed to be used in `ExecuteBatch`
// operations.
type SleepRequest struct {
	reqData
	// Delay in milliseconds to wait before continuing.
	SleepMillis int `json:"sleepMillis"`
}

func (c *Client) Sleep(SleepMillis int) (*SleepResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := SleepRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "Sleep",
		},
		SleepMillis: SleepMillis,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &SleepResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type SleepResponse struct {
	resData
}

//   Note: Controlling outputs is an experimental feature of obs-websocket. Some
// plugins which add outputs to OBS may not function properly when they are
// controlled in this way.
type StartOutputRequest struct {
	reqData
	// Output name
	OutputName string `json:"outputName"`
}

func (c *Client) StartOutput(OutputName string) (*StartOutputResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := StartOutputRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "StartOutput",
		},
		OutputName: OutputName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &StartOutputResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type StartOutputResponse struct {
	resData
}

// Start recording. Will return an `error` if recording is already active.
type StartRecordingRequest struct {
	reqData
}

func (c *Client) StartRecording() (*StartRecordingResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := StartRecordingRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "StartRecording",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &StartRecordingResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type StartRecordingResponse struct {
	resData
}

// Start recording into the Replay Buffer. Will return an `error` if the Replay
// Buffer is already active or if the "Save Replay Buffer" hotkey is not set in
// OBS' settings. Setting this hotkey is mandatory, even when triggering saves
// only through obs-websocket.
type StartReplayBufferRequest struct {
	reqData
}

func (c *Client) StartReplayBuffer() (*StartReplayBufferResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := StartReplayBufferRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "StartReplayBuffer",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &StartReplayBufferResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type StartReplayBufferResponse struct {
	resData
}

// Toggle recording on or off (depending on the current recording state).
type StartStopRecordingRequest struct {
	reqData
}

func (c *Client) StartStopRecording() (*StartStopRecordingResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := StartStopRecordingRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "StartStopRecording",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &StartStopRecordingResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type StartStopRecordingResponse struct {
	resData
}

// Toggle the Replay Buffer on/off (depending on the current state of the replay
// buffer).
type StartStopReplayBufferRequest struct {
	reqData
}

func (c *Client) StartStopReplayBuffer() (*StartStopReplayBufferResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := StartStopReplayBufferRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "StartStopReplayBuffer",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &StartStopReplayBufferResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type StartStopReplayBufferResponse struct {
	resData
}

// Toggle streaming on or off (depending on the current stream state).
type StartStopStreamingRequest struct {
	reqData
}

func (c *Client) StartStopStreaming() (*StartStopStreamingResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := StartStopStreamingRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "StartStopStreaming",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &StartStopStreamingResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type StartStopStreamingResponse struct {
	resData
}

// Toggle virtual cam on or off (depending on the current virtual cam state).
type StartStopVirtualCamRequest struct {
	reqData
}

func (c *Client) StartStopVirtualCam() (*StartStopVirtualCamResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := StartStopVirtualCamRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "StartStopVirtualCam",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &StartStopVirtualCamResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type StartStopVirtualCamResponse struct {
	resData
}

// Start streaming. Will return an `error` if streaming is already active.
type StartStreamingRequest struct {
	reqData
	// Special stream configuration. Note: these won't be saved to OBS'
	// configuration.
	Stream StartStreamingStream `json:"stream"`
}

func (c *Client) StartStreaming(Stream StartStreamingStream) (*StartStreamingResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := StartStreamingRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "StartStreaming",
		},
		Stream: Stream,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &StartStreamingResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type StartStreamingResponse struct {
	resData
}

// Start virtual cam. Will return an `error` if virtual cam is already active.
type StartVirtualCamRequest struct {
	reqData
}

func (c *Client) StartVirtualCam() (*StartVirtualCamResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := StartVirtualCamRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "StartVirtualCam",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &StartVirtualCamResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type StartVirtualCamResponse struct {
	resData
}

// Stop a media source. Supports ffmpeg and vlc media sources (as of OBS
// v25.0.8)
type StopMediaRequest struct {
	reqData
	// Source name.
	SourceName string `json:"sourceName"`
}

func (c *Client) StopMedia(SourceName string) (*StopMediaResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := StopMediaRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "StopMedia",
		},
		SourceName: SourceName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &StopMediaResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type StopMediaResponse struct {
	resData
}

//   Note: Controlling outputs is an experimental feature of obs-websocket. Some
// plugins which add outputs to OBS may not function properly when they are
// controlled in this way.
type StopOutputRequest struct {
	reqData
	// Output name
	OutputName string `json:"outputName"`
	// Force stop (default: false)
	Force *bool `json:"force,omitempty"`
}

func (c *Client) StopOutput(OutputName string, Force *bool) (*StopOutputResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := StopOutputRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "StopOutput",
		},
		OutputName: OutputName,
		Force:      Force,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &StopOutputResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type StopOutputResponse struct {
	resData
}

// Stop recording. Will return an `error` if recording is not active.
type StopRecordingRequest struct {
	reqData
}

func (c *Client) StopRecording() (*StopRecordingResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := StopRecordingRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "StopRecording",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &StopRecordingResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type StopRecordingResponse struct {
	resData
}

// Stop recording into the Replay Buffer. Will return an `error` if the Replay
// Buffer is not active.
type StopReplayBufferRequest struct {
	reqData
}

func (c *Client) StopReplayBuffer() (*StopReplayBufferResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := StopReplayBufferRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "StopReplayBuffer",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &StopReplayBufferResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type StopReplayBufferResponse struct {
	resData
}

// Stop streaming. Will return an `error` if streaming is not active.
type StopStreamingRequest struct {
	reqData
}

func (c *Client) StopStreaming() (*StopStreamingResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := StopStreamingRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "StopStreaming",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &StopStreamingResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type StopStreamingResponse struct {
	resData
}

// Stop virtual cam. Will return an `error` if virtual cam is not active.
type StopVirtualCamRequest struct {
	reqData
}

func (c *Client) StopVirtualCam() (*StopVirtualCamResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := StopVirtualCamRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "StopVirtualCam",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &StopVirtualCamResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type StopVirtualCamResponse struct {
	resData
}

//   At least `embedPictureFormat` or `saveToFilePath` must be specified.
// Clients can specify `width` and `height` parameters to receive scaled
// pictures. Aspect ratio is preserved if only one of these two parameters is
// specified.
type TakeSourceScreenshotRequest struct {
	reqData
	// Source name. Note: Since scenes are also sources, you can also provide a
	// scene name. If not provided, the currently active scene is used.
	SourceName string `json:"sourceName,omitempty"`
	// Format of the Data URI encoded picture. Can be "png", "jpg", "jpeg" or "bmp"
	// (or any other value supported by Qt's Image module)
	EmbedPictureFormat string `json:"embedPictureFormat,omitempty"`
	// Full file path (file extension included) where the captured image is to be
	// saved. Can be in a format different from `pictureFormat`. Can be a relative
	// path.
	SaveToFilePath string `json:"saveToFilePath,omitempty"`
	// Format to save the image file as (one of the values provided in the
	// `supported-image-export-formats` response field of `GetVersion`). If not
	// specified, tries to guess based on file extension.
	FileFormat string `json:"fileFormat,omitempty"`
	// Compression ratio between -1 and 100 to write the image with. -1 is
	// automatic, 1 is smallest file/most compression, 100 is largest file/least
	// compression. Varies with image type.
	CompressionQuality *int `json:"compressionQuality,omitempty"`
	// Screenshot width. Defaults to the source's base width.
	Width *int `json:"width,omitempty"`
	// Screenshot height. Defaults to the source's base height.
	Height *int `json:"height,omitempty"`
}

func (c *Client) TakeSourceScreenshot(SourceName string, EmbedPictureFormat string, SaveToFilePath string, FileFormat string, CompressionQuality *int, Width *int, Height *int) (*TakeSourceScreenshotResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := TakeSourceScreenshotRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "TakeSourceScreenshot",
		},
		SourceName:         SourceName,
		EmbedPictureFormat: EmbedPictureFormat,
		SaveToFilePath:     SaveToFilePath,
		FileFormat:         FileFormat,
		CompressionQuality: CompressionQuality,
		Width:              Width,
		Height:             Height,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &TakeSourceScreenshotResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type TakeSourceScreenshotResponse struct {
	resData
	// Source name
	SourceName string `json:"sourceName"`
	// Image Data URI (if `embedPictureFormat` was specified in the request)
	Img string `json:"img"`
	// Absolute path to the saved image file (if `saveToFilePath` was specified in
	// the request)
	ImageFile string `json:"imageFile"`
}

// Inverts the mute status of a specified source.
type ToggleMuteRequest struct {
	reqData
	// Source name.
	Source string `json:"source"`
}

func (c *Client) ToggleMute(Source string) (*ToggleMuteResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := ToggleMuteRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "ToggleMute",
		},
		Source: Source,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &ToggleMuteResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type ToggleMuteResponse struct {
	resData
}

// Toggles Studio Mode (depending on the current state of studio mode).
type ToggleStudioModeRequest struct {
	reqData
}

func (c *Client) ToggleStudioMode() (*ToggleStudioModeResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := ToggleStudioModeRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "ToggleStudioMode",
		},
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &ToggleStudioModeResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type ToggleStudioModeResponse struct {
	resData
}

// Transitions the currently previewed scene to the main output. Will return an
// `error` if Studio Mode is not enabled.
type TransitionToProgramRequest struct {
	reqData
	// Change the active transition before switching scenes. Defaults to the active
	// transition.
	WithTransition TransitionToProgramWithTransition `json:"with-transition"`
}

func (c *Client) TransitionToProgram(WithTransition TransitionToProgramWithTransition) (*TransitionToProgramResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := TransitionToProgramRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "TransitionToProgram",
		},
		WithTransition: WithTransition,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &TransitionToProgramResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type TransitionToProgramResponse struct {
	resData
}

// Executes hotkey routine, identified by hotkey unique name
type TriggerHotkeyByNameRequest struct {
	reqData
	// Unique name of the hotkey, as defined when registering the hotkey (e.g.
	// "ReplayBuffer.Save")
	HotkeyName string `json:"hotkeyName"`
}

func (c *Client) TriggerHotkeyByName(HotkeyName string) (*TriggerHotkeyByNameResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := TriggerHotkeyByNameRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "TriggerHotkeyByName",
		},
		HotkeyName: HotkeyName,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &TriggerHotkeyByNameResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type TriggerHotkeyByNameResponse struct {
	resData
}

// Executes hotkey routine, identified by bound combination of keys. A single
// key combination might trigger multiple hotkey routines depending on user
// settings
type TriggerHotkeyBySequenceRequest struct {
	reqData
	// Main key identifier (e.g. `OBS_KEY_A` for key "A"). Available identifiers
	// [here](https://github.com/obsproject/obs-studio/blob/master/libobs/obs-hotkeys.h)
	KeyId string `json:"keyId"`
	// Optional key modifiers object. False entries can be ommitted
	KeyModifiers TriggerHotkeyBySequenceKeyModifiers `json:"keyModifiers"`
}

func (c *Client) TriggerHotkeyBySequence(KeyId string, KeyModifiers TriggerHotkeyBySequenceKeyModifiers) (*TriggerHotkeyBySequenceResponse, error) {
	uuid := uuid.NewString()
	errch := make(chan error)
	defer close(errch)
	req := TriggerHotkeyBySequenceRequest{
		reqData: reqData{
			MessageId:   uuid,
			RequestType: "TriggerHotkeyBySequence",
		},
		KeyId:        KeyId,
		KeyModifiers: KeyModifiers,
	}

	jdata, err := json.Marshal(&req)
	if err != nil {
		return nil, err
	}
	recvch := c.send(jdata, uuid, errch)
	defer close(recvch)
	select {
	case val := <-recvch:
		res := &TriggerHotkeyBySequenceResponse{}
		err = json.Unmarshal(val, res)
		if err != nil {
			return nil, err
		}
		return res, nil
	case err := <-errch:
		return nil, err
	}
}

type TriggerHotkeyBySequenceResponse struct {
	resData
}

type DeleteSceneItemItem struct {
	// Scene Item name (prefer `id`, including both is acceptable).
	Name string `json:"name"`
	// Scene Item ID.
	Id int `json:"id"`
}

type DuplicateSceneItemItem struct {
	// Scene Item name (prefer `id`, including both is acceptable).
	Name string `json:"name"`
	// Scene Item ID.
	Id int `json:"id"`
}

type ExecuteBatchRequests struct {
	// Request type. Eg. `GetVersion`.
	RequestType string `json:"request-type"`
	// ID of the individual request. Can be any string and not required to be
	// unique. Defaults to empty string if not specified.
	MessageId string `json:"message-id,omitempty"`
}

type GetSceneItemPropertiesItem struct {
	// Scene Item name (if the `item` field is an object)
	Name string `json:"name,omitempty"`
	// Scene Item ID (if the `item` field is an object)
	Id *int `json:"id,omitempty"`
}

type ReorderSceneItemsItems struct {
	// Id of a specific scene item. Unique on a scene by scene basis.
	Id *int `json:"id,omitempty"`
	// Name of a scene item. Sufficiently unique if no scene items share sources
	// within the scene.
	Name string `json:"name,omitempty"`
}

type ResetSceneItemItem struct {
	// Scene Item name (if the `item` field is an object)
	Name string `json:"name,omitempty"`
	// Scene Item ID (if the `item` field is an object)
	Id *int `json:"id,omitempty"`
}

type SetSceneItemPropertiesItem struct {
	// Scene Item name (if the `item` field is an object)
	Name string `json:"name,omitempty"`
	// Scene Item ID (if the `item` field is an object)
	Id *int `json:"id,omitempty"`
}

type SetSceneItemPropertiesPosition struct {
	// The new x position of the source.
	X *float64 `json:"x,omitempty"`
	// The new y position of the source.
	Y *float64 `json:"y,omitempty"`
	// The new alignment of the source.
	Alignment *int `json:"alignment,omitempty"`
}

type SetSceneItemPropertiesScale struct {
	// The new x scale of the item.
	X *float64 `json:"x,omitempty"`
	// The new y scale of the item.
	Y *float64 `json:"y,omitempty"`
	// The new scale filter of the source. Can be "OBS_SCALE_DISABLE",
	// "OBS_SCALE_POINT", "OBS_SCALE_BICUBIC", "OBS_SCALE_BILINEAR",
	// "OBS_SCALE_LANCZOS" or "OBS_SCALE_AREA".
	Filter string `json:"filter,omitempty"`
}

type SetSceneItemPropertiesCrop struct {
	// The new amount of pixels cropped off the top of the source before scaling.
	Top *int `json:"top,omitempty"`
	// The new amount of pixels cropped off the bottom of the source before scaling.
	Bottom *int `json:"bottom,omitempty"`
	// The new amount of pixels cropped off the left of the source before scaling.
	Left *int `json:"left,omitempty"`
	// The new amount of pixels cropped off the right of the source before scaling.
	Right *int `json:"right,omitempty"`
}

type SetSceneItemPropertiesBounds struct {
	// The new bounds type of the source. Can be "OBS_BOUNDS_STRETCH",
	// "OBS_BOUNDS_SCALE_INNER", "OBS_BOUNDS_SCALE_OUTER",
	// "OBS_BOUNDS_SCALE_TO_WIDTH", "OBS_BOUNDS_SCALE_TO_HEIGHT",
	// "OBS_BOUNDS_MAX_ONLY" or "OBS_BOUNDS_NONE".
	Type string `json:"type,omitempty"`
	// The new alignment of the bounding box. (0-2, 4-6, 8-10)
	Alignment *int `json:"alignment,omitempty"`
	// The new width of the bounding box.
	X *float64 `json:"x,omitempty"`
	// The new height of the bounding box.
	Y *float64 `json:"y,omitempty"`
}

type SetStreamSettingsSettings struct {
	// The publish URL.
	Server string `json:"server,omitempty"`
	// The publish key.
	Key string `json:"key,omitempty"`
	// Indicates whether authentication should be used when connecting to the
	// streaming server.
	UseAuth *bool `json:"use_auth,omitempty"`
	// The username for the streaming service.
	Username string `json:"username,omitempty"`
	// The password for the streaming service.
	Password string `json:"password,omitempty"`
}

type SetTextFreetype2PropertiesFont struct {
	// Font face.
	Face string `json:"face,omitempty"`
	// Font text styling flag. `Bold=1, Italic=2, Bold Italic=3, Underline=5,
	// Strikeout=8`
	Flags *int `json:"flags,omitempty"`
	// Font text size.
	Size *int `json:"size,omitempty"`
	// Font Style (unknown function).
	Style string `json:"style,omitempty"`
}

type SetTextGDIPlusPropertiesFont struct {
	// Font face.
	Face string `json:"face,omitempty"`
	// Font text styling flag. `Bold=1, Italic=2, Bold Italic=3, Underline=5,
	// Strikeout=8`
	Flags *int `json:"flags,omitempty"`
	// Font text size.
	Size *int `json:"size,omitempty"`
	// Font Style (unknown function).
	Style string `json:"style,omitempty"`
}

type StartStreamingStream struct {
	// If specified ensures the type of stream matches the given type (usually
	// 'rtmp_custom' or 'rtmp_common'). If the currently configured stream type does
	// not match the given stream type, all settings must be specified in the
	// `settings` object or an error will occur when starting the stream.
	Type string `json:"type,omitempty"`
	// Adds the given object parameters as encoded query string parameters to the
	// 'key' of the RTMP stream. Used to pass data to the RTMP service about the
	// streaming. May be any String, Numeric, or Boolean field.
	Metadata interface{} `json:"metadata,omitempty"`
	// Settings for the stream.
	Settings interface{} `json:"settings,omitempty"`
	// The publish URL.
	Server string `json:"server,omitempty"`
	// The publish key of the stream.
	Key string `json:"key,omitempty"`
	// Indicates whether authentication should be used when connecting to the
	// streaming server.
	UseAuth *bool `json:"use_auth,omitempty"`
	// If authentication is enabled, the username for the streaming server. Ignored
	// if `use_auth` is not set to `true`.
	Username string `json:"username,omitempty"`
	// If authentication is enabled, the password for the streaming server. Ignored
	// if `use_auth` is not set to `true`.
	Password string `json:"password,omitempty"`
}

type TransitionToProgramWithTransition struct {
	// Name of the transition.
	Name string `json:"name"`
	// Transition duration (in milliseconds).
	Duration *int `json:"duration,omitempty"`
}

type TriggerHotkeyBySequenceKeyModifiers struct {
	// Trigger Shift Key
	Shift bool `json:"shift"`
	// Trigger Alt Key
	Alt bool `json:"alt"`
	// Trigger Control (Ctrl) Key
	Control bool `json:"control"`
	// Trigger Command Key (Mac)
	Command bool `json:"command"`
}
