#include "wm.h"
#include "xkbcommon/xkbcommon-keysyms.h"

#define TERMCOLOR_COUNT 16

static const int cfg_border_size = 2;
static const int cfg_gap_size = 10;
static const char *cfg_terminal = "kitty";

static const char *cfg_colorscheme[COLOR_COUNT] = {
    [BorderActive] = "9ece6a",
    [BorderInactive] = "f7768e",
};
// TODO: replace with actual colors
static const char *cfg_termcolors[TERMCOLOR_COUNT] = {
    "ffffff", /* black */
    "ffffff", /* red */
    "ffffff", /* green */
    "ffffff", /* yellow */
    "ffffff", /* blue */
    "ffffff", /* magenta */
    "ffffff", /* cyan */
    "ffffff", /* white */
    "ffffff", /* bright black */
    "ffffff", /* bright red */
    "ffffff", /* bright green */
    "ffffff", /* bright yellow */
    "ffffff", /* bright blue */
    "ffffff", /* bright magenta */
    "ffffff", /* bright cyan */
    "ffffff", /* bright white */
};

#define MODKEY XCB_MOD_MASK_1
#define MODSHIFT XCB_MOD_MASK_SHIFT
#define MODCTRL XCB_MOD_MASK_CONTROL

static Key cfg_keybinds[] = {
    {MODKEY, XKB_KEY_C, func_close},
    {MODKEY, XKB_KEY_F, func_make_fullscreen},
    {MODKEY, XKB_KEY_H, func_master_dec},
    {MODKEY, XKB_KEY_L, func_master_inc},
    {MODKEY, XKB_KEY_J, func_focus_prev},
    {MODKEY, XKB_KEY_K, func_focus_next},
    {MODKEY, XKB_KEY_Q, func_quit},
    {MODKEY, XKB_KEY_space, func_make_tiling},
    {MODKEY | MODSHIFT, XKB_KEY_J, func_move_stack_down},
    {MODKEY | MODSHIFT, XKB_KEY_K, func_move_stack_up},
    {MODKEY | MODSHIFT | MODCTRL, XKB_KEY_R, func_restart},
    {MODKEY | MODSHIFT, XKB_KEY_Return, func_spawn_terminal},
};

static Button cfg_mousebinds[] = {
    {LocWin, MODKEY, XCB_BUTTON_INDEX_1, mouse_move},
    {LocWin, MODKEY, XCB_BUTTON_INDEX_3, mouse_resize},
};

static Rule cfg_rules[] = {
    {},
};
