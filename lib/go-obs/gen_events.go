package go_obs

import "encoding/json"

// A custom broadcast message, sent by the server, requested by one of the
// websocket clients.
type BroadcastCustomMessageEvent struct {
	eventData
	// Identifier provided by the sender
	Realm string `json:"realm"`
	// User-defined data
	Data interface{} `json:"data"`
}

// OBS is exiting.
type ExitingEvent struct {
	eventData
}

// Emitted every 2 seconds after enabling it by calling SetHeartbeat.
type HeartbeatEvent struct {
	eventData
	// Toggles between every JSON message as an "I am alive" indicator.
	Pulse bool `json:"pulse"`
	// Current active profile.
	CurrentProfile string `json:"current-profile,omitempty"`
	// Current active scene.
	CurrentScene string `json:"current-scene,omitempty"`
	// Current streaming state.
	Streaming *bool `json:"streaming,omitempty"`
	// Total time (in seconds) since the stream started.
	TotalStreamTime *int `json:"total-stream-time,omitempty"`
	// Total bytes sent since the stream started.
	TotalStreamBytes *int `json:"total-stream-bytes,omitempty"`
	// Total frames streamed since the stream started.
	TotalStreamFrames *int `json:"total-stream-frames,omitempty"`
	// Current recording state.
	Recording *bool `json:"recording,omitempty"`
	// Total time (in seconds) since recording started.
	TotalRecordTime *int `json:"total-record-time,omitempty"`
	// Total bytes recorded since the recording started.
	TotalRecordBytes *int `json:"total-record-bytes,omitempty"`
	// Total frames recorded since the recording started.
	TotalRecordFrames *int `json:"total-record-frames,omitempty"`
	// OBS Stats
	Stats OBSStats `json:"stats"`
}

//   Note: These events are emitted by the OBS sources themselves. For example
// when the media file ends. The behavior depends on the type of media source
// being used.
type MediaEndedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// The ID type of the source (Eg. `vlc_source` or `ffmpeg_source`)
	SourceKind string `json:"sourceKind"`
}

//   Note: This event is only emitted when something actively controls the
// media/VLC source. In other words, the source will never emit this on its own
// naturally.
type MediaNextEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// The ID type of the source (Eg. `vlc_source` or `ffmpeg_source`)
	SourceKind string `json:"sourceKind"`
}

//   Note: This event is only emitted when something actively controls the
// media/VLC source. In other words, the source will never emit this on its own
// naturally.
type MediaPausedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// The ID type of the source (Eg. `vlc_source` or `ffmpeg_source`)
	SourceKind string `json:"sourceKind"`
}

//   Note: This event is only emitted when something actively controls the
// media/VLC source. In other words, the source will never emit this on its own
// naturally.
type MediaPlayingEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// The ID type of the source (Eg. `vlc_source` or `ffmpeg_source`)
	SourceKind string `json:"sourceKind"`
}

//   Note: This event is only emitted when something actively controls the
// media/VLC source. In other words, the source will never emit this on its own
// naturally.
type MediaPreviousEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// The ID type of the source (Eg. `vlc_source` or `ffmpeg_source`)
	SourceKind string `json:"sourceKind"`
}

//   Note: This event is only emitted when something actively controls the
// media/VLC source. In other words, the source will never emit this on its own
// naturally.
type MediaRestartedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// The ID type of the source (Eg. `vlc_source` or `ffmpeg_source`)
	SourceKind string `json:"sourceKind"`
}

//   Note: These events are emitted by the OBS sources themselves. For example
// when the media file starts playing. The behavior depends on the type of media
// source being used.
type MediaStartedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// The ID type of the source (Eg. `vlc_source` or `ffmpeg_source`)
	SourceKind string `json:"sourceKind"`
}

