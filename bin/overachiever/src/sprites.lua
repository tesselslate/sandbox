--[[
    overachiever | sprites.lua
    SPDX-License-Identifier: GPL-3.0-only
--]]

local M = {}

--- Get the list of sprites to display for advancements.
--- @param advancements table The formatted advancements table.
--- @return table result The list of sprites to display.
function M.advancements(advancements)
    local needed = {
        ["story/root"] = "grass_block",
        ["story/mine_stone"] = "wooden_pickaxe",
        ["story/upgrade_tools"] = "stone_pickaxe",
        ["story/smelt_iron"] = "iron_ingot",
        ["story/obtain_armor"] = "iron_chestplate",
        ["story/lava_bucket"] = "lava_bucket",
        ["story/iron_tools"] = "iron_pickaxe",
        ["story/deflect_arrow"] = "shield",
        ["story/form_obsidian"] = "obsidian",
        ["story/mine_diamond"] = "diamond",
        ["story/enter_the_nether"] = "flint_and_steel",
        ["story/shiny_gear"] = "diamond_chestplate",
        ["story/enchant_item"] = "enchanted_book",
        ["story/cure_zombie_villager"] = "golden_apple",
        ["story/follow_ender_eye"] = "ender_eye",
        ["story/enter_the_end"] = "end_stone",
        ["nether/root"] = "netherrack",
        ["nether/return_to_sender"] = "fire_charge",
        ["nether/find_bastion"] = "polished_blackstone",
        ["nether/obtain_ancient_debris"] = "ancient_debris",
        ["nether/fast_travel"] = "map",
        ["nether/find_fortress"] = "nether_bricks",
        ["nether/obtain_crying_obsidian"] = "crying_obsidian",
        ["nether/distract_piglin"] = "gold_ingot",
        ["nether/ride_strider"] = "warped_fungus_on_a_stick",
        ["nether/uneasy_alliance"] = "ghast_tear",
        ["nether/loot_bastion"] = "chest",
        ["nether/use_lodestone"] = "lodestone",
        ["nether/netherite_armor"] = "netherite_chestplate",
        ["nether/get_wither_skull"] = "wither_skeleton_skull",
        ["nether/obtain_blaze_rod"] = "blaze_rod",
        ["nether/charge_respawn_anchor"] = "respawn_anchor",
        ["nether/explore_nether"] = "netherite_boots",
        ["nether/summon_wither"] = "nether_star",
        ["nether/brew_potion"] = "potion",
        ["nether/create_beacon"] = "beacon",
        ["nether/all_potions"] = "milk_bucket",
        ["nether/create_full_beacon"] = "beacon",
        ["nether/all_effects"] = "bucket",
        ["end/root"] = "end_stone",
        ["end/kill_dragon"] = "dragon_head",
        ["end/dragon_egg"] = "dragon_egg",
        ["end/enter_end_gateway"] = "ender_pearl",
        ["end/respawn_dragon"] = "end_crystal",
        ["end/dragon_breath"] = "dragon_breath",
        ["end/find_end_city"] = "purpur_block",
        ["end/elytra"] = "elytra",
        ["end/levitate"] = "shulker_shell",
        ["adventure/root"] = "map",
        ["adventure/voluntary_exile"] = "ominous_banner",
        ["adventure/kill_a_mob"] = "iron_sword",
        ["adventure/trade"] = "emerald",
        ["adventure/honey_block_slide"] = "honey_block",
        ["adventure/ol_betsy"] = "crossbow_standby",
        ["adventure/sleep_in_bed"] = "red_bed",
        ["adventure/hero_of_the_village"] = "ominous_banner",
        ["adventure/throw_trident"] = "trident",
        ["adventure/shoot_arrow"] = "bow",
        ["adventure/kill_all_mobs"] = "diamond_sword",
        ["adventure/totem_of_undying"] = "totem_of_undying",
        ["adventure/summon_iron_golem"] = "carved_pumpkin",
        ["adventure/two_birds_one_arrow"] = "crossbow_standby",
        ["adventure/whos_the_pillager_now"] = "crossbow_standby",
        ["adventure/arbalistic"] = "crossbow_standby",
        ["adventure/adventuring_time"] = "diamond_boots",
        ["adventure/very_very_frightening"] = "trident",
        ["adventure/sniper_duel"] = "arrow",
        ["adventure/bullseye"] = "target",
        ["husbandry/root"] = "hay_bale",
        ["husbandry/safely_harvest_honey"] = "honey_bottle",
        ["husbandry/breed_an_animal"] = "wheat",
        ["husbandry/tame_an_animal"] = "lead",
        ["husbandry/fishy_business"] = "fishing_rod",
        ["husbandry/silk_touch_nest"] = "bee_nest",
        ["husbandry/plant_seed"] = "wheat",
        ["husbandry/bred_all_animals"] = "golden_carrot",
        ["husbandry/complete_catalogue"] = "cod",
        ["husbandry/tactical_fishing"] = "pufferfish_bucket",
        ["husbandry/balanced_diet"] = "apple",
        ["husbandry/obtain_netherite_hoe"] = "netherite_hoe"
    }

    for _, k in ipairs(advancements.done) do
        needed[k:sub(11)] = nil
    end

    local res = {}
    for k, v in pairs(needed) do
        if v ~= nil then
            table.insert(res, { k, v })
        end
    end

    return res
end

