-- System imports
local component = require("component")
local computer  = require("computer")
local sides     = require("sides")

local inv       = component.inventory_controller
local robot     = component.robot
local redstone  = component.redstone

-- User imports
local cfg       = require("config")
local db        = require("db")
local move      = require("move")
local util      = require("util")

--[[
--
--   Internal
--
--]]

--- Trigger the transvector dislocator and set the binder up again.
-- The robot must already have the transvector binder equipped.
local dislocate = function()
    move.to(util.POS_DISLOCATOR)
    redstone.setOutput(sides.down, 15)
    redstone.setOutput(sides.down, 0)
    robot.use(sides.down)
end

--- Restocks on crop sticks if needed. Does not move the robot back.
-- @return Whether or not the robot needed to restock
local restock = function()
    if robot.count(util.SLOT_CROPS) >= cfg.restock_threshold then
        return false
    end

    move.to(util.POS_CROPS)
    robot.select(util.SLOT_CROPS)
    inv.suckFromSlot(sides.down, 2, robot.space(util.SLOT_CROPS))

    return true
end

--- Places the specified number of crop sticks below the robot.
-- @param count The number of crop sticks to place (default: 1)
local place_sticks = function(count)
    local pos = move.get_pos()

    if restock() then
        move.to(pos)
    end

    util.equip_scoped(util.SLOT_CROPS, function()
        for _ = 1, count do
            robot.use(sides.down)
        end
    end)
end

--- Performs a robot "use" action beneath the robot while sneaking.
-- This is primarily used for dislocating crops which may or may not be ready
-- for harvest.
local sneak_down = function()
    return robot.use(sides.down, sides.down, true)
end

--- Attempts to move the currently hovered crop to an empty parent slot.
-- @param pos The current position of the robot
-- @param crop The crop to move
-- @return Whether the crop was transplanted
local transplant_parent = function(pos, crop)
    local slot = db.find_empty_parent()

    if not slot then
        return false
    end

    util.equip_scoped(util.SLOT_DISLOCATOR, function()
        -- Move the crop into the dislocator buffer.
        assert(sneak_down(), "could not bind dislocator to source block")
        dislocate()

        -- Move the crop to the target location within the breeding field.
        move.to(slot)
        assert(sneak_down(), "could not bind dislocator to destination block")
        dislocate()
    end)

    db.clear(pos)
    db.set(slot, crop)

    -- Replace the sticks at the source crop's location so a new crop can
    -- crossbreed in its place.
    move.to(pos)
    place_sticks(2)

    return true
end

--[[
--
--   Module
--
--]]

local M = {}

--- Attempts to place the crop beneath the robot into storage.
-- If a crop with the same name already exists in storage, the crop beneath the
-- robot will simply be destroyed.
-- If no crop exists with the same name, it will be placed into storage. If
-- there is no space, it will be destroyed to roll the chance of a seed drop.
-- @return Whether or not the crop was placed in storage
M.archive = function()
    local pos = move.get_pos()
    local crop = util.get_crop()

    if not db.should_archive(crop.name) then
        M.break_crop()
        M.place_sticks(1)
        return false
    end

    local slot = db.get_storage_slot()
    assert(slot, "no storage slot for crop")

    util.equip_scoped(util.SLOT_DISLOCATOR, function()
        -- Move the crop into the dislocator buffer.
        assert(sneak_down(), "could not bind dislocator to source block")
        dislocate()

        -- Move the crop to the target location within storage.
        move.to(slot)
        assert(sneak_down(), "could not bind dislocator to destination block")
        dislocate()
    end)

    -- Update the database to reflect the crop's movement.
    db.clear(pos)
    db.set(slot, crop)

    -- Put crop sticks back.
    move.to(pos)
    M.place_sticks(2)
end

--- Breaks the crop beneath the robot, preserving the crop stick.
-- @raise could not break crop
M.break_crop = function()
    util.equip_scoped(util.SLOT_SPADE, function()
        assert(robot.use(sides.down), "could not break crop at " .. util.inspect(move.get_pos()))
    end)

    db.clear(move.get_pos())

    M.clear_inventory()
end

--- Breaks the crop stick beneath the robot.
-- @raise could not break crop sticks
M.break_sticks = function()
    util.equip_scoped(util.SLOT_SPADE, function()
        assert(robot.swing(sides.down), "could not break crop sticks")
    end)

    M.clear_inventory()
end

--- Charges the robot if its battery is too low (below 20%).
-- @param ret Whether to return to the previous location after charging
M.charge = function(ret)
    if computer.energy() / computer.maxEnergy() >= 0.25 then
        return
    end

    local pos = move.get_pos()

    move.to(util.POS_ORIGIN)

    while computer.energy() / computer.maxEnergy() < 0.98 do
        os.sleep(1)
    end

    if ret then
        move.to(pos)
    end
end

--- Clears the robot's inventory of crop seeds and drops if it is too full.
-- @param Whether the robot cleared its inventory
M.clear_inventory = function()
    local pos = move.get_pos()

    -- Don't clear the inventory if there are at least 2 empty slots.
    if robot.count(util.SLOT_CROPS - 2) == 0 then
        return false
    end

    move.to(util.POS_DROPOFF)

    local orig_slot = robot.select()

    local last_slot = 0
    local slots = inv.getInventorySize(sides.down)
    assert(slots, "expected dropoff inventory")

    for i = 1, util.SLOT_CROPS - 1 do
        robot.select(i)
        if robot.count(i) == 0 then
            break
        end

        for slot = last_slot + 1, slots do
            last_slot = slot

            if not inv.getStackInSlot(sides.down, slot) then
                inv.dropIntoSlot(sides.down, slot, robot.count(i))
                break
            end
        end
    end

    robot.select(orig_slot)
    move.to(pos)
    return true
end

--- Places the specified number of crop sticks below the robot.
-- @param count The number of crop sticks to place (default: 1)
M.place_sticks = place_sticks

--- Restocks on crop sticks if needed. Does not move the robot back.
-- @return Whether or not the robot needed to restock
M.restock = restock

--- Attempts to replace an existing crop with the crop beneath the robot.
-- If all existing crops have better or equal stats, no replacement will occur
-- and the crop beneath the robot will instead be broken.
-- @return Whether or not the crop was transplanted
M.transplant = function()
    local pos = move.get_pos()
    local crop = util.get_crop()

    local slot = db.find_worst(crop)

    -- If there is no inferior parent crop, try to find an empty parent to
    -- transplant this crop into.
    if not slot then
        return transplant_parent(pos, crop)
    end

    util.equip_scoped(util.SLOT_DISLOCATOR, function()
        -- Move the crop into the dislocator buffer.
        assert(sneak_down(), "could not bind dislocator to source block")
        dislocate()

        -- Move the crop to the target location within the breeding field,
        -- breaking the previous crop and crop sticks at the target location.
        move.to(slot)
        M.break_crop()
        M.break_sticks()
        assert(sneak_down(), "could not bind dislocator to destination block")
        dislocate()
    end)

    db.clear(pos)
    db.set(slot, crop)

    -- Replace the sticks at the source crop's location so a new crop can
    -- crossbreed in its place.
    move.to(pos)
    M.place_sticks(2)

    return true
end

--- Attempts to move the currently hovered crop to an empty parent crop slot.
-- @return Whether or not the crop was transplanted
M.transplant_empty = function()
    local pos = move.get_pos()
    local crop = util.get_crop()

    return transplant_parent(pos, crop)
end

return M
