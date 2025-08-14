/*
    overachiever | main.c
    SPDX-License-Identifier: GPL-3.0-only
 */

#include <luajit-2.1/lua.h>
#include <luajit-2.1/lualib.h>
#include <luajit-2.1/lauxlib.h>
#include <raylib.h>
#include "main.h"

/* ----------------------------
    Atlas bundle
   ---------------------------- */

__asm__(
    ".global f_atlas_start\n"
    ".global f_meta_start\n"
    ".global f_atlas_end\n"
    ".global f_meta_end\n"

    "f_atlas_start:\n"
    "   .incbin \"./sprites/atlas.png\"\n"
    "   .byte 0\n"
    "f_atlas_end:\n"

    "f_meta_start:\n"
    "   .incbin \"./sprites/atlas.txt\"\n"
    "   .byte 0\n"
    "f_meta_end:\n"
);

extern const char f_atlas_start;
extern const char f_meta_start;
extern const char f_atlas_end;
extern const char f_meta_end;

/* ----------------------------
    Lua VM setup
   ---------------------------- */

// Lua C module functions.
static const struct luaL_Reg lua_module[] = {
    { "get_atlas_meta",     l_get_atlas_meta    },
    { "get_atlas_texture",  l_get_atlas_texture },
    { NULL, NULL }
};

int l_get_atlas_meta(lua_State *L) {
    lua_pushstring(L, &f_meta_start);
    return 1;
}

int l_get_atlas_texture(lua_State *L) {
    lua_pushlightuserdata(L, (void*) &f_atlas_start);
    lua_pushinteger(L, &f_atlas_end - &f_atlas_start);
    return 2;
}

// Sets up and starts the Lua VM.
int start_lua() {
    printf("overachiever: start lua\n");

    // start lua vm
    lua_State *L = luaL_newstate();
    luaL_openlibs(L);
    printf("overachiever: open lua libraries\n");
    
    // register C module
    luaL_openlib(L, "utilc", lua_module, 0);
    printf("overachiever: open c->lua module\n");

    // run display
    int result = luaL_dostring(L, "require('main')");
    if (result) {
        fprintf(stderr, "lua error: %s\n", lua_tostring(L, -1));

        luaL_traceback(L, L, NULL, 0);

        lua_pop(L, 1);
    }

    // stop
    lua_close(L);
    return 0;
}

int main() {
    start_lua();
}
