-- System imports
local component = require("component")
local shell     = require("shell")
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
]]--

local _, sh_ops = shell.parse()

-- Allow duplicate crops in storage.
db.allow_duplicates = true

-- Bind the dislocator for its first use.
util.equip_scoped(util.SLOT_DISLOCATOR, function()
    move.to(util.POS_DISLOCATOR)
    robot.use(sides.down)
end)

-- Get some crop sticks.
action.restock()

-- Scan the crop field to populate the internal database.
db.scan(not sh_ops["skip-scan"])

local target_crop = nil
for x = 1, util.SIZE_BREEDING - 1, 2 do
    for z = 1, util.SIZE_BREEDING - 1, 2 do
        local pos = {util.POS_BREEDING[1] + x, util.POS_BREEDING[2] + z}

        local crop = db.get(pos)

        if not crop or not crop.name then
            print("Missing parent crops")
            os.exit()
        end

        if not target_crop then
            target_crop = crop.name
        elseif target_crop ~= crop.name then
            print("Multiple crop types found (" .. target_crop .. ", " .. crop.name .. ")")
            os.exit()
        end
    end
end

if not target_crop then
    print("Breeding field not full")
    os.exit()
end

print("Found target crop: " .. target_crop)

--[[
--
--   Main loop
--
]]--

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
                if util.is_weed(crop) then
                    -- If it's a weed, break the weed and put the double sticks
                    -- back.
                    action.break_crop()
                    action.place_sticks(1)
                elseif crop.name == target_crop then
                    -- If it's the target crop, store it for later use (or
                    -- replace a killed parent crop if one exists.)
                    if not action.transplant_duplicate() then
                        if util.stats_ok(crop) then
                            action.archive()
                        else
                            action.break_crop()
                            action.place_sticks(1)
                        end
                    end
                else
                    -- If it's not the target crop, break it.
                    action.break_crop()
                    action.place_sticks(1)
                end
            end
        else
            -- Parent crop

            if crop and util.is_weed(crop) then
                -- If a parent crop gets weeded, simply break the sticks. The
                -- crop will be replanted the next time the bot gets a suitable
                -- child crop.
                action.break_crop()
                action.break_sticks()

                print("Parent crop at " .. util.inspect(pos) .. " killed by weed")
            end
        end
    end)
end
