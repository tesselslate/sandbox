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

local M = {}

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

--- Returns the position of a parent crop whose name does not match, if any.
-- @param target_name The name of the target breeding crop
-- @return The position of a parent crop whose name does not match, if any
local find_parent = function(target_name)
    for x = 0, util.SIZE_BREEDING - 1, 2 do
        for z = 0, util.SIZE_BREEDING - 1, 2 do
            local pos = {util.POS_BREEDING[1] + x, util.POS_BREEDING[2] + z}
            local crop = db.get(pos)

            if crop and crop.name ~= target_name then
                return pos
            end
        end
    end
end

--- Attempts to find a worse target crop parent to replace.
-- @param crop The source crop
-- @return The position of a worse target crop, if any
local find_worse_parent = function(crop)
    local score = util.score_crop(crop)

    for x = 1, util.SIZE_BREEDING - 2, 2 do
        for z = 1, util.SIZE_BREEDING - 2, 2 do
            local candidate_pos = {util.POS_BREEDING[1] + x, util.POS_BREEDING[2] + z}
            local candidate = db.get(candidate_pos)

            if not candidate then
                return candidate_pos
            elseif util.score_crop(candidate) < score then
                return candidate_pos
            end
        end
    end
end

--- Performs a robot "use" action beneath the robot while sneaking.
-- This is primarily used for dislocating crops which may or may not be ready
-- for harvest.
local sneak_down = function()
    return robot.use(sides.down, sides.down, true)
end

--- Moves a crop from one position to another, breaking the destination crop.
-- @param src The position of the crop to move
-- @param dst The position to move the crop to
local move_crop = function(src, dst)
    move.to(src)
    local src_crop = util.get_crop()

    util.equip_scoped(util.SLOT_DISLOCATOR, function()
        -- Move the crop into the dislocator buffer.
        assert(sneak_down(), "could not bind dislocator to source block")
        dislocate()

        -- Move the crop to the destination, breaking the previous crop and crop
        -- sticks (if any) at the destination.
        move.to(dst)
        local dst_crop = util.get_crop()

        if dst_crop then
            if dst_crop.name then
                M.break_crop()
            end
            M.break_sticks()
        end

        assert(sneak_down(), "could not bind dislocator to destination block")
        dislocate()
    end)

    db.clear(src)
    db.set(dst, src_crop)
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

--[[
--
--   Module
--
--]]

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

    -- Move the crop into storage.
    move_crop(pos, slot)

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

--- Attempts to transplant the crop beneath the robot with the duplicate rules.
-- 1. If there is an existing parent crop whose species is not the target
-- species (typically stickreed), it will be replaced.
-- 2. If there is an empty parent crop slot, the hovered crop will get moved
-- there.
-- @param target_name The name of the target breeding crop
-- @return Whether or not the crop was transplanted
M.transplant_duplicate = function(target_name)
    local pos = move.get_pos()
    local crop = util.get_crop()
    local slot

    -- If this crop is not good enough, check if its parents are worse and need
    -- to be statted up.
    if not util.stats_ok(crop) then
        slot = find_worse_parent(crop)

        if not slot then
            return false
        end
    end

    if not slot then
        slot = find_parent(target_name)
    end

    -- If there is no suitable parent crop, try to find an empty parent to
    -- transplant this crop into.
    if not slot then
        slot = db.find_empty_parent()

        if not slot then
            return false
        end
    end

    -- Transplant the crop.
    move_crop(pos, slot)

    -- Replace the sticks at the source crop's location so a new crop can
    -- crossbreed in its place.
    move.to(pos)
    M.place_sticks(2)

    return true
end

--- Attempts to transplant the crop beneath the robot with the stat rules.
-- 1. If there is an existing parent crop with inferior stats, it will be
-- replaced.
-- 2. If there is an empty parent crop slot, the hovered crop will get moved
-- there regardless of its stats.
-- @return Whether or not the crop was transplanted
M.transplant_stat = function()
    local pos = move.get_pos()
    local crop = util.get_crop()

    local slot = db.find_worst(crop)

    -- If there is no inferior parent crop, try to find an empty parent to
    -- transplant this crop into.
    if not slot then
        slot = db.find_empty_parent()

        if not slot then
            return false
        end
    end

    -- Transplant the crop.
    move_crop(pos, slot)

    -- Replace the sticks at the source crop's location so a new crop can
    -- crossbreed in its place.
    move.to(pos)
    M.place_sticks(2)

    return true
end

return M