--- Get the list of sprites to display for Adventuring Time and Hot Tourist Destinations.
--- @param advancements table The formatted advancements table.
--- @return table result The list of sprites to display.
function M.adventuring(advancements)
    local needed = {
        jungle_edge = true,
        cold_ocean = true,
        snowy_mountains = true,
        forest = true,
        mountains = true,
        badlands_plateau = true,
        mushroom_fields = true,
        taiga = true,
        desert_hills = true,
        giant_tree_taiga = true,
        deep_cold_ocean = true,
        snowy_tundra = true,
        taiga_hills = true,
        desert = true,
        frozen_river = true,
        deep_frozen_ocean = true,
        jungle = true,
        birch_forest = true,
        jungle_hills = true,
        snowy_beach = true,
        bamboo_jungle = true,
        warm_ocean = true,
        deep_lukewarm_ocean = true,
        badlands = true,
        savanna_plateau = true,
        beach = true,
        dark_forest = true,
        river = true,
        lukewarm_ocean = true,
        snowy_taiga = true,
        birch_forest_hills = true,
        wooded_mountains = true,
        bamboo_jungle_hills = true,
        wooded_hills = true,
        giant_tree_taiga_hills = true,
        stone_shore = true,
        wooded_badlands_plateau = true,
        mushroom_field_shore = true,
        swamp = true,
        snowy_taiga_hills = true,
        savanna = true,
        plains = true,
        basalt_deltas = true,
        crimson_forest = true,
        nether_wastes = true,
        soul_sand_valley = true,
        warped_forest = true
    }

    for _, k in ipairs(advancements.adventuring) do
        needed[k:sub(11)] = false
    end

    local res = {}
    for k, v in pairs(needed) do
        if v then
            table.insert(res, k)
        end
    end

    return res
end

--- Get the list of sprites to display for A Complete Catalogue.
--- @param advancements table The formatted advancements table.
--- @return table result The list of sprites to display.
function M.catalogue(advancements)
    local needed = {
        red = true,
        calico = true,
        tabby = true,
        white = true,
        black = true,
        jellie = true,
        siamese = true,
        ragdoll = true,
        british_shorthair = true,
        persian = true,
        all_black = true
    }

    for _, k in ipairs(advancements.catalogue) do
        needed[k:sub(21, -5)] = false
    end

    local res = {}
    for k, v in pairs(needed) do
        if v then
            table.insert(res, k)
        end
    end

    return res
end

--- Get the list of sprites to display for A Balanced Diet.
--- @param advancements table The formatted advancements table.
--- @return table result The list of sprites to display.
function M.diet(advancements)
    local needed = {
        dried_kelp = true,
        melon_slice = true,
        golden_carrot = true,
        beetroot = true,
        cooked_rabbit = true,
        cooked_chicken = true,
        enchanted_golden_apple = true,
        mushroom_stew = true,
        cod = true,
        rabbit_stew = true,
        cooked_salmon = true,
        carrot = true,
        cooked_porkchop = true,
        chicken = true,
        honey_bottle = true,
        cooked_mutton = true,
        sweet_berries = true,
        cooked_beef = true,
        chorus_fruit = true,
        beef = true,
        baked_potato = true,
        porkchop = true,
        tropical_fish = true,
        beetroot_soup = true,
        apple = true,
        spider_eye = true,
        potato = true,
        cooked_cod = true,
        rabbit = true,
        poisonous_potato = true,
        pumpkin_pie = true,
        mutton = true,
        pufferfish = true,
        bread = true,
        golden_apple = true,
        cookie = true,
        rotten_flesh = true,
        suspicious_stew = true,
        salmon = true
    }

    for _, k in ipairs(advancements.diet) do
        needed[k] = false
    end

    local res = {}
    for k, v in pairs(needed) do
        if v then
            table.insert(res, k)
        end
    end

    return res
end

--- Get the list of sprites to display for Monsters Hunted.
--- @param advancements table The formatted advancements table.
--- @return table result The list of sprites to display.
function M.monsters(advancements)
    local needed = {
        endermite = true,
        vex = true,
        zombie = true,
        drowned = true,
        zombie_villager = true,
        hoglin = true,
        blaze = true,
        pillager = true,
        skeleton = true,
        elder_guardian = true,
        zoglin = true,
        ravager = true,
        ghast = true,
        guardian = true,
        vindicator = true,
        magma_cube = true,
        spider = true,
        creeper = true,
        wither = true,
        evoker = true,
        slime = true,
        phantom = true,
        zombified_piglin = true,
        witch = true,
        wither_skeleton = true,
        husk = true,
        ender_dragon = true,
        shulker = true,
        cave_spider = true,
        piglin = true,
        enderman = true,
        silverfish = true,
        stray = true
    }

    for _, k in ipairs(advancements.monsters) do
        needed[k:sub(11)] = false
    end

    local res = {}
    for k, v in pairs(needed) do
        if v then
            table.insert(res, k)
        end
    end

    return res
end

--- Get the list of sprites to display for Two By Two.
--- @param advancements table The formatted advancements table.
--- @return table result The list of sprites to display.
function M.passive(advancements)
    local needed = {
        horse = true,
        rabbit = true,
        bee = true,
        cat = true,
        donkey = true,
        fox = true,
        pig = true,
        llama = true,
        turtle = true,
        sheep = true,
        mule = true,
        hoglin = true,
        mooshroom = true,
        strider = true,
        ocelot = true,
        cow = true,
        chicken = true,
        wolf = true,
        panda = true
    }

    for _, k in ipairs(advancements.passive) do
        needed[k:sub(11)] = false
    end

    local res = {}
    for k, v in pairs(needed) do
        if v then
            table.insert(res, k)
        end
    end

    return res
end

return M
