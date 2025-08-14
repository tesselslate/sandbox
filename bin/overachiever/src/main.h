/*
    overachiever | main.h
    SPDX-License-Identifier: GPL-3.0-only
 */

#include <luajit-2.1/lua.h>
#include <stddef.h>

// Returns a string containing the atlas metadata.
int l_get_atlas_meta(lua_State *L);

// Returns the atlas texture after loading with raylib.
int l_get_atlas_texture(lua_State *L);
