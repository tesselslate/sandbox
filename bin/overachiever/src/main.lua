--[[
    overachiever | main.lua
    SPDX-License-Identifier: GPL-3.0-only
--]]

local WIN_HEIGHT = 640
local WIN_WIDTH = 480
local MAX_ITEMS = 16

-- load modules
local atlas = require("atlas")
local lang = require("lang")
local raylib = require("raylib")
local sprites = require("sprites")
local state = require("state")
local tracker = require("tracker")
local util = require("util")

-- data
local hasInstance = false
local hasWorld = false

local advancements = {}
local progress = {}
local to_display = {
    advancements = {},
    subobj = {}
}

local ly = 0
local ry = 0

-- initialize raylib
raylib.InitWindow(WIN_WIDTH, WIN_HEIGHT, "overachiever - advancement tracker")
raylib.SetTargetFPS(60)
local frameCount = 0

-- load atlas data
local texture, meta = atlas.load()

local function draw_sprite(name, x, y, w, h)
    local e = meta[name]
    raylib.DrawTexturePro(
        texture,
        raylib.Rectangle(e.x, e.y, e.w, e.h),
        raylib.Rectangle(x, y, w, h),
        raylib.Vector2(0, 0),
        0.0,
        raylib.WHITE
    )
end

local function draw()
    -- check that instance and world available
    if not hasInstance then
        raylib.DrawText("No Minecraft instance found.", 4, WIN_HEIGHT - 24, 20, raylib.DARKGRAY)
        return
    elseif not hasWorld then
        raylib.DrawText("No world loaded.", 4, WIN_HEIGHT - 24, 20, raylib.DARKGRAY)
        return
    end

    local adv_count = state.completion(advancements)
    if adv_count == 80 then
        raylib.DrawText("80/80 advancements | complete", 4, WIN_HEIGHT - 24, 20, raylib.DARKGRAY)
        return
    end

    -- display advancements
    for i, sprite in ipairs(to_display.advancements) do
        draw_sprite(sprite[2], 4, (ly - 64 + i * 40), 32, 32)
        raylib.DrawText(lang.advancements[sprite[1]], 40, (ly - 52 + i * 40), 20, raylib.DARKGRAY)

        if i > MAX_ITEMS then
            break
        end
    end

    -- display subobjectives
    for i, sprite in ipairs(to_display.subobj) do
        draw_sprite(sprite, WIN_WIDTH - 40, (ly - 64 + i * 40), 32, 32)

        if i > MAX_ITEMS then
            break
        end
    end

    -- display total progress
    raylib.DrawRectangle(0, WIN_HEIGHT - 32, WIN_WIDTH, 32, raylib.WHITE)
    raylib.DrawText(
        tostring(adv_count) .. " / 80 advancements | check in " ..
        tostring(math.ceil((600 - frameCount) / 60)) .. "s",

        4, WIN_HEIGHT - 24, 20, raylib.DARKGRAY
    )

    -- update heights
    ly = ly + 1
    ry = ry + 1

    if ly == 40 then
        ly = 0
        local last = table.remove(to_display.advancements)
        table.insert(to_display.advancements, 1, last)
    end

    if ry == 40 then
        ry = 0
        local last = table.remove(to_display.subobj)
        table.insert(to_display.subobj, 1, last)
    end
end

local function update()
    local instances = util.get_instances()
    if instances ~= nil and #instances ~= 0 then
        hasInstance = true
        advancements = tracker.get_advancements(instances)

        if advancements ~= nil then
            hasWorld = true
            progress = state.progress(advancements)

            local advancements = sprites.advancements(progress)
            local adventuring = sprites.adventuring(progress)
            local catalogue = sprites.catalogue(progress)
            local diet = sprites.diet(progress)
            local monsters = sprites.monsters(progress)
            local passive = sprites.passive(progress)

            if #advancements ~= #to_display.advancements then
                to_display.advancements = advancements
            end

            local new_subobj_count = #adventuring +
                #catalogue +
                #diet +
                #monsters +
                #passive

            if new_subobj_count ~= #to_display.subobj then
                local function merge(tbl)
                    for _, v in ipairs(tbl) do
                        table.insert(to_display.subobj, v)
                    end
                end

                to_display.subobj = {}
                merge(adventuring)
                merge(catalogue)
                merge(diet)
                merge(monsters)
                merge(passive)
            end
        else
            hasWorld = false
        end
    else
        hasInstance = false
    end
end

-- attempt to locate instance before starting display
update()

while not raylib.WindowShouldClose() do
    -- render display
    raylib.BeginDrawing()
    raylib.ClearBackground(raylib.WHITE)
    draw()
    raylib.EndDrawing()

    -- refresh advancements every 10 sec
    frameCount = frameCount + 1
    if frameCount == 600 then
        frameCount = 0
        update()
    end
end
