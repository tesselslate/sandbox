package go_obs

// An OBS Scene Item.
type SceneItem struct {
	Cy float64
	Cx float64
	// The point on the source that the item is manipulated from. The sum of 1=Left
	// or 2=Right, and 4=Top or 8=Bottom, or omit to center on that axis.
	Alignment float64
	// The name of this Scene Item.
	Name string
	// Scene item ID
	Id int
	// Whether or not this Scene Item is set to "visible".
	Render bool
	// Whether or not this Scene Item is muted.
	Muted bool
	// Whether or not this Scene Item is locked and can't be moved around
	Locked   bool
	SourceCx float64
	SourceCy float64
	// Source type. Value is one of the following: "input", "filter", "transition",
	// "scene" or "unknown"
	Type   string
	Volume float64
	X      float64
	Y      float64
	// Name of the item's parent (if this item belongs to a group)
	ParentGroupName string
	// List of children (if this item is a group)
	GroupChildren []SceneItem
}

type SceneItemTransform struct {
	// The x position of the scene item from the left.
	Position struct {
		// The x position of the scene item from the left.
		X float64 `json:"x"`
		// The y position of the scene item from the top.
		Y float64 `json:"y"`
		// The point on the scene item that the item is manipulated from.
		Alignment int `json:"alignment"`
	}
	// The clockwise rotation of the scene item in degrees around the point of
	// alignment.
	Rotation float64
	// The x-scale factor of the scene item.
	Scale struct {
		// The x-scale factor of the scene item.
		X float64 `json:"x"`
		// The y-scale factor of the scene item.
		Y float64 `json:"y"`
		// The scale filter of the source. Can be "OBS_SCALE_DISABLE",
		// "OBS_SCALE_POINT", "OBS_SCALE_BICUBIC", "OBS_SCALE_BILINEAR",
		// "OBS_SCALE_LANCZOS" or "OBS_SCALE_AREA".
		Filter string `json:"filter"`
	}
	// The number of pixels cropped off the top of the scene item before scaling.
	Crop struct {
		// The number of pixels cropped off the top of the scene item before scaling.
		Top int `json:"top"`
		// The number of pixels cropped off the right of the scene item before scaling.
		Right int `json:"right"`
		// The number of pixels cropped off the bottom of the scene item before scaling.
		Bottom int `json:"bottom"`
		// The number of pixels cropped off the left of the scene item before scaling.
		Left int `json:"left"`
	}
	// If the scene item is visible.
	Visible bool
	// If the scene item is locked in position.
	Locked bool
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
	}
	// Base width (without scaling) of the source
	SourceWidth int
	// Base source (without scaling) of the source
	SourceHeight int
	// Scene item width (base source width multiplied by the horizontal scaling
	// factor)
	Width float64
	// Scene item height (base source height multiplied by the vertical scaling
	// factor)
	Height float64
	// Name of the item's parent (if this item belongs to a group)
	ParentGroupName string
	// List of children (if this item is a group)
	GroupChildren []SceneItemTransform
}

type OBSStats struct {
	// Current framerate.
	Fps float64
	// Number of frames rendered
	RenderTotalFrames int
	// Number of frames missed due to rendering lag
	RenderMissedFrames int
	// Number of frames outputted
	OutputTotalFrames int
	// Number of frames skipped due to encoding lag
	OutputSkippedFrames int
	// Average frame render time (in milliseconds)
	AverageFrameTime float64
	// Current CPU usage (percentage)
	CpuUsage float64
	// Current RAM usage (in megabytes)
	MemoryUsage float64
	// Free recording disk space (in megabytes)
	FreeDiskSpace float64
}

type Output struct {
	// Output name
	Name string
	// Output type/kind
	Type string
	// Video output width
	Width int
	// Video output height
	Height int
	// Output flags
	Flags struct {
		// Raw flags value
		RawValue int `json:"rawValue"`
		// Output uses audio
		Audio bool `json:"audio"`
		// Output uses video
		Video bool `json:"video"`
		// Output is encoded
		Encoded bool `json:"encoded"`
		// Output uses several audio tracks
		MultiTrack bool `json:"multiTrack"`
		// Output uses a service
		Service bool `json:"service"`
	}
	// Output settings
	Settings interface{}
	// Output status (active or not)
	Active bool
	// Output reconnection status (reconnecting or not)
	Reconnecting bool
	// Output congestion
	Congestion float64
	// Number of frames sent
	TotalFrames int
	// Number of frames dropped
	DroppedFrames int
	// Total bytes sent
	TotalBytes int
}

type ScenesCollection struct {
	// Name of the scene collection
	ScName string
}

type Scene struct {
	// Name of the currently active scene.
	Name string
	// Ordered list of the current scene's source items.
	Sources []SceneItem
}
