-- System imports
local component = require("component")
local szn       = require("serialization")
local sides     = require("sides")

local geolyzer  = component.geolyzer
local inv       = component.inventory_controller
local robot     = component.robot

-- User imports
local cfg       = require("config")

--[[
--
--   Module
--
--]]

local M = {}

--- Attempts to run the given function with the given item slot equipped.
-- @param slot The item slot to equip from
-- @param callback The function to run with the item equipped
-- @raise failed to equip slot
-- @raise failed to unequip slot
-- @raise selected slot changed during equip_scope
M.equip_scoped = function(slot, callback)
    local orig_slot = robot.select()
    robot.select(slot)

    if not inv.equip() then
        error("failed to equip slot " .. slot)
    end

    callback()

    if not inv.equip() then
        error("failed to unequip slot " .. slot)
    end

    assert(robot.select() == slot, "selected slot changed during equip scope")
    robot.select(orig_slot)
end

--- Returns information about the crop beneath the robot.
-- @return The name and statistics of the crop beneath the robot, if any.
M.get_crop = function()
    local block = geolyzer.analyze(sides.down)

    if block.name ~= M.BLOCK_CROP then
        return nil
    elseif block["crop:name"] then
        return {
            name = block["crop:name"],
            gr   = block["crop:growth"],
            ga   = block["crop:gain"],
            re   = block["crop:resistance"]
        }
    else
        return {}
    end
end

--- Returns a pretty printed string containing the given table's contents.
-- @param tbl The table to pretty print
-- @return A string with the table's contents pretty printed
M.inspect = function(tbl)
    return szn.serialize(tbl)
end

--- Returns whether or not the given position represents a child crop.
-- @param pos The position to check
-- @return Whether the position represents a child crop in the breeding field.
M.is_child = function(pos)
    local dx = pos[1] - M.POS_BREEDING[1]
    local dz = pos[2] - M.POS_BREEDING[2]

    return (dx + dz) % 2 == 1
end

--- Calculates and returns the sign of the input number.
-- @param num The number to calculate the sign of
-- @return The sign of the number (1, -1, or 0)
M.sign = function(num)
    if num > 0 then
        return 1
    elseif num < 0 then
        return -1
    else
        return 0
    end
end

--- Returns a pretty printed version of the crop and its statistics.
M.str_crop = function(crop)
    if crop.name then
        return crop.name .. "(" ..
            tostring(crop.gr) .. ", " ..
            tostring(crop.ga) .. ", " ..
            tostring(crop.re) .. ")"
    else
        return "<empty>"
    end
end

M.BLOCK_CROP      = "IC2:blockCrop" -- The IC2 crop block ID.
M.CROP_GRASS      = "Grass"         -- The grass crop ID.
M.CROP_WEED       = "weed"          -- The weed crop ID.
M.POS_BREEDING    = {0, 1}          -- The coordinates of the northwest corner of the breeding field.
M.POS_CROPS       = {3, 0}          -- The coordinates of the crop sticks storage.
M.POS_DISLOCATOR  = {1, 0}          -- The coordinates of the transvector dislocator.
M.POS_DROPOFF     = {4, 0}          -- The coordinates of the excess dropoff inventory.
M.POS_ORIGIN      = {0, 0}          -- The coordinates of the origin.
M.POS_STORAGE     = {-2, -9}        -- The coordinates of the northwest corner of the storage field.
M.SIZE_BREEDING   = 5               -- The side length of the breeding farm.
M.SIZE_STORAGE    = 9               -- The side length of the storage farm.
M.SLOT_CROPS      = 14              -- The crop stick slot ID.
M.SLOT_SPADE      = 15              -- The spade slot ID.
M.SLOT_DISLOCATOR = 16              -- The transvector dislocator slot ID.

return M
