--[[
    overachiever | atlas.lua
    SPDX-License-Identifier: GPL-3.0-only
--]]

local raylib = require("raylib")
local util = require("util")

local atlas_texture = nil
local atlas_meta = {}
local M = {}

--- Loads the texture atlas and its metadata.
--- @return ffi.ctype* texture, table meta The texture and subtextures.
function M.load()
    if atlas_texture ~= nil then
        return
    end

    -- load texture
    local ptr, size = utilc.get_atlas_texture()
    local img = raylib.LoadImageFromMemory(".png", ptr, size);
    atlas_texture = raylib.LoadTextureFromImage(img);
    raylib.UnloadImage(img);

    -- load metadata
    local meta_lines = util.split(utilc.get_atlas_meta(), "\n")
    for _, line in ipairs(meta_lines) do
        local splits = util.split(line, ",")
        if #splits == 5 then
            atlas_meta[splits[5]] = {
                x = tonumber(splits[1]),
                y = tonumber(splits[2]),
                w = tonumber(splits[3]),
                h = tonumber(splits[4])
            }
        end
    end

    return atlas_texture, atlas_meta
end

--- Unloads the texture atlas.
function M.unload()
    if atlas_texture ~= nil then
        raylib.UnloadTexture(atlas_texture)
    end
end

return M
