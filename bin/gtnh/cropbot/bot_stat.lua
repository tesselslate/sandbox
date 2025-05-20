-- System imports
local component = require("component")
local sides     = require("sides")

local robot     = component.robot

-- User imports
local action    = require("action")
local db        = require("db")
local move      = require("move")
local scan      = require("scan")
local util      = require("util")

--[[
--
--   Initialization
--
--]]

-- Bind the dislocator for its first use.
util.equip_scoped(util.SLOT_DISLOCATOR, function()
    move.to(util.POS_DISLOCATOR)
    robot.use(sides.down)
end)

-- Get some crop sticks.
action.restock()

-- Scan the crop field to populate the internal database.
db.scan(true)
print("Found target crop: " .. db.get_target_crop())

--[[
--
--   Main loop
--
--]]

while true do
    -- Recharge if low on battery.
    action.charge()

    scan.field(util.POS_BREEDING, util.SIZE_BREEDING, function(pos)
        local crop = util.get_crop()

        if util.is_child(pos) then
            -- Child crop

            if not crop then
                -- Place double sticks on empty child crop slots.
                action.place_sticks(2)
            elseif crop.name then
                -- Process the new child crop.
                if util.is_weed(crop) then
                    -- If it's a weed, break the weed and put the double sticks
                    -- back.
                    action.break_crop()
                    action.place_sticks(1)
                elseif crop.name ~= db.get_target_crop() then
                    -- If it's not the target crop, try storing it.
                    action.archive()
                else
                    -- If it is the target crop, try finding an inferior parent
                    -- to replace.
                    if not action.transplant() then
                        -- If there is no inferior crop to replace, destroy it.
                        action.break_crop()
                        action.place_sticks(1)
                    end
                end
            end
        else
            -- Parent crop

            if crop and util.is_weed(crop) then
                -- If a parent crop gets weeded, simply break the sticks. The
                -- crop will be replanted the next time the bot gets an
                -- unsuitable child crop.
                action.break_crop()
                action.break_sticks()

                print("Parent crop at " .. util.inspect(pos) .. " killed by weed")
            end
        end
    end)
end
