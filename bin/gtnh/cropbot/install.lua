local internet = require("internet")
local filesystem = require("filesystem")

local base = "https://raw.githubusercontent.com/tesselslate/sandbox/refs/heads/main/bin/gtnh/cropbot/"
local files = {
    "action.lua",
    "bot_stat.lua",
    "config.lua",
    "db.lua",
    "move.lua",
    "scan.lua",
    "util.lua",
}

for _, file in ipairs(files) do
    local handle = filesystem.open("/home/" .. file, "w")

    for chunk in internet.request(base .. file) do
        handle:write(chunk)
        os.sleep(0)
    end

    local sz = handle:seek("cur", 0)
    print("Downloaded " .. file .. " (" .. tostring(sz) .. " bytes)")

    handle:close()
end