//   Note: This event is only emitted when something actively controls the
// media/VLC source. In other words, the source will never emit this on its own
// naturally.
type MediaStoppedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// The ID type of the source (Eg. `vlc_source` or `ffmpeg_source`)
	SourceKind string `json:"sourceKind"`
}

// The selected preview scene has changed (only available in Studio Mode).
type PreviewSceneChangedEvent struct {
	eventData
	// Name of the scene being previewed.
	SceneName string `json:"scene-name"`
	// List of sources composing the scene. Same specification as
	// [`GetCurrentScene`](#getcurrentscene).
	Sources []SceneItem `json:"sources"`
}

// Triggered when switching to another profile or when renaming the current
// profile.
type ProfileChangedEvent struct {
	eventData
	// Name of the new current profile.
	Profile string `json:"profile"`
}

// Triggered when a profile is created, added, renamed, or removed.
type ProfileListChangedEvent struct {
	eventData
	// Profiles list.
	Profiles []struct {
		// Profile name.
		Name string `json:"name"`
	} `json:"profiles"`
}

// Current recording paused
type RecordingPausedEvent struct {
	eventData
}

// Current recording resumed
type RecordingResumedEvent struct {
	eventData
}

// Recording started successfully.
type RecordingStartedEvent struct {
	eventData
	// Absolute path to the file of the current recording.
	RecordingFilename string `json:"recordingFilename"`
}

//   Note: `recordingFilename` is not provided in this event because this
// information is not available at the time this event is emitted.
type RecordingStartingEvent struct {
	eventData
}

// Recording stopped successfully.
type RecordingStoppedEvent struct {
	eventData
	// Absolute path to the file of the current recording.
	RecordingFilename string `json:"recordingFilename"`
}

// A request to stop recording has been issued.
type RecordingStoppingEvent struct {
	eventData
	// Absolute path to the file of the current recording.
	RecordingFilename string `json:"recordingFilename"`
}

// Replay Buffer started successfully
type ReplayStartedEvent struct {
	eventData
}

// A request to start the replay buffer has been issued.
type ReplayStartingEvent struct {
	eventData
}

// Replay Buffer stopped successfully
type ReplayStoppedEvent struct {
	eventData
}

// A request to stop the replay buffer has been issued.
type ReplayStoppingEvent struct {
	eventData
}

// Triggered when switching to another scene collection or when renaming the
// current scene collection.
type SceneCollectionChangedEvent struct {
	eventData
	// Name of the new current scene collection.
	SceneCollection string `json:"sceneCollection"`
}

// Triggered when a scene collection is created, added, renamed, or removed.
type SceneCollectionListChangedEvent struct {
	eventData
	// Scene collections list.
	SceneCollections []struct {
		// Scene collection name.
		Name string `json:"name"`
	} `json:"sceneCollections"`
}

// A scene item has been added to a scene.
type SceneItemAddedEvent struct {
	eventData
	// Name of the scene.
	SceneName string `json:"scene-name"`
	// Name of the item added to the scene.
	ItemName string `json:"item-name"`
	// Scene item ID
	ItemId int `json:"item-id"`
}

// A scene item is deselected.
type SceneItemDeselectedEvent struct {
	eventData
	// Name of the scene.
	SceneName string `json:"scene-name"`
	// Name of the item in the scene.
	ItemName string `json:"item-name"`
	// Name of the item in the scene.
	ItemId int `json:"item-id"`
}

// A scene item's locked status has been toggled.
type SceneItemLockChangedEvent struct {
	eventData
	// Name of the scene.
	SceneName string `json:"scene-name"`
	// Name of the item in the scene.
	ItemName string `json:"item-name"`
	// Scene item ID
	ItemId int `json:"item-id"`
	// New locked state of the item.
	ItemLocked bool `json:"item-locked"`
}

// A scene item has been removed from a scene.
type SceneItemRemovedEvent struct {
	eventData
	// Name of the scene.
	SceneName string `json:"scene-name"`
	// Name of the item removed from the scene.
	ItemName string `json:"item-name"`
	// Scene item ID
	ItemId int `json:"item-id"`
}

