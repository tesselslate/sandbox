-- User imports
local move      = require("move")

--[[
--
--   Module
--
--]]

local M = {}

--- Scans a field of crops, executing the specified callback above each crop.
-- The callback will be invoked with the current position of the robot.
-- @param pos The coordinates of the northwest corner of the field
-- @param size The size of the field
-- @param cb The callback for each crop
M.field = function(pos, size, cb)
    size = size - 1

    for x = 0, size do
        -- Scan the field in a sensible order (north for one row, south for the
        -- next, ...) so that the robot does not do twice as many movements as
        -- needed.
        local start = (x % 2 == 1) and size or 0
        local step  = (x % 2 == 1) and -1   or 1
        local stop  = (x % 2 == 1) and 0    or size

        for z = start, stop, step do
            local slot = {pos[1] + x, pos[2] + z}
            move.to(slot)
            cb(slot)
        end
    end
end

return M
