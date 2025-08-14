--[[
    overachiever | lang.lua
    SPDX-License-Identifier: GPL-3.0-only
--]]

local util = require("util")

local snake_mt = {
    __index = util.snake_to_title
}

local M = {}
M.advancements = {
    ["story/root"] = "Minecraft",
    ["story/mine_stone"] = "Stone Age",
    ["story/upgrade_tools"] = "Getting an Upgrade",
    ["story/smelt_iron"] = "Acquire Hardware",
    ["story/obtain_armor"] = "Suit Up",
    ["story/lava_bucket"] = "Hot Stuff",
    ["story/iron_tools"] = "Isn't It Iron Pick",
    ["story/deflect_arrow"] = "Not Today, Thank You",
    ["story/form_obsidian"] = "Ice Bucket Challenge",
    ["story/mine_diamond"] = "Diamonds!",
    ["story/enter_the_nether"] = "We Need to Go Deeper",
    ["story/shiny_gear"] = "Cover Me With Diamonds",
    ["story/enchant_item"] = "Enchanter",
    ["story/cure_zombie_villager"] = "Zombie Doctor",
    ["story/follow_ender_eye"] = "Eye Spy",
    ["story/enter_the_end"] = "The End?",
    ["nether/root"] = "Nether",
    ["nether/return_to_sender"] = "Return to Sender",
    ["nether/find_bastion"] = "Those Were the Days",
    ["nether/obtain_ancient_debris"] = "Hidden in the Depths",
    ["nether/fast_travel"] = "Subspace Bubble",
    ["nether/find_fortress"] = "A Terrible Fortress",
    ["nether/obtain_crying_obsidian"] = "Who is Cutting Onions?",
    ["nether/distract_piglin"] = "Oh Shiny",
    ["nether/ride_strider"] = "This Boat Has Legs",
    ["nether/uneasy_alliance"] = "Uneasy Alliance",
    ["nether/loot_bastion"] = "War Pigs",
    ["nether/use_lodestone"] = "Country Lode, Take Me Home",
    ["nether/netherite_armor"] = "Cover Me in Debris",
    ["nether/get_wither_skull"] = "Spooky Scary Skeleton",
    ["nether/obtain_blaze_rod"] = "Into Fire",
    ["nether/charge_respawn_anchor"] = "Not Quite \"Nine\" Lives",
    ["nether/explore_nether"] = "Hot Tourist Destinations",
    ["nether/summon_wither"] = "Withering Heights",
    ["nether/brew_potion"] = "Local Brewery",
    ["nether/create_beacon"] = "Bring Home the Beacon",
    ["nether/all_potions"] = "A Furious Cocktail",
    ["nether/create_full_beacon"] = "Beaconator",
    ["nether/all_effects"] = "How Did We Get Here?",
    ["end/root"] = "The End?",
    ["end/kill_dragon"] = "Free the End",
    ["end/dragon_egg"] = "The Next Generation",
    ["end/enter_end_gateway"] = "Remote Getaway",
    ["end/respawn_dragon"] = "The End... Again...",
    ["end/dragon_breath"] = "You Need a Mint",
    ["end/find_end_city"] = "The City at the End of the Game",
    ["end/elytra"] = "Sky's the Limit",
    ["end/levitate"] = "Great View From Up Here",
    ["adventure/root"] = "Adventure",
    ["adventure/voluntary_exile"] = "Voluntary Exile",
    ["adventure/kill_a_mob"] = "Monster Hunter",
    ["adventure/trade"] = "What a Deal!",
    ["adventure/honey_block_slide"] = "Sticky Situation",
    ["adventure/ol_betsy"] = "Ol' Betsy",
    ["adventure/sleep_in_bed"] = "Sweet Dreams",
    ["adventure/hero_of_the_village"] = "Hero of the Village",
    ["adventure/throw_trident"] = "A Throwaway Joke",
    ["adventure/shoot_arrow"] = "Take Aim",
    ["adventure/kill_all_mobs"] = "Monsters Hunted",
    ["adventure/totem_of_undying"] = "Postmortal",
    ["adventure/summon_iron_golem"] = "Hired Help",
    ["adventure/two_birds_one_arrow"] = "Two Birds, One Arrow",
    ["adventure/whos_the_pillager_now"] = "Who's the Pillager Now?",
    ["adventure/arbalistic"] = "Arbalistic",
    ["adventure/adventuring_time"] = "Adventuring Time",
    ["adventure/very_very_frightening"] = "Very Very Frightening",
    ["adventure/sniper_duel"] = "Sniper Duel",
    ["adventure/bullseye"] = "Bullseye",
    ["husbandry/root"] = "Husbandry",
    ["husbandry/safely_harvest_honey"] = "Bee Our Guest",
    ["husbandry/breed_an_animal"] = "The Parrots and the Bats",
    ["husbandry/tame_an_animal"] = "Best Friends Forever",
    ["husbandry/fishy_business"] = "Fishy Business",
    ["husbandry/silk_touch_nest"] = "Total Beelocation",
    ["husbandry/plant_seed"] = "A Seedy Place",
    ["husbandry/bred_all_animals"] = "Two by Two",
    ["husbandry/complete_catalogue"] = "A Complete Catalogue",
    ["husbandry/tactical_fishing"] = "Tactical Fishing",
    ["husbandry/balanced_diet"] = "A Balanced Diet",
    ["husbandry/obtain_netherite_hoe"] = "Serious Dedication"
}

M.adventuring = {}
setmetatable(M.adventuring, snake_mt)

M.catalogue = {
    red = "Red",
    calico = "Calico",
    tabby = "Tabby",
    white = "White",
    black = "Black",
    jellie = "Jellie",
    siamese = "Siamese",
    ragdoll = "Ragdoll",
    british_shorthair = "British Shorthair",
    persian = "Persian",
    all_black = "Tuxedo"
}

M.diet = {
    dried_kelp = "Dried Kelp",
    melon_slice = "Melon Slice",
    golden_carrot = "Golden Carrot",
    beetroot = "Beetroot",
    cooked_rabbit = "Cooked Rabbit",
    cooked_chicken = "Cooked Chicken",
    enchanted_golden_apple = "God Apple",
    mushroom_stew = "Mushroom Stew",
    cod = "Raw Cod",
    rabbit_stew = "Rabbit Stew",
    cooked_salmon = "Cooked Salmon",
    carrot = "Carrot",
    cooked_porkchop = "Cooked Porkchop",
    chicken = "Raw Chicken",
    honey_bottle = "Honey Bottle",
    cooked_mutton = "Cooked Mutton",
    sweet_berries = "Sweet Berries",
    cooked_beef = "Steak",
    chorus_fruit = "Chorus Fruit",
    beef = "Raw Beef",
    baked_potato = "Baked Potato",
    porkchop = "Raw Porkchop",
    tropical_fish = "Tropical Fish",
    beetroot_soup = "Beetroot Soup",
    apple = "Apple",
    spider_eye = "Spider Eye",
    potato = "Potato",
    cooked_cod = "Cooked Cod",
    rabbit = "Raw Rabbit",
    poisonous_potato = "Poisonous Potato",
    pumpkin_pie = "Pumpkin Pie",
    mutton = "Mutton",
    pufferfish = "Pufferfish",
    bread = "Bread",
    golden_apple = "Golden Apple",
    cookie = "Cookie",
    rotten_flesh = "Rotten Flesh",
    suspicious_stew = "Suspicious Stew",
    salmon = "Raw Salmon"
}

M.monsters = {}
setmetatable(M.monsters, snake_mt)

M.passive = {}
setmetatable(M.passive, snake_mt)

return M