// A scene item is selected.
type SceneItemSelectedEvent struct {
	eventData
	// Name of the scene.
	SceneName string `json:"scene-name"`
	// Name of the item in the scene.
	ItemName string `json:"item-name"`
	// Name of the item in the scene.
	ItemId int `json:"item-id"`
}

// A scene item's transform has been changed.
type SceneItemTransformChangedEvent struct {
	eventData
	// Name of the scene.
	SceneName string `json:"scene-name"`
	// Name of the item in the scene.
	ItemName string `json:"item-name"`
	// Scene item ID
	ItemId int `json:"item-id"`
	// Scene item transform properties
	Transform SceneItemTransform `json:"transform"`
}

// A scene item's visibility has been toggled.
type SceneItemVisibilityChangedEvent struct {
	eventData
	// Name of the scene.
	SceneName string `json:"scene-name"`
	// Name of the item in the scene.
	ItemName string `json:"item-name"`
	// Scene item ID
	ItemId int `json:"item-id"`
	// New visibility state of the item.
	ItemVisible bool `json:"item-visible"`
}

//   Note: This event is not fired when the scenes are reordered.
type ScenesChangedEvent struct {
	eventData
	// Scenes list.
	Scenes []Scene `json:"scenes"`
}

// A source has added audio.
type SourceAudioActivatedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
}

// A source has removed audio.
type SourceAudioDeactivatedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
}

// Audio mixer routing changed on a source.
type SourceAudioMixersChangedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// Routing status of the source for each audio mixer (array of 6 values)
	Mixers []struct {
		// Mixer number
		Id int `json:"id"`
		// Routing status
		Enabled bool `json:"enabled"`
	} `json:"mixers"`
	// Raw mixer flags (little-endian, one bit per mixer) as an hexadecimal value
	HexMixersValue string `json:"hexMixersValue"`
}

// The audio sync offset of a source has changed.
type SourceAudioSyncOffsetChangedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// Audio sync offset of the source (in nanoseconds)
	SyncOffset int `json:"syncOffset"`
}

// A source has been created. A source can be an input, a scene or a transition.
type SourceCreatedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// Source type. Can be "input", "scene", "transition" or "filter".
	SourceType string `json:"sourceType"`
	// Source kind.
	SourceKind string `json:"sourceKind"`
	// Source settings
	SourceSettings interface{} `json:"sourceSettings"`
}

// A source has been destroyed/removed. A source can be an input, a scene or a
// transition.
type SourceDestroyedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// Source type. Can be "input", "scene", "transition" or "filter".
	SourceType string `json:"sourceType"`
	// Source kind.
	SourceKind string `json:"sourceKind"`
}

// A filter was added to a source.
type SourceFilterAddedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// Filter name
	FilterName string `json:"filterName"`
	// Filter type
	FilterType string `json:"filterType"`
	// Filter settings
	FilterSettings interface{} `json:"filterSettings"`
}

// A filter was removed from a source.
type SourceFilterRemovedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// Filter name
	FilterName string `json:"filterName"`
	// Filter type
	FilterType string `json:"filterType"`
}

// The visibility/enabled state of a filter changed
type SourceFilterVisibilityChangedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// Filter name
	FilterName string `json:"filterName"`
	// New filter state
	FilterEnabled bool `json:"filterEnabled"`
}

// Filters in a source have been reordered.
type SourceFiltersReorderedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// Ordered Filters list
	Filters []struct {
		// Filter name
		Name string `json:"name"`
		// Filter type
		Type string `json:"type"`
		// Filter visibility status
		Enabled bool `json:"enabled"`
	} `json:"filters"`
}

// A source has been muted or unmuted.
type SourceMuteStateChangedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// Mute status of the source
	Muted bool `json:"muted"`
}

