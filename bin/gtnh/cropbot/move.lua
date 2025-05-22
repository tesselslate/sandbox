-- System imports
local component = require("component")
local sides     = require("sides")

local robot     = component.robot

-- User imports
local util      = require("util")

-- State
local pos    = {0, 0}  -- current position (relative to station)
local facing = {0, -1} -- current facing   ({dx, dz} for 1 forward step)

local M = {}

--[[
--
--   Internal
--
--]]

--- Moves in one direction for a set number of blocks.
-- If any obstructions (blocks or entities) are encountered, the robot will wait
-- and attempt to move again shortly after. If an impossible move is attempted,
-- an error will be thrown.
--
-- Does not update the internal position of the robot.
-- @param side  The direction to move in
-- @param count The number of blocks to move
-- @raise impossible move
local step = function(side, count)
    for _ = 1, count do
        local ok, err

        while not ok do
            ok, err = robot.move(side)
            if err == "impossible move" then
                error(err)
            end
        end
    end
end

--- Moves a set number of blocks on one axis.
-- The robot must be facing the specified axis.
-- @param axis The axis to move on (X=1, Z=2)
-- @param count The number of blocks to move
local half_move = function(axis, count)
    local side = util.sign(count) == util.sign(facing[axis]) and sides.front or sides.back
    step(side, count * util.sign(count))
end

--[[
--
--   Module
--
--]]

--- Returns the current facing of the robot.
-- The facing is represented as a difference in position from one forward step.
-- @return {x, z}
M.get_facing = function()
    return {facing[1], facing[2]}
end

--- Returns the current position of the robot.
-- @return {x, z}
M.get_pos = function()
    return {pos[1], pos[2]}
end

--- Turns the robot clockwise and updates its internal facing.
M.turn = function()
    robot.turn(true)

    -- ( 0, -1) -> ( 1,  0)
    -- ( 1,  0) -> ( 0,  1)
    -- ( 0,  1) -> ( -1, 0)
    -- (-1,  0) -> ( 0, -1)

    local xf = facing[1]
    local zf = facing[2]
    facing[1] = -zf
    facing[2] = xf
end

--- Attempts to move the robot to the given location relative to its origin.
-- @param dst The destination {x, z} location to move to
-- @raise impossible move
M.to = function(dst)
    local dx = dst[1] - pos[1]
    local dz = dst[2] - pos[2]

    local fx = facing[1] ~= 0
    local fz = facing[2] ~= 0

    -- If the robot is facing +X or -X, move on the X axis first; otherwise,
    -- move on the Z axis first.
    if fx then
        half_move(1, dx)
        if dz ~= 0 then
            M.turn()
            half_move(2, dz)
        end
    elseif fz then
        half_move(2, dz)
        if dx ~= 0 then
            M.turn()
            half_move(1, dx)
        end
    end

    pos[1] = dst[1]
    pos[2] = dst[2]
end

return M
