--[[
    overachiever | tracker.lua
    SPDX-License-Identifier: GPL-3.0-only
--]]

local json = require("json")
local util = require("util")

local M = {}

--- Reads all of the advancement files from the most recent instance's world.
--- @param instances table The list of minecraft directories.
--- @return table res The table containing all advancement data for the world.
function M.get_advancements(instances)
    local res = {}

    -- get recent instance log file
    local recent = M.recent(instances)
    local log = instances[recent] .. "/logs/latest.log"

    local world_name = nil

    -- https://stackoverflow.com/a/497750
    local fh = io.open(log, "r")
    local pos = fh:seek("end")

    -- read from backward of file 256 bytes at a time
    while world_name == nil do
        fh:seek("set", math.max(0, pos - 256))
        pos = pos - 256

        local lines = util.split(fh:read("*a"), "\n")
        for _, line in ipairs(lines) do
            if line:find("Saving chunks for level") then
                local left = line:find("ServerLevel%[")
                local right = line:find("%]%'%/")
                world_name = line:sub(left + 12, right - 1)

                break
            end
        end

        if pos <= 0 then
            break
        end
    end

    fh:close()

    if not world_name then
        return nil
    end

    -- get advancements
    local adv_dir = instances[recent] .. "/saves/" .. world_name .. "/advancements"
    local adv_files = util.get_dir_files(adv_dir)
    for _, file in ipairs(adv_files) do
        local path = adv_dir .. "/" .. file
        local fh = io.open(path, "r")
        local contents = fh:read("*a")
        fh:close()

        table.insert(res, json.decode(contents))
    end

    print("overachiever: read advancements from world " .. world_name .. " instance " .. recent)

    return res
end

--- Determines which instance has been most recently played.
--- @param instances table The list of minecraft directories.
--- @return number number The index of the most recent instance.
function M.recent(instances)
    local most_recent_time = 0
    local most_recent = -1

    for i, dir in ipairs(instances) do
        local log = dir .. "/logs/latest.log"
        if util.file_exists(log) then
            local mod_time = util.get_mod_time(log)
            if mod_time > most_recent_time then
                most_recent_time = mod_time
                most_recent = i
            end
        end
    end

    return most_recent
end

return M