// Scene items within a scene have been reordered.
type SourceOrderChangedEvent struct {
	eventData
	// Name of the scene where items have been reordered.
	SceneName string `json:"scene-name"`
	// Ordered list of scene items
	SceneItems []struct {
		// Item source name
		SourceName string `json:"source-name"`
		// Scene item unique ID
		ItemId int `json:"item-id"`
	} `json:"scene-items"`
}

// A source has been renamed.
type SourceRenamedEvent struct {
	eventData
	// Previous source name
	PreviousName string `json:"previousName"`
	// New source name
	NewName string `json:"newName"`
	// Type of source (input, scene, filter, transition)
	SourceType string `json:"sourceType"`
}

// The volume of a source has changed.
type SourceVolumeChangedEvent struct {
	eventData
	// Source name
	SourceName string `json:"sourceName"`
	// Source volume
	Volume float32 `json:"volume"`
	// Source volume in Decibel
	VolumeDb float32 `json:"volumeDb"`
}

// Streaming started successfully.
type StreamStartedEvent struct {
	eventData
}

// A request to start streaming has been issued.
type StreamStartingEvent struct {
	eventData
	// Always false (retrocompatibility).
	PreviewOnly bool `json:"preview-only"`
}

// Emitted every 2 seconds when stream is active.
type StreamStatusEvent struct {
	eventData
	// Current streaming state.
	Streaming bool `json:"streaming"`
	// Current recording state.
	Recording bool `json:"recording"`
	// Replay Buffer status
	ReplayBufferActive bool `json:"replay-buffer-active"`
	// Amount of data per second (in bytes) transmitted by the stream encoder.
	BytesPerSec int `json:"bytes-per-sec"`
	// Amount of data per second (in kilobits) transmitted by the stream encoder.
	KbitsPerSec int `json:"kbits-per-sec"`
	// Percentage of dropped frames.
	Strain float64 `json:"strain"`
	// Total time (in seconds) since the stream started.
	TotalStreamTime int `json:"total-stream-time"`
	// Total number of frames transmitted since the stream started.
	NumTotalFrames int `json:"num-total-frames"`
	// Number of frames dropped by the encoder since the stream started.
	NumDroppedFrames int `json:"num-dropped-frames"`
	// Current framerate.
	Fps float64 `json:"fps"`
	// Number of frames rendered
	RenderTotalFrames int `json:"render-total-frames"`
	// Number of frames missed due to rendering lag
	RenderMissedFrames int `json:"render-missed-frames"`
	// Number of frames outputted
	OutputTotalFrames int `json:"output-total-frames"`
	// Number of frames skipped due to encoding lag
	OutputSkippedFrames int `json:"output-skipped-frames"`
	// Average frame time (in milliseconds)
	AverageFrameTime float64 `json:"average-frame-time"`
	// Current CPU usage (percentage)
	CpuUsage float64 `json:"cpu-usage"`
	// Current RAM usage (in megabytes)
	MemoryUsage float64 `json:"memory-usage"`
	// Free recording disk space (in megabytes)
	FreeDiskSpace float64 `json:"free-disk-space"`
	// Always false (retrocompatibility).
	PreviewOnly bool `json:"preview-only"`
}

// Streaming stopped successfully.
type StreamStoppedEvent struct {
	eventData
}

// A request to stop streaming has been issued.
type StreamStoppingEvent struct {
	eventData
	// Always false (retrocompatibility).
	PreviewOnly bool `json:"preview-only"`
}

// Studio Mode has been enabled or disabled.
type StudioModeSwitchedEvent struct {
	eventData
	// The new enabled state of Studio Mode.
	NewState bool `json:"new-state"`
}

// Indicates a scene change.
type SwitchScenesEvent struct {
	eventData
	// The new scene.
	SceneName string `json:"scene-name"`
	// List of scene items in the new scene. Same specification as
	// [`GetCurrentScene`](#getcurrentscene).
	Sources []SceneItem `json:"sources"`
}

