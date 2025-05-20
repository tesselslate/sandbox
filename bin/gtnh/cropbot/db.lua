-- User imports
local cfg       = require("config")
local scan      = require("scan")
local util      = require("util")

-- State
local pos_table = function()
    local data = {}

    local get_id = function(pos)
        return (pos[1] + 100) * 200 + (pos[2] + 100)
    end

    return setmetatable({}, {
        __pairs = function(self)
            local pk = nil

            return function()
                local k, v = next(data, pk)
                pk = k

                if k then
                    local x = math.floor(k / 200)
                    local z = k % 200

                    return {x, z}, v
                end
            end
        end,

        __index = function(self, k)
            assert(type(k) == "table" and #k == 2, "not a position")

            return data[get_id(k)]
        end,
        __newindex = function(self, k, v)
            assert(type(k) == "table" and #k == 2, "not a position")

            data[get_id(k)] = v
        end,
    })
end

local breeding  = pos_table() -- breeding crops
local storage   = pos_table() -- storage crops

local storage_slots = util.SIZE_STORAGE * util.SIZE_STORAGE -- # of open slots
local target_crop = nil                                     -- breeding target

--[[
--
--   Internal
--
--]]

--- Returns whether or not the given position is in the breeding field.
-- @param pos The position to check
-- @return Whether it is in the breeding field
local is_breeding = function(pos)
    return pos[2] > 0
end

--- Scans a field of crops, storing its contents in tbl.
-- @param tbl The table to store the field contents in
-- @param pos The coordinates of the northwest corner of the field
-- @param size The size of the field
local scan_field = function(tbl, pos, size)
    scan.field(pos, size, function(slot)
        local crop = util.get_crop()

        if crop and crop.name then
            tbl[slot] = crop
        end
    end)
end

--- Calculates a score based on the given crop's statistics.
-- @param crop The crop to score
local score_crop = function(crop)
    return crop.gr + crop.ga - crop.re
end

--- Updates the storage_slots value.
-- @param num The number to adjust storage_slots by
local shift_storage_slots = function(num)
    storage_slots = storage_slots + num
    print("Storage slots: " .. tostring(storage_slots))
end

--[[
--
--   Module
--
--]]

local M = {}

--- Clears the data about the crop at the given position from the database.
-- @param pos The position to clear from the database
M.clear = function(pos)
    if is_breeding(pos) then
        breeding[pos] = nil
    else
        if storage[pos] then
            assert(storage_slots < util.SIZE_STORAGE * util.SIZE_STORAGE, "storage_slots desynchronized")
            shift_storage_slots(1)
        end

        storage[pos] = nil
    end
end

--- Attempts to find a breeding crop worse than the comparison crop.
-- @param comp The new crossbred crop to compare against
-- @return The coordinates of an inferior crop, if any
M.find_worst = function(comp)
    -- Crops which exceed the desired maximum growth or resistance stats should
    -- be destroyed.
    if comp.gr > cfg.max_growth or comp.re > cfg.max_resistance then
        return nil
    end

    -- Sort the list of breeding crops based on their stats, and then compare the
    -- lowest stat crop against the comparison crop.
    local worst = nil
    local worst_score = 10000
    for k, v in pairs(breeding) do
        if not util.is_child(k) then
            local val = score_crop(v)
            if val < worst_score then
                worst_score = val
                worst = k
            end
        end
    end

    -- Only return the worst crop if the comparison crop is actually better.
    if worst_score < score_crop(comp) then
        return worst
    end
end

--- Finds an open storage slot for a crop to be placed in.
-- @return The coordinates of an open slot in the storage field
-- @raise could not find storage slot
M.get_storage_slot = function()
    for x = 0, util.SIZE_STORAGE - 1 do
        for z = 0, util.SIZE_STORAGE - 1 do
            local pos = {util.POS_STORAGE[1] + x, util.POS_STORAGE[2] + z}

            if not storage[pos] then
                return pos
            end
        end
    end

    error("could not find storage slot")
end

--- Returns the target crop for stats breeding.
-- @return The target crop name
M.get_target_crop = function()
    assert(target_crop, "must have target crop")

    return target_crop
end

--- Scans the breeding and storage fields to initialize the in-memory database.
-- @param do_storage Whether to scan the storage field
-- @raise multiple parent crop types found
-- @raise parent slots not filled
M.scan = function(do_storage)
    breeding = pos_table()
    scan_field(breeding, util.POS_BREEDING, util.SIZE_BREEDING)

    local num_breeding = 0
    for k, v in pairs(breeding) do
        if v and not util.is_child(k) then
            if not target_crop then
                target_crop = v.name
            else
                if v.name ~= target_crop then
                    error("multiple parent crop types found (" .. v.name .. ")")
                end
            end

            num_breeding = num_breeding + 1
        end
    end

    local expected = (util.SIZE_BREEDING * util.SIZE_BREEDING) // 2 + 1
    if num_breeding ~= expected then
        error("parent slots not filled (" .. tostring(num_breeding) .. "/" .. tostring(expected) .. ")")
    end

    if do_storage then
        storage = pos_table()
        scan_field(storage, util.POS_STORAGE, util.SIZE_STORAGE)

        for k, v in pairs(storage) do
            if v then
                storage_slots = storage_slots - 1
                print("Stored crop: " .. util.str_crop(v))
            end
        end
    end

    shift_storage_slots(0)
end

--- Places the given position and crop pairing into the database.
-- @param pos The position to store the crop at
-- @param crop The crop to store in the database
M.set = function(pos, crop)
    assert(crop, "db.set must have a crop")

    if is_breeding(pos) then
        breeding[pos] = crop
    else
        if not storage[pos] then
            assert(storage_slots > 0, "storage_slots desynchronized")
            shift_storage_slots(-1)
        end

        storage[pos] = crop
    end
end

--- Returns whether or not a crop with the given name should be archived.
-- @param crop_name The name of the crop to check for
-- @return Whether or not a crop with the given name should be archived
M.should_archive = function(crop_name)
    for k, v in pairs(storage) do
        if type(v) == "table" and v.name == crop_name then
            print("Already stored " .. crop_name)
            return false
        end
    end

    return storage_slots > 0
end

return M
