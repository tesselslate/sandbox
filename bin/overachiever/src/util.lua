--[[
    overachiever | util.lua
    SPDX-License-Identifier: GPL-3.0-only
--]]

local ffi = require("ffi")
local raylib = require("raylib")

local M = {}

--- Checks if a file exists.
--- @param file string Filepath as a string
--- @return boolean result Whether or not the file exists
function M.file_exists(file)
    local fh = io.open(file, "r")
    if fh ~= nil then
        fh:close()
    end

    return fh ~= nil
end

--- Gets a list of files within the given directory.
--- @param dir string The directory to list files within.
--- @return table files The list of files within the directory.
function M.get_dir_files(dir)
    -- call raylib to get dir files
    local res = {}
    local n = 0
    local nptr = ffi.new("int[1]", n)
    local r = raylib.GetDirectoryFiles(dir, nptr)

    for i = 0, nptr[0] - 1, 1 do
        local str = ffi.string(r[i])
        if str:sub(1, 1) ~= "." then
            table.insert(res, str)
        end
    end

    -- free raylib allocations
    raylib.ClearDirectoryFiles()

    return res
end

--- Gets the last time a file was modified.
--- @param file string The file to check.
--- @return number time The last time it was modified.
function M.get_mod_time(file)
    return raylib.GetFileModTime(file)
end

--- Gets a list of .minecraft directories for all running Minecraft instances.
--- @return table directories The list of directories for running instances.
function M.get_instances()
    local res = {}

    local proc = M.run_cmd("pgrep java")
    if not proc then
        return nil
    end

    for _, pid in ipairs(M.split(proc, "\n")) do
        if pid:len() <= 1 then break end
        local ps = M.run_cmd("ps aux | grep " .. pid .. " -m 1")

        for _, arg in ipairs(M.split(ps, " ")) do
            if arg:find("-Djava.library.path=") then
                local natives = M.split(arg, "=")[2]
                local mc = natives:gsub("natives", ".minecraft")
                table.insert(res, mc)
            end
        end
    end

    return res
end

--- Runs a shell command and returns the result.
--- @param cmd string The command to run.
--- @return string result The resulting output.
function M.run_cmd(cmd)
    local h = io.popen(cmd, "r")
    if not h then
        return nil
    end

    return h:read("*a")
end

--- Converts a snake_case string to Title Case.
--- @param input string The string.
--- @return string result The converted string.
function M.snake_to_title(input)
    local words = M.split(input, "_")
    local result = ""

    for _, word in ipairs(words) do
        local upper = word:gsub("^%l", string.upper)
        result = result .. upper .. " "
    end

    return result
end

--- Splits a string by a delimiter.
--- @param input string The input string to split.
--- @param delim string The split delimiter.
--- @return table splits A table containing each split section.
function M.split(input, delim)
    local index = 0
    local res = {}

    while true do
        local a, b = input:find(delim, index)
        if not a then
            table.insert(res, input:sub(index))
            break
        end

        table.insert(res, input:sub(index, a - 1))
        index = b + 1
    end

    return res
end

return M