// The active transition has been changed.
type SwitchTransitionEvent struct {
	eventData
	// The name of the new active transition.
	TransitionName string `json:"transition-name"`
}

// A transition (other than "cut") has begun.
type TransitionBeginEvent struct {
	eventData
	// Transition name.
	Name string `json:"name"`
	// Transition type.
	Type string `json:"type"`
	// Transition duration (in milliseconds). Will be -1 for any transition with a
	// fixed duration, such as a Stinger, due to limitations of the OBS API.
	Duration int `json:"duration"`
	// Source scene of the transition
	FromScene string `json:"from-scene,omitempty"`
	// Destination scene of the transition
	ToScene string `json:"to-scene"`
}

// The active transition duration has been changed.
type TransitionDurationChangedEvent struct {
	eventData
	// New transition duration.
	NewDuration int `json:"new-duration"`
}

// A transition (other than "cut") has ended. Note: The `from-scene` field is
// not available in TransitionEnd.
type TransitionEndEvent struct {
	eventData
	// Transition name.
	Name string `json:"name"`
	// Transition type.
	Type string `json:"type"`
	// Transition duration (in milliseconds).
	Duration int `json:"duration"`
	// Destination scene of the transition
	ToScene string `json:"to-scene"`
}

// The list of available transitions has been modified. Transitions have been
// added, removed, or renamed.
type TransitionListChangedEvent struct {
	eventData
	// Transitions list.
	Transitions []struct {
		// Transition name.
		Name string `json:"name"`
	} `json:"transitions"`
}

// A stinger transition has finished playing its video.
type TransitionVideoEndEvent struct {
	eventData
	// Transition name.
	Name string `json:"name"`
	// Transition type.
	Type string `json:"type"`
	// Transition duration (in milliseconds).
	Duration int `json:"duration"`
	// Source scene of the transition
	FromScene string `json:"from-scene,omitempty"`
	// Destination scene of the transition
	ToScene string `json:"to-scene"`
}

// Virtual cam started successfully.
type VirtualCamStartedEvent struct {
	eventData
}

// Virtual cam stopped successfully.
type VirtualCamStoppedEvent struct {
	eventData
}

