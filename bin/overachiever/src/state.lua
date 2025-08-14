--[[
    overachiever | state.lua
    SPDX-License-Identifier: GPL-3.0-only
--]]

local M = {}

local function try_insert(tbl, val)
    for _, v in ipairs(tbl) do
        if v == val then
            return false
        end
    end

    table.insert(tbl, val)
    return true
end

--- Returns the number of fully completed advancements.
--- @param advancements table The JSON advancement data.
--- @return number total The total number of completed advancements.
function M.completion(advancements)
    local res = {}
    local count = 0

    for _, tbl in ipairs(advancements) do
        for k, v in pairs(tbl) do
            if k ~= "DataVersion" and not k:find("minecraft:recipes") then
                if type(v) == "table" and v.done and try_insert(res, k) then
                    count = count + 1
                end
            end
        end
    end

    return count
end

--- Reads the advancement JSON data and returns a neatly organized
--- structure with data about the player's progress.
--- @param advancements table The JSON advancement data.
--- @return table result More nicely formatted data.
function M.progress(advancements)
    local res = {
        done = {},
        adventuring = {},
        catalogue = {},
        diet = {},
        monsters = {},
        passive = {}
    }

    for _, tbl in ipairs(advancements) do
        for k, v in pairs(tbl) do
            if k ~= "DataVersion" and not k:find("minecraft:recipes") and type(v) == "table" then
                -- insert into completed advancements table
                if v.done then
                    try_insert(res.done, k)
                end

                if k == "minecraft:adventure/adventuring_time" then
                    for k, _ in pairs(v.criteria) do
                        table.insert(res.adventuring, k)
                    end
                elseif k == "minecraft:nether/explore_nether" then
                    for k, _ in pairs(v.criteria) do
                        table.insert(res.adventuring, k)
                    end
                elseif k == "minecraft:adventure/kill_all_mobs" then
                    for k, _ in pairs(v.criteria) do
                        table.insert(res.monsters, k)
                    end
                elseif k == "minecraft:husbandry/balanced_diet" then
                    for k, _ in pairs(v.criteria) do
                        table.insert(res.diet, k)
                    end
                elseif k == "minecraft:husbandry/bred_all_animals" then
                    for k, _ in pairs(v.criteria) do
                        table.insert(res.passive, k)
                    end
                elseif k == "minecraft:husbandry/complete_catalogue" then
                    for k, _ in pairs(v.criteria) do
                        table.insert(res.catalogue, k)
                    end
                end
            end
        end
    end

    return res
end

return M