var eventConverters = map[string]func([]byte) any{
	"BroadcastCustomMessage": func(data []byte) any {
		evt := &BroadcastCustomMessageEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"Exiting": func(data []byte) any {
		evt := &ExitingEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"Heartbeat": func(data []byte) any {
		evt := &HeartbeatEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"MediaEnded": func(data []byte) any {
		evt := &MediaEndedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"MediaNext": func(data []byte) any {
		evt := &MediaNextEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"MediaPaused": func(data []byte) any {
		evt := &MediaPausedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"MediaPlaying": func(data []byte) any {
		evt := &MediaPlayingEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"MediaPrevious": func(data []byte) any {
		evt := &MediaPreviousEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"MediaRestarted": func(data []byte) any {
		evt := &MediaRestartedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"MediaStarted": func(data []byte) any {
		evt := &MediaStartedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"MediaStopped": func(data []byte) any {
		evt := &MediaStoppedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"PreviewSceneChanged": func(data []byte) any {
		evt := &PreviewSceneChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"ProfileChanged": func(data []byte) any {
		evt := &ProfileChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"ProfileListChanged": func(data []byte) any {
		evt := &ProfileListChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"RecordingPaused": func(data []byte) any {
		evt := &RecordingPausedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"RecordingResumed": func(data []byte) any {
		evt := &RecordingResumedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"RecordingStarted": func(data []byte) any {
		evt := &RecordingStartedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"RecordingStarting": func(data []byte) any {
		evt := &RecordingStartingEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"RecordingStopped": func(data []byte) any {
		evt := &RecordingStoppedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"RecordingStopping": func(data []byte) any {
		evt := &RecordingStoppingEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"ReplayStarted": func(data []byte) any {
		evt := &ReplayStartedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"ReplayStarting": func(data []byte) any {
		evt := &ReplayStartingEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"ReplayStopped": func(data []byte) any {
		evt := &ReplayStoppedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"ReplayStopping": func(data []byte) any {
		evt := &ReplayStoppingEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SceneCollectionChanged": func(data []byte) any {
		evt := &SceneCollectionChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SceneCollectionListChanged": func(data []byte) any {
		evt := &SceneCollectionListChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SceneItemAdded": func(data []byte) any {
		evt := &SceneItemAddedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SceneItemDeselected": func(data []byte) any {
		evt := &SceneItemDeselectedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SceneItemLockChanged": func(data []byte) any {
		evt := &SceneItemLockChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SceneItemRemoved": func(data []byte) any {
		evt := &SceneItemRemovedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SceneItemSelected": func(data []byte) any {
		evt := &SceneItemSelectedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SceneItemTransformChanged": func(data []byte) any {
		evt := &SceneItemTransformChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SceneItemVisibilityChanged": func(data []byte) any {
		evt := &SceneItemVisibilityChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"ScenesChanged": func(data []byte) any {
		evt := &ScenesChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SourceAudioActivated": func(data []byte) any {
		evt := &SourceAudioActivatedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SourceAudioDeactivated": func(data []byte) any {
		evt := &SourceAudioDeactivatedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SourceAudioMixersChanged": func(data []byte) any {
		evt := &SourceAudioMixersChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SourceAudioSyncOffsetChanged": func(data []byte) any {
		evt := &SourceAudioSyncOffsetChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SourceCreated": func(data []byte) any {
		evt := &SourceCreatedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SourceDestroyed": func(data []byte) any {
		evt := &SourceDestroyedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SourceFilterAdded": func(data []byte) any {
		evt := &SourceFilterAddedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SourceFilterRemoved": func(data []byte) any {
		evt := &SourceFilterRemovedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SourceFilterVisibilityChanged": func(data []byte) any {
		evt := &SourceFilterVisibilityChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SourceFiltersReordered": func(data []byte) any {
		evt := &SourceFiltersReorderedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SourceMuteStateChanged": func(data []byte) any {
		evt := &SourceMuteStateChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SourceOrderChanged": func(data []byte) any {
		evt := &SourceOrderChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SourceRenamed": func(data []byte) any {
		evt := &SourceRenamedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SourceVolumeChanged": func(data []byte) any {
		evt := &SourceVolumeChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"StreamStarted": func(data []byte) any {
		evt := &StreamStartedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"StreamStarting": func(data []byte) any {
		evt := &StreamStartingEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"StreamStatus": func(data []byte) any {
		evt := &StreamStatusEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"StreamStopped": func(data []byte) any {
		evt := &StreamStoppedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"StreamStopping": func(data []byte) any {
		evt := &StreamStoppingEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"StudioModeSwitched": func(data []byte) any {
		evt := &StudioModeSwitchedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SwitchScenes": func(data []byte) any {
		evt := &SwitchScenesEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"SwitchTransition": func(data []byte) any {
		evt := &SwitchTransitionEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"TransitionBegin": func(data []byte) any {
		evt := &TransitionBeginEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"TransitionDurationChanged": func(data []byte) any {
		evt := &TransitionDurationChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"TransitionEnd": func(data []byte) any {
		evt := &TransitionEndEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"TransitionListChanged": func(data []byte) any {
		evt := &TransitionListChangedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"TransitionVideoEnd": func(data []byte) any {
		evt := &TransitionVideoEndEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"VirtualCamStarted": func(data []byte) any {
		evt := &VirtualCamStartedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
	"VirtualCamStopped": func(data []byte) any {
		evt := &VirtualCamStoppedEvent{}
		err := json.Unmarshal(data, evt)
		if err != nil {
			return nil
		}
		return evt
	},
}
