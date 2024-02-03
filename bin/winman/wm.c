#include "wm.h"
#include "config.h"
#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <xcb/xcb.h>
#include <xcb/xcb_cursor.h>
#include <xcb/xcb_keysyms.h>
#include <xcb/xproto.h>

#define ARRAY_LENGTH(array) (int)(sizeof(array) / sizeof(array[0]))
#define BUTTON_MASK XCB_EVENT_MASK_BUTTON_PRESS | XCB_EVENT_MASK_BUTTON_RELEASE
#define CONFIG_MASK                                                            \
    XCB_CONFIG_WINDOW_X | XCB_CONFIG_WINDOW_Y | XCB_CONFIG_WINDOW_WIDTH |      \
        XCB_CONFIG_WINDOW_HEIGHT
#define GAP_NONE 0
#define GAP_FULL 1
#define GAP_HALF 2
#define MAX(a, b) (a > b ? a : b)
#define MOTION_MASK                                                            \
    XCB_EVENT_MASK_BUTTON_PRESS | XCB_EVENT_MASK_BUTTON_RELEASE |              \
        XCB_EVENT_MASK_POINTER_MOTION | XCB_EVENT_MASK_BUTTON_MOTION
#define WM_NAME "winman"

#define SPAWN(cmd) mg_spawn(cmd, (const char **){NULL})
#define WIN_IS_FLOATING(win) ((win->flags & WIN_FLOATING) != 0)
#define WIN_IS_FULLSCREEN(win) ((win->flags & WIN_FULLSCREEN) != 0)
#define WIN_IS_TILED(win) (!WIN_IS_FLOATING(win) && !WIN_IS_FULLSCREEN(win))

static xcb_atom_t atoms[ATOM_COUNT];
static char *atom_names[ATOM_COUNT] = {
    [ATOM_DELETE_WINDOW] = "WM_DELETE_WINDOW",
    [ATOM_NET_ACTIVE_WINDOW] = "_NET_ACTIVE_WINDOW",
    [ATOM_NET_CLIENT_LIST] = "_NET_CLIENT_LIST",
    [ATOM_NET_CLOSE_WINDOW] = "_NET_CLOSE_WINDOW",
    [ATOM_NET_SUPPORTED] = "_NET_SUPPORTED",
    [ATOM_NET_SUPPORTING_WM_CHECK] = "_NET_SUPPORTING_WM_CHECK",
    [ATOM_NET_WM_NAME] = "_NET_WM_NAME",
    [ATOM_NET_WM_WINDOW_TYPE] = "_NET_WM_WINDOW_TYPE",
    [ATOM_NET_WM_WINDOW_TYPE_DIALOG] = "_NET_WM_WINDOW_TYPE_DIALOG",
    [ATOM_UTF8_STRING] = "UTF8_STRING",
    [ATOM_WM_CLASS] = "WM_CLASS",
    [ATOM_WM_NAME] = "WM_NAME",
    [ATOM_WM_NORMAL_HINTS] = "WM_NORMAL_HINTS",
    [ATOM_WM_PROTOCOLS] = "WM_PROTOCOLS",
    [ATOM_WM_TAKE_FOCUS] = "WM_TAKE_FOCUS",
    [ATOM_WM_TRANSIENT_FOR] = "WM_TRANSIENT_FOR",
};
static uint32_t colors[COLOR_COUNT];
static xcb_cursor_t cursors[CURSOR_COUNT];
static uint32_t termcolors[TERMCOLOR_COUNT];

static char *const *args;
static xcb_window_t ewmh_check_win;
static Window *focused = NULL;
static float master_scale = 0.5;
static int16_t mouse_x, mouse_y;
static int please_quit = 0;
static xcb_screen_t *screen = NULL;
static int screen_width, screen_height;
static Window *winlist = NULL;
static xcb_connection_t *xcb = NULL;

// Prints the specified error message and exits.
static void die(const char *text) {
    fprintf(stderr, "%s\n", text);
    exit(1);
}

// Gets the keycode from the given keysymbol. Returns 0 if failed.
static xcb_keycode_t get_keycode(xcb_keysym_t sym) {
    xcb_keycode_t *keycode;
    xcb_key_symbols_t *keysyms = xcb_key_symbols_alloc(xcb);
    if (!keysyms) {
        return 0;
    }
    keycode = xcb_key_symbols_get_keycode(keysyms, sym);
    xcb_key_symbols_free(keysyms);
    xcb_keycode_t code = *keycode;
    free(keycode);
    return code;
}

// Gets a string property from a window.
static char *get_string_property(xcb_window_t win, Atom property) {
    xcb_atom_t atom = atoms[property];
    xcb_get_property_cookie_t cookie =
        xcb_get_property(xcb, 0, win, atom, XCB_ATOM_STRING, 0, UINT32_MAX);
    xcb_generic_error_t *err;
    xcb_get_property_reply_t *reply = xcb_get_property_reply(xcb, cookie, &err);
    if (err) {
        free(reply);
        return NULL;
    }
    int len = xcb_get_property_value_length(reply);
    char *buf = malloc(len + 1);
    if (!buf) {
        free(reply);
        return NULL;
    }
    void *str = xcb_get_property_value(reply);
    memcpy(buf, str, len);
    free(reply);
    return buf;
}

// Check if the given window supports the given protocol.
static int is_protocol_supported(xcb_window_t win, xcb_atom_t protocol) {
    xcb_get_property_cookie_t cookie = xcb_get_property(
        xcb, 0, win, atoms[ATOM_WM_PROTOCOLS], XCB_ATOM_ATOM, 0, UINT32_MAX);
    xcb_generic_error_t *err;
    xcb_get_property_reply_t *reply = xcb_get_property_reply(xcb, cookie, &err);
    if (err) {
        free(reply);
        return 0;
    }
    xcb_atom_t *supported = xcb_get_property_value(reply);
    for (int i = 0; i < xcb_get_property_value_length(reply) / 4; i++) {
        if (supported[i] == protocol) {
            free(reply);
            return 1;
        }
    }
    free(reply);
    return 0;
}

// Gets the RGB color components of a hex color string.
static void parse_rgb(const char *rgb, unsigned int *r, unsigned int *g,
                      unsigned int *b) {
    sscanf(rgb, "%2x%2x%2x", r, g, b);
}

// Prints information about the given XCB error.
static void print_xcb_error(xcb_generic_error_t *err) {
    if (!err) {
        return;
    }
    fprintf(stderr,
            "XCB error\nResponse type: %i\nError code: %i\nSequence: "
            "%i\nResource: %i\nMinor: %i\nMajor: %i\n",
            err->response_type, err->error_code, err->sequence,
            err->resource_id, err->minor_code, err->major_code);
}

// Returns 1 if the given window is tiled, otherwise false.
static int comp_tiled(Window *win) {
    return WIN_IS_TILED(win);
}

// Handle a button press event.
static void evt_button_press(xcb_button_press_event_t *evt) {
    Window *win = winlist_find(evt->event);
    if (!win) {
        return;
    }
    // Focus windows when clicked.
    if (evt->event != focused->win) {
        mg_focus_window(win);
    }

    // Check for mouse binds.
    for (int i = 0; i < ARRAY_LENGTH(cfg_mousebinds); i++) {
        // TODO: Check for bar tag keybinds once the bar is implemented.
        if (cfg_mousebinds[i].loc == LocWin &&
            cfg_mousebinds[i].button == evt->detail &&
            cfg_mousebinds[i].mod == evt->state) {
            cfg_mousebinds[i].func(win);
        }
    }
}

// Handle a client message event.
static void evt_client_message(xcb_client_message_event_t *evt) {
    // TODO: handle _NET_CURRENT_DESTKOP message
    if (evt->format != 32) {
        return;
    }
    if (evt->type == atoms[ATOM_NET_ACTIVE_WINDOW]) {
        Window *win = winlist_find(evt->window);
        if (!win) {
            return;
        }
        mg_focus_window(win);
    } else if (evt->type == atoms[ATOM_NET_CLOSE_WINDOW]) {
        mg_close_window(evt->window);
    }
}

// Handle a configure request event.
static void evt_config_request(xcb_configure_request_event_t *evt) {
    Window *win = winlist_find(evt->window);

    // Extract the necessary properties from the request.
    int x = (evt->value_mask & XCB_CONFIG_WINDOW_X) != 0;
    int y = (evt->value_mask & XCB_CONFIG_WINDOW_Y) != 0;
    int w = (evt->value_mask & XCB_CONFIG_WINDOW_WIDTH) != 0;
    int h = (evt->value_mask & XCB_CONFIG_WINDOW_HEIGHT) != 0;
    int s = !win && (evt->value_mask & XCB_CONFIG_WINDOW_SIBLING) != 0;
    int m = !win && (evt->value_mask & XCB_CONFIG_WINDOW_STACK_MODE) != 0;
    int count = x + y + w + h + s + m;
    uint32_t values[count];
    int i = 0;
    int mask = 0;
    if (x) {
        values[i++] = evt->x;
        mask &= XCB_CONFIG_WINDOW_X;
    }
    if (y) {
        values[i++] = evt->y;
        mask &= XCB_CONFIG_WINDOW_Y;
    }
    if (w) {
        values[i++] = evt->width;
        mask &= XCB_CONFIG_WINDOW_WIDTH;
    }
    if (h) {
        values[i++] = evt->height;
        mask &= XCB_CONFIG_WINDOW_HEIGHT;
    }
    if (s) {
        values[i++] = evt->sibling;
        mask &= XCB_CONFIG_WINDOW_SIBLING;
    }
    if (m) {
        values[i++] = evt->stack_mode;
        mask &= XCB_CONFIG_WINDOW_STACK_MODE;
    }

    // Set the window's properties accordingly.
    if (win) {
        if (x)
            win->x = evt->x;
        if (y)
            win->y = evt->y;
        if (w)
            win->w = evt->width;
        if (h)
            win->h = evt->height;
    }

    // Ignore the request if the window is tiled.
    if (win && WIN_IS_TILED(win)) {
        return;
    }

    // Forward the request.
    xcb_configure_window(xcb, evt->window, mask, values);
}

// Handle a destroy notify event.
static void evt_destroy_notify(xcb_destroy_notify_event_t *evt) {
    mg_del_window(evt->window);
}

// Handle a key press event.
static void evt_key_press(xcb_key_press_event_t *evt) {
    for (int i = 0; i < ARRAY_LENGTH(cfg_keybinds); i++) {
        if (cfg_keybinds[i].sym == evt->detail &&
            cfg_keybinds[i].mod == evt->state) {
            cfg_keybinds[i].func();
        }
    }
}

// Handle a mapping notify event.
static void evt_mapping_notify(xcb_mapping_notify_event_t *evt) {
    // Refresh keyboard.
    xcb_key_symbols_t *keysyms = xcb_key_symbols_alloc(xcb);
    if (!keysyms) {
        return;
    }
    xcb_refresh_keyboard_mapping(keysyms, evt);
    if (evt->request == XCB_MAPPING_KEYBOARD) {
        mg_grab_keys();
    }
    free(keysyms);
}

// Handle a map window request event.
static void evt_map_request(xcb_map_request_event_t *evt) {
    // Do nothing if the window is already managed.
    if (winlist_find(evt->window)) {
        return;
    }

    // Ignore the map request if the window has override-redirect set.
    xcb_get_window_attributes_cookie_t cookie =
        xcb_get_window_attributes(xcb, evt->window);
    xcb_generic_error_t *err;
    xcb_get_window_attributes_reply_t *reply =
        xcb_get_window_attributes_reply(xcb, cookie, &err);
    if (err) {
        fprintf(stderr, "evt_map_request: geometry error\n");
        return;
    }
    int override = reply->override_redirect;
    free(reply);
    if (override) {
        return;
    }

    // Set the border width of the window.
    uint32_t values[] = {cfg_border_size};
    xcb_configure_window(xcb, evt->window, XCB_CONFIG_WINDOW_BORDER_WIDTH,
                         values);

    // Add the window to the list of managed windows.
    Window *win = mg_add_window(evt->window);
    if (!win) {
        return;
    }

    // Map the window.
    xcb_map_window(xcb, evt->window);
    xcb_flush(xcb);
    mg_focus_window(win);
    if (WIN_IS_TILED(win)) {
        mg_layout();
    }
}

// Handle a property notify event.
static void evt_property_notify(xcb_property_notify_event_t *evt) {
    if (evt->state == XCB_PROPERTY_DELETE) {
        return;
    }
    Window *win = winlist_find(evt->window);
    if (!win) {
        return;
    }
    if (evt->atom == atoms[ATOM_WM_NORMAL_HINTS]) {
        mg_update_size_hints(win);
    } else if (evt->atom == atoms[ATOM_NET_WM_WINDOW_TYPE]) {
        mg_update_type(win);
    } else if (evt->atom == atoms[ATOM_WM_TRANSIENT_FOR]) {
        int was_floating = WIN_IS_FLOATING(win);
        win->flags |= WIN_FLOATING;
        if (!was_floating) {
            mg_resize_window(win, screen_width / 2 - win->w / 2,
                             screen_height / 2 - win->h / 2, win->w, win->h);
            mg_layout();
        }
    }
}

// Handle an unmapping notify event.
static void evt_unmap_notify(xcb_unmap_notify_event_t *evt) {
    mg_del_window(evt->window);
    mg_layout();
}

// Updates the _NET_CLIENT_LIST property of the root window.
static void ewmh_update_client_list() {
    if (winlist == NULL) {
        xcb_delete_property_checked(xcb, screen->root, ATOM_NET_CLIENT_LIST);
        xcb_flush(xcb);
        return;
    }
    int wincount = winlist_count(NULL);

    // Don't allocate too much. Although if 1024 managed windows are open
    // then that is the bigger issue at hand.
    if (wincount > 1024) {
        printf("Too many windows for updating client list\n");
        return;
    }

    // Get a list of open windows.
    Window *win = winlist;
    xcb_window_t list[wincount];
    for (int i = 0; i < wincount; i++) {
        list[i] = win->win;
        win = win->next;
    }
    xcb_change_property(xcb, XCB_PROP_MODE_REPLACE, screen->root,
                        atoms[ATOM_NET_CLIENT_LIST], XCB_ATOM_WINDOW, 32,
                        wincount, list);
}

// Closes the focused window.
// No cleanup needs to happen in this function, as the DestroyNotify event
// handler should take care of everything.
static void func_close() {
    // Do nothing if there are no windows.
    if (!focused) {
        return;
    }
    mg_close_window(focused->win);
}

// Switches focus to the next window (if any.)
static void func_focus_next() {
    Window *win;
    if (focused->next) {
        win = focused->next;
    } else {
        win = winlist;
    }
    if (win) {
        mg_focus_window(win);
    }
}

// Switches focus to the previous window (if any.)
static void func_focus_prev() {
    Window *win;
    if (focused->prev) {
        win = focused->prev;
    } else {
        win = winlist_last();
    }
    if (win) {
        mg_focus_window(win);
    }
}

// Toggles a window's fullscreen state.
static void func_make_fullscreen() {
    if (!focused) {
        return;
    }
    focused->flags ^= WIN_FULLSCREEN;
    if (WIN_IS_FULLSCREEN(focused)) {
        int width = (focused->maxw != 0 ? focused->maxw : screen_width);
        int height = (focused->maxh != 0 ? focused->maxh : screen_height);
        mg_resize_window(focused, 0, 0, width, height);
        uint32_t value_list[] = {0};
        xcb_configure_window(xcb, focused->win, XCB_CONFIG_WINDOW_BORDER_WIDTH,
                             value_list);
        xcb_flush(xcb);
    } else {
        uint32_t value_list[] = {cfg_border_size};
        xcb_configure_window(xcb, focused->win, XCB_CONFIG_WINDOW_BORDER_WIDTH,
                             value_list);
        xcb_flush(xcb);
    }
    mg_layout();
}

// Restores a window to tiling state.
static void func_make_tiling() {
    if (!focused) {
        return;
    }
    focused->flags &= ~WIN_FLOATING;
    mg_layout();
}

// Increases the width of the master window.
static void func_master_inc() {
    if (master_scale >= 0.8) {
        return;
    }
    master_scale += 0.05;
    mg_layout();
}

// Decreases the width of the master window.
static void func_master_dec() {
    if (master_scale <= 0.2) {
        return;
    }
    master_scale -= 0.05;
    mg_layout();
}

// Moves the focused window down the stack.
static void func_move_stack_up() {
    if (!focused || !WIN_IS_TILED(focused)) {
        return;
    }

    // Find the next tiled window to swap places with.
    Window *win = focused->next;
    while (1) {
        if (!win) {
            win = winlist;
        }
        if (win == focused) {
            return;
        }
        if (WIN_IS_TILED(win)) {
            winlist_swap(win, focused);
            mg_layout();
            return;
        }
        win = win->next;
    }
}

// Moves the focused window up the stack.
static void func_move_stack_down() {
    if (!focused || !WIN_IS_TILED(focused)) {
        return;
    }
    Window *win = focused->prev;
    while (1) {
        if (!win) {
            win = winlist_last();
        }
        if (win == focused) {
            return;
        }
        if (WIN_IS_TILED(win)) {
            winlist_swap(win, focused);
            mg_layout();
            return;
        }
        win = win->prev;
    }
}

// Closes the X connection and restarts winman with exec.
static void func_restart() {
    char buf[1024];
    ssize_t read = readlink("/proc/self/exe", buf, sizeof(buf));
    if (read == -1) {
        fprintf(stderr, "readlink err: %s\n", strerror(errno));
        return;
    }
    buf[read] = 0;
    mg_fini();
    printf("Restarting!\n");
    execvp(buf, args);
    fprintf(stderr, "restart: execvp failed\n");
    die(strerror(errno));
}

// Spawns a terminal.
static void func_spawn_terminal() {
    SPAWN(cfg_terminal);
}

// Quits winman.
static void func_quit() {
    please_quit = 1;
}

// Adds a window to the list of managed windows.
static Window *mg_add_window(xcb_window_t win) {
    // Add the window.
    xcb_get_geometry_cookie_t cookie = xcb_get_geometry(xcb, win);
    xcb_generic_error_t *err;
    xcb_get_geometry_reply_t *reply = xcb_get_geometry_reply(xcb, cookie, &err);
    if (err) {
        fprintf(stderr, "Geometry failed in add_window\n");
        return NULL;
    }
    Window w = {
        .x = reply->x,
        .y = reply->y,
        .w = reply->width,
        .h = reply->height,
        .win = win,
    };
    free(reply);
    mg_grab_buttons(&w, 0);
    Window *window = winlist_add(w);
    ewmh_update_client_list();

    // Check the window's properties.
    mg_update_type(window);
    mg_update_size_hints(window);
    xcb_get_property_cookie_t propcookie =
        xcb_get_property(xcb, 0, win, atoms[ATOM_WM_TRANSIENT_FOR],
                         XCB_ATOM_WINDOW, 0, UINT32_MAX);
    xcb_get_property_reply_t *propreply =
        xcb_get_property_reply(xcb, propcookie, &err);
    if (!err) {
        if (propreply->format != 0) {
            window->flags |= WIN_FLOATING;
        }
        free(propreply);
    }
    if (WIN_IS_FLOATING(window)) {
        // Center floating window.
        mg_resize_window(window, screen_width / 2 - window->w / 2,
                         screen_height / 2 - window->h / 2, window->w,
                         window->h);
    }

    // Apply any applicable configuration rules.
    char *name = get_string_property(win, ATOM_WM_NAME);
    if (!name) {
        return window;
    }
    char *class = get_string_property(win, ATOM_WM_CLASS);
    if (!class) {
        free(name);
        return window;
    }
    for (int i = 0; i < ARRAY_LENGTH(cfg_rules); i++) {
        if (cfg_rules[i].name && strstr(name, cfg_rules[i].name)) {
            window->flags = cfg_rules[i].flags;
        }
        if (cfg_rules[i].class && strstr(class, cfg_rules[i].class)) {
            window->flags = cfg_rules[i].flags;
        }
    }
    free(name);
    free(class);

    return window;
}

// Closes the given window.
static void mg_close_window(xcb_window_t win) {
    // Try to send a DELETE_WINDOW message. If the client window does not
    // support it, kill the client.
    if (is_protocol_supported(win, atoms[ATOM_DELETE_WINDOW])) {
        xcb_client_message_event_t evt = {
            .response_type = XCB_CLIENT_MESSAGE,
            .format = 32,
            .sequence = 0,
            .window = win,
            .type = atoms[ATOM_WM_PROTOCOLS],
            .data = {{
                atoms[ATOM_DELETE_WINDOW],
                XCB_CURRENT_TIME,
            }},
        };
        xcb_send_event_checked(xcb, 0, win, XCB_EVENT_MASK_NO_EVENT,
                               (char *)&evt);
        xcb_flush(xcb);
    } else {
        xcb_kill_client_checked(xcb, win);
        xcb_flush(xcb);
    }
}

// Deletes a window from the list of managed windows.
static void mg_del_window(xcb_window_t wid) {
    Window *win = winlist_find(wid);
    if (!win) {
        return;
    }
    int was_focused = win == focused;

    // Ungrabbing the button will fail if the window was deleted. Send a
    // checked request so we don't get an unhandled error.
    xcb_ungrab_button_checked(xcb, XCB_BUTTON_INDEX_ANY, win->win,
                              XCB_MOD_MASK_ANY);
    xcb_flush(xcb);

    // Delete the window from the list of managed windows.
    winlist_del(win);
    ewmh_update_client_list();

    // Change focus if necessary.
    if (!was_focused) {
        return;
    }
    focused = NULL;
    Window *last = winlist_last();
    if (!last) {
        return;
    }
    mg_focus_window(last);
}

// Cleans up resources allocated by winman.
static void mg_fini() {
    for (int i = 0; i < CURSOR_COUNT; i++) {
        if (cursors[i] != 0) {
            xcb_free_cursor(xcb, cursors[i]);
        }
    }
    if (xcb) {
        xcb_disconnect(xcb);
    }
}

// Transfers focus to the given window.
static void mg_focus_window(Window *win) {
    // Do nothing if the focused window will not change.
    if (focused && win == focused) {
        return;
    }

    // Switch the mouse button grabs and border color of the previously
    // focused window.
    uint32_t values[1];
    if (focused) {
        mg_grab_buttons(focused, 0);
        values[0] = colors[BorderInactive];
        xcb_change_window_attributes(xcb, focused->win, XCB_CW_BORDER_PIXEL,
                                     values);
    }

    // Switch focus to the given window.
    focused = win;
    xcb_set_input_focus(xcb, XCB_INPUT_FOCUS_PARENT, win->win,
                        XCB_CURRENT_TIME);
    values[0] = XCB_STACK_MODE_ABOVE;
    xcb_configure_window(xcb, win->win, XCB_CONFIG_WINDOW_STACK_MODE, values);
    values[0] = colors[BorderActive];
    xcb_change_window_attributes(xcb, win->win, XCB_CW_BORDER_PIXEL, values);
    mg_grab_buttons(win, 1);
    xcb_flush(xcb);

    // Send a WM_TAKE_FOCUS message.
    xcb_client_message_event_t evt = {
        .response_type = XCB_CLIENT_MESSAGE,
        .format = 32,
        .sequence = 0,
        .window = win->win,
        .type = atoms[ATOM_WM_PROTOCOLS],
        .data = {{
            atoms[ATOM_WM_TAKE_FOCUS],
            XCB_CURRENT_TIME,
        }},
    };
    xcb_send_event_checked(xcb, 0, win->win, XCB_EVENT_MASK_NO_EVENT,
                           (char *)&evt);
    xcb_flush(xcb);

    // Set the EWMH _NET_ACTIVE_WINDOW property.
    xcb_change_property(xcb, XCB_PROP_MODE_REPLACE, screen->root,
                        atoms[ATOM_NET_ACTIVE_WINDOW], XCB_ATOM_WINDOW, 32, 1,
                        &focused->win);
}

// Grabs mouse buttons from a window.
static void mg_grab_buttons(Window *win, int focus) {
    // Release any old button grabs.
    xcb_ungrab_button(xcb, XCB_BUTTON_INDEX_ANY, win->win, XCB_MOD_MASK_ANY);

    // If the window is focused, only grab the normal mouse binds as defined
    // in config.h. Otherwise, grab everything.
    if (focus) {
        for (int i = 0; i < ARRAY_LENGTH(cfg_mousebinds); i++) {
            if (cfg_mousebinds[i].loc == LocWin) {
                xcb_grab_button(
                    xcb, 0, win->win, BUTTON_MASK, XCB_GRAB_MODE_ASYNC,
                    XCB_GRAB_MODE_ASYNC, screen->root, XCB_CURSOR_NONE,
                    cfg_mousebinds[i].button, cfg_mousebinds[i].mod);
            }
        }
    } else {
        xcb_grab_button(xcb, 0, win->win, BUTTON_MASK, XCB_GRAB_MODE_ASYNC,
                        XCB_GRAB_MODE_ASYNC, screen->root, XCB_CURSOR_NONE,
                        XCB_BUTTON_INDEX_ANY, XCB_MOD_MASK_ANY);
    }
}

// Grabs any necessary keys.
static void mg_grab_keys() {
    // Ungrab all keys.
    xcb_ungrab_key(xcb, XCB_GRAB_ANY, screen->root, XCB_MOD_MASK_ANY);

    // Grab keys from config.
    for (int i = 0; i < ARRAY_LENGTH(cfg_keybinds); i++) {
        xcb_grab_key(xcb, 1, screen->root, cfg_keybinds[i].mod,
                     cfg_keybinds[i].sym, XCB_GRAB_MODE_ASYNC,
                     XCB_GRAB_MODE_ASYNC);
    }
    xcb_flush(xcb);
}

// Processes the next event in the queue from the X server.
static int mg_handle_event() {
    xcb_generic_event_t *evt = xcb_wait_for_event(xcb);
    if (!evt || evt->response_type == 0) {
        if (xcb_connection_has_error(xcb)) {
            fprintf(stderr, "X connection errored (closed?)\n");
            return 1;
        }
        fprintf(stderr, "Unhandled X error\n");
        return 0;
    }

    switch (evt->response_type & ~0x80) {
    case XCB_BUTTON_PRESS:
        evt_button_press((xcb_button_press_event_t *)evt);
        break;
    case XCB_CLIENT_MESSAGE:
        evt_client_message((xcb_client_message_event_t *)evt);
        break;
    case XCB_CONFIGURE_REQUEST:
        evt_config_request((xcb_configure_request_event_t *)evt);
        break;
    case XCB_DESTROY_NOTIFY:
        evt_destroy_notify((xcb_destroy_notify_event_t *)evt);
        break;
    case XCB_KEY_PRESS:
        evt_key_press((xcb_key_press_event_t *)evt);
        break;
    case XCB_MAPPING_NOTIFY:
        evt_mapping_notify((xcb_mapping_notify_event_t *)evt);
        break;
    case XCB_MAP_REQUEST:
        evt_map_request((xcb_map_request_event_t *)evt);
        break;
    case XCB_PROPERTY_NOTIFY:
        evt_property_notify((xcb_property_notify_event_t *)evt);
        break;
    case XCB_UNMAP_NOTIFY:
        evt_unmap_notify((xcb_unmap_notify_event_t *)evt);
        break;
    }
    free(evt);
    return 0;
}

// Perform various initialization actions (grabbing keys,
// substructure redirection, etc)
static void mg_init() {
    // Get the necessary cursors (left pointer, move, resize)
    xcb_cursor_context_t *ctx;
    if (xcb_cursor_context_new(xcb, screen, &ctx) != 0) {
        die("Failed to create cursor context");
    }
    cursors[CursorNormal] = xcb_cursor_load_cursor(ctx, "left_ptr");
    cursors[CursorMove] = xcb_cursor_load_cursor(ctx, "move");
    cursors[CursorResize] = xcb_cursor_load_cursor(ctx, "size_all");
    xcb_cursor_context_free(ctx);

    // Set the substructure redirect mask and cursor on the root window.
    int value_list[] = {XCB_EVENT_MASK_SUBSTRUCTURE_REDIRECT |
                            XCB_EVENT_MASK_SUBSTRUCTURE_NOTIFY |
                            XCB_EVENT_MASK_STRUCTURE_NOTIFY |
                            XCB_EVENT_MASK_PROPERTY_CHANGE,
                        cursors[CursorNormal]};
    xcb_void_cookie_t cookie = xcb_change_window_attributes_checked(
        xcb, screen->root, XCB_CW_EVENT_MASK | XCB_CW_CURSOR, value_list);
    xcb_generic_error_t *error = xcb_request_check(xcb, cookie);
    if (error != NULL) {
        print_xcb_error(error);
        die("Failed to get substructure redirect");
    }

    // Convert the keysym of each keybind to keycodes.
    for (int i = 0; i < ARRAY_LENGTH(cfg_keybinds); i++) {
        xcb_keycode_t code = get_keycode(cfg_keybinds[i].sym);
        if (code == 0) {
            die("Failed to convert keysym to keycode");
        }
        cfg_keybinds[i].sym = code;
    }

    // Get the necessary atoms.
    for (int i = 0; i < ARRAY_LENGTH(atom_names); i++) {
        xcb_intern_atom_cookie_t cookie =
            xcb_intern_atom(xcb, 0, strlen(atom_names[i]), atom_names[i]);
        xcb_generic_error_t *err;
        xcb_intern_atom_reply_t *reply =
            xcb_intern_atom_reply(xcb, cookie, &err);
        if (err) {
            die("Failed to get atoms");
        }
        atoms[i] = reply->atom;
        free(reply);
    }

    // Create colors.
    unsigned int r, g, b;
    xcb_generic_error_t *err;
    for (int i = 0; i < COLOR_COUNT; i++) {
        parse_rgb(cfg_colorscheme[i], &r, &g, &b);
        xcb_alloc_color_reply_t *reply =
            xcb_alloc_color_reply(xcb,
                                  xcb_alloc_color(xcb, screen->default_colormap,
                                                  r * 256, g * 256, b * 256),
                                  &err);
        if (err) {
            die("Failed to allocate color");
        }
        colors[i] = reply->pixel;
        free(reply);
    }
    for (int i = 0; i < TERMCOLOR_COUNT; i++) {
        parse_rgb(cfg_termcolors[i], &r, &g, &b);
        xcb_alloc_color_reply_t *reply = xcb_alloc_color_reply(
            xcb, xcb_alloc_color(xcb, screen->default_colormap, r, g, b), &err);
        if (err) {
            die("Failed to allocate color");
        }
        termcolors[i] = reply->pixel;
        free(reply);
    }

    // Scan for any already-present windows. This is only necessary after
    // a restart.
    xcb_query_tree_cookie_t treecookie = xcb_query_tree(xcb, screen->root);
    xcb_query_tree_reply_t *tree = xcb_query_tree_reply(xcb, treecookie, &err);
    if (err) {
        die("Failed to scan root window children");
    }
    xcb_window_t *children = xcb_query_tree_children(tree);
    for (int i = 0; i < xcb_query_tree_children_length(tree); i++) {
        xcb_window_t win = children[i];
        xcb_get_window_attributes_cookie_t attribcookie =
            xcb_get_window_attributes(xcb, win);
        xcb_get_window_attributes_reply_t *attrib =
            xcb_get_window_attributes_reply(xcb, attribcookie, &err);
        if (err) {
            die("Failed to get window attributes when scanning");
        }
        if (attrib->map_state == XCB_MAP_STATE_VIEWABLE &&
            !attrib->override_redirect) {
            Window *w = mg_add_window(win);
            if (w) {
                mg_focus_window(w);
            }
        }
        free(attrib);
    }
    free(tree);

    // Create the EWMH check window.
    ewmh_check_win = xcb_generate_id(xcb);
    xcb_create_window_checked(
        xcb, XCB_COPY_FROM_PARENT, ewmh_check_win, screen->root, 0, 0, 1, 1, 0,
        XCB_WINDOW_CLASS_INPUT_ONLY, screen->root_visual, 0, NULL);
    xcb_change_property(xcb, XCB_PROP_MODE_REPLACE, ewmh_check_win,
                        atoms[ATOM_NET_SUPPORTING_WM_CHECK], XCB_ATOM_WINDOW,
                        32, 1, &ewmh_check_win);
    xcb_change_property(xcb, XCB_PROP_MODE_REPLACE, ewmh_check_win,
                        atoms[ATOM_NET_WM_NAME], atoms[ATOM_UTF8_STRING], 8,
                        strlen(WM_NAME), WM_NAME);
    xcb_change_property(xcb, XCB_PROP_MODE_REPLACE, screen->root,
                        atoms[ATOM_NET_SUPPORTING_WM_CHECK], XCB_ATOM_WINDOW,
                        32, 1, &ewmh_check_win);

    // Set the _NET_SUPPORTED EWMH property.
    xcb_atom_t net_atoms[] = {
        atoms[ATOM_NET_ACTIVE_WINDOW],
        atoms[ATOM_NET_CLIENT_LIST],
        atoms[ATOM_NET_WM_WINDOW_TYPE],
        atoms[ATOM_NET_WM_WINDOW_TYPE_DIALOG],
    };
    xcb_change_property(xcb, XCB_PROP_MODE_REPLACE, screen->root,
                        atoms[ATOM_NET_SUPPORTED], XCB_ATOM_ATOM, 32,
                        ARRAY_LENGTH(net_atoms), net_atoms);
    xcb_flush(xcb);

    // Grab keybinds.
    mg_grab_keys();
}

// Moves all tiled windows to the correct locations.
static void mg_layout() {
    // Get the amount of tiled windows.
    int win_count = winlist_count(comp_tiled);
    if (win_count == 0) {
        return;
    }

    // If there is only one tiled window, give it the entire screen.
    int master_width = screen_width * master_scale;
    if (win_count == 1) {
        Window *win = winlist_get(NULL, comp_tiled);
        mg_resize_padded(win, 0, 0, screen_width, screen_height, GAP_FULL,
                         GAP_FULL, GAP_FULL, GAP_FULL);
        return;
    }

    // Move the first tiled window to the master area.
    Window *win = winlist_get(NULL, comp_tiled);
    mg_resize_padded(win, 0, 0, master_width, screen_height, GAP_FULL, GAP_FULL,
                     GAP_HALF, GAP_FULL);

    // Move the rest of the tiled windows to the stacking area.
    int window_height = screen_height / (win_count - 1);
    for (int i = 0; i < win_count - 1; i++) {
        win = winlist_get(win->next, comp_tiled);
        char gap_a = GAP_HALF;
        char gap_b = GAP_HALF;
        if (i == 0) {
            gap_a = GAP_FULL;
            if (win_count <= 2) {
                gap_b = GAP_FULL;
            }
        } else if (i == win_count - 2) {
            gap_b = GAP_FULL;
        }
        mg_resize_padded(win, master_width, window_height * i,
                         screen_width - master_width, window_height, GAP_HALF,
                         gap_a, GAP_FULL, gap_b);
    }
}

// Resizes the window with padding around the edges for gaps.
static void mg_resize_padded(Window *win, uint16_t x, uint16_t y, uint16_t w,
                             uint16_t h, char pad_left, char pad_top,
                             char pad_right, char pad_bottom) {
    x -= cfg_border_size / 2 + 1;
    y -= cfg_border_size / 2 + 1;
    switch (pad_left) {
    case GAP_FULL:
        x += cfg_gap_size;
        w -= cfg_gap_size;
        break;
    case GAP_HALF:
        x += cfg_gap_size / 2;
        w -= cfg_gap_size / 2;
        break;
    }
    switch (pad_top) {
    case GAP_FULL:
        y += cfg_gap_size;
        h -= cfg_gap_size;
        break;
    case GAP_HALF:
        y += cfg_gap_size / 2;
        h -= cfg_gap_size / 2;
        break;
    }
    switch (pad_right) {
    case GAP_FULL:
        w -= cfg_gap_size;
        break;
    case GAP_HALF:
        w -= cfg_gap_size / 2;
        break;
    }
    switch (pad_bottom) {
    case GAP_FULL:
        h -= cfg_gap_size;
        break;
    case GAP_HALF:
        h -= cfg_gap_size / 2;
        break;
    }
    mg_resize_window(win, x, y, w, h);
}

// Resizes the given window to the given bounds.
static void mg_resize_window(Window *win, uint16_t x, uint16_t y, uint16_t w,
                             uint16_t h) {
    uint32_t values[] = {x, y, w, h};
    xcb_configure_window(xcb, win->win, CONFIG_MASK, values);
    xcb_flush(xcb);
    win->x = x;
    win->y = y;
    win->w = w;
    win->h = h;
}

// Forks the process and runs the given command.
static void mg_spawn(const char *cmd, const char *argv[]) {
    if (fork() == 0) {
        // Close the X connection's file descriptor if it exists.
        if (xcb) {
            close(xcb_get_file_descriptor(xcb));
        }
        setsid();
        execvp(cmd, (char **)argv);
        fprintf(stderr, "spawn: execvp (program %s) failed\n", cmd);
        exit(0);
    }
}

// Handle any updates to a window's WM_NORMAL_HINTS property.
static void mg_update_size_hints(Window *win) {
    xcb_get_property_cookie_t cookie =
        xcb_get_property(xcb, 0, win->win, atoms[ATOM_WM_NORMAL_HINTS],
                         XCB_ATOM_WM_SIZE_HINTS, 0, UINT32_MAX);
    xcb_generic_error_t *err;
    xcb_get_property_reply_t *reply = xcb_get_property_reply(xcb, cookie, &err);
    if (err) {
        return;
    }
    SizeHints *hints = xcb_get_property_value(reply);
    if (hints->flags & 16) {
        win->minw = hints->min_width;
        win->minh = hints->min_height;
    }
    if (hints->flags & 32) {
        win->maxw = hints->max_width;
        win->maxh = hints->max_height;
    }
    free(reply);
}

// Handle any updates to a window's _NET_WM_WINDOW_TYPE property.
static void mg_update_type(Window *win) {
    // Make the window floating if it is a dialog.
    xcb_get_property_cookie_t cookie =
        xcb_get_property(xcb, 0, win->win, atoms[ATOM_NET_WM_WINDOW_TYPE],
                         XCB_ATOM_ATOM, 0, UINT32_MAX);
    xcb_generic_error_t *err;
    xcb_get_property_reply_t *reply = xcb_get_property_reply(xcb, cookie, &err);
    if (err) {
        fprintf(stderr, "Couldn't get _NET_WM_WINDOW_TYPE on new window\n");
        return;
    }
    for (int i = 0; i < xcb_get_property_value_length(reply); i++) {
        xcb_atom_t *atom = xcb_get_property_value(reply);
        if (*atom == atoms[ATOM_NET_WM_WINDOW_TYPE_DIALOG]) {
            win->flags |= WIN_FLOATING;
        }
    }
    free(reply);
}

// Functions as a stand-in event loop while the mouse pointer is grabbed.
static void mouse_handle_events(Window *win,
                                void (*func)(Window *, int16_t, int16_t)) {
    xcb_configure_request_event_t *config;
    xcb_motion_notify_event_t *motion;

    // Get the current pointer location.
    xcb_query_pointer_cookie_t cookie = xcb_query_pointer(xcb, screen->root);
    xcb_generic_error_t *err;
    xcb_query_pointer_reply_t *reply =
        xcb_query_pointer_reply(xcb, cookie, &err);
    if (err) {
        fprintf(stderr, "mouse_handle_events: Failed to query pointer\n");
        return;
    }
    mouse_x = reply->root_x;
    mouse_y = reply->root_y;
    free(reply);

    // Start processing events.
    while (1) {
        xcb_generic_event_t *evt = xcb_wait_for_event(xcb);
        if (!evt || evt->response_type == 0) {
            if (xcb_connection_has_error(xcb)) {
                fprintf(stderr, "X connection errored (closed?)\n");
                return;
            }
            fprintf(stderr, "Unhandled X error\n");
            continue;
        }

        switch (evt->response_type & ~0x80) {
        case XCB_BUTTON_RELEASE:
            free(evt);
            return;
        case XCB_CLIENT_MESSAGE:
            evt_client_message((xcb_client_message_event_t *)evt);
            break;
        case XCB_CONFIGURE_REQUEST:
            config = (xcb_configure_request_event_t *)evt;
            if (config->window != win->win) {
                evt_config_request(config);
            }
            break;
        case XCB_DESTROY_NOTIFY:
            evt_destroy_notify((xcb_destroy_notify_event_t *)evt);
            break;
        case XCB_MAPPING_NOTIFY:
            evt_mapping_notify((xcb_mapping_notify_event_t *)evt);
            break;
        case XCB_MAP_REQUEST:
            evt_map_request((xcb_map_request_event_t *)evt);
            break;
        case XCB_MOTION_NOTIFY:
            motion = (xcb_motion_notify_event_t *)evt;
            func(win, motion->root_x, motion->root_y);
            mouse_x = motion->root_x;
            mouse_y = motion->root_y;
            break;
        case XCB_PROPERTY_NOTIFY:
            evt_property_notify((xcb_property_notify_event_t *)evt);
            break;
        case XCB_UNMAP_NOTIFY:
            evt_unmap_notify((xcb_unmap_notify_event_t *)evt);
            break;
        }
        free(evt);
    }
}

// Moves the window being clicked on by the mouse.
static void mouse_move(Window *win) {
    // Make the window floating.
    int was_floating = WIN_IS_FLOATING(win);
    win->flags |= WIN_FLOATING;
    if (!was_floating) {
        mg_layout();
    }

    // Grab the pointer and start the mouse event handler.
    xcb_grab_pointer(xcb, 0, screen->root, MOTION_MASK, XCB_GRAB_MODE_ASYNC,
                     XCB_GRAB_MODE_ASYNC, screen->root, cursors[CursorMove],
                     XCB_CURRENT_TIME);
    xcb_flush(xcb);
    mouse_handle_events(win, mouse_move_loop);
    xcb_ungrab_pointer(xcb, XCB_CURRENT_TIME);
    xcb_flush(xcb);
}

static void mouse_move_loop(Window *win, int16_t x, int16_t y) {
    mg_resize_window(win, win->x + (x - mouse_x), win->y + (y - mouse_y),
                     win->w, win->h);
}

// Resizes the window being clicked on by the mouse.
static void mouse_resize(Window *win) {
    // Do nothing if the window is tiled.
    // TODO: Allow for resizing master/stack widths once that is implemented
    if (WIN_IS_TILED(win)) {
        return;
    }

    // Grab the pointer and start the mouse event handler.
    xcb_warp_pointer(xcb, XCB_NONE, win->win, 0, 0, 0, 0, win->w, win->h);
    xcb_grab_pointer(xcb, 0, screen->root, MOTION_MASK, XCB_GRAB_MODE_ASYNC,
                     XCB_GRAB_MODE_ASYNC, screen->root, cursors[CursorResize],
                     XCB_CURRENT_TIME);
    xcb_flush(xcb);
    mouse_handle_events(win, mouse_resize_loop);
    xcb_ungrab_pointer(xcb, XCB_CURRENT_TIME);
    xcb_flush(xcb);
}

static void mouse_resize_loop(Window *win, int16_t x, int16_t y) {
    int w = x - win->x;
    int h = y - win->y;
    if (win->minw && w < win->minw) {
        w = win->minw;
    }
    if (win->maxw && w > win->maxw) {
        w = win->maxw;
    }
    if (win->minh && h < win->minh) {
        h = win->minh;
    }
    if (win->maxh && h > win->maxh) {
        h = win->maxh;
    }
    w = MAX(w, 16);
    h = MAX(h, 16);
    mg_resize_window(win, win->x, win->y, w, h);
}

// Adds the given window to the list of managed windows.
static Window *winlist_add(Window win) {
    // If this is the first managed window, set it as the head of the list.
    Window *current = winlist;
    if (!current) {
        Window *ptr = malloc(sizeof(Window));
        if (!ptr) {
            die("malloc");
        }
        *ptr = win;
        winlist = ptr;
        return ptr;
    }

    // Otherwise, find the tail of the list and add the window as the next
    // element.
    while (current->next) {
        current = current->next;
    }
    Window *ptr = malloc(sizeof(Window));
    if (!ptr) {
        die("malloc");
    }
    win.prev = current;
    *ptr = win;
    current->next = ptr;
    return ptr;
}

// Returns the number of windows in the list. If given a comparator, only
// counts windows for which the comparator returns a non-zero value.
static int winlist_count(int (*comparator)(Window *)) {
    if (!winlist) {
        return 0;
    }
    int count = 0;
    Window *win = winlist;
    while (win) {
        if (comparator) {
            if (comparator(win)) {
                count++;
            }
        } else {
            count++;
        }
        win = win->next;
    }
    return count;
}

// Deletes the given window from the list of managed windows.
// Does not change the focused window.
static void winlist_del(Window *win) {
    // Check if the window to delete is the beginning of the list.
    if (winlist == win) {
        // If the window to delete is the only one in the list, then
        // delete the list.
        if (!winlist->next) {
            free(winlist);
            winlist = NULL;
            return;
        }

        // Make the 2nd element the new head of the list.
        Window *old_winlist = winlist;
        winlist->next->prev = NULL;
        winlist = winlist->next;
        free(old_winlist);
        return;
    }
    Window *prev = win->prev;
    Window *next = win->next;
    prev->next = next;
    if (next) {
        next->prev = prev;
    }
    free(win);
}

// Finds the window with the given ID in the list.
static Window *winlist_find(xcb_window_t win) {
    Window *current = winlist;
    if (current == NULL) {
        return NULL;
    }
    if (current->win == win) {
        return winlist;
    }
    while (current->next) {
        current = current->next;
        if (current->win == win) {
            return current;
        }
    }
    return NULL;
}

// Returns the first window after the given window (if any) that satisfies
// the given comparator.
static Window *winlist_get(Window *win, int (*comparator)(Window *)) {
    if (win == NULL) {
        win = winlist;
    }
    while (win) {
        if (comparator(win)) {
            return win;
        }
        win = win->next;
    }
    return NULL;
}

// Gets the last window in the list.
static Window *winlist_last() {
    Window *current = winlist;
    if (winlist == NULL) {
        return NULL;
    }
    while (current->next) {
        current = current->next;
    }
    return current;
}

// Swaps the locations of the given windows in the list.
static void winlist_swap(Window *a, Window *b) {
    Window c = *a;
    *a = *b;
    a->next = c.next;
    a->prev = c.prev;
    c.next = b->next;
    c.prev = b->prev;
    *b = c;
    if (a == focused) {
        focused = b;
    } else if (b == focused) {
        focused = a;
    }
}

int main(int argc, char **argv) {
    if (argc != 1) {
        fprintf(stderr, "winman - X window manager");
        return 1;
    }
    args = argv;

    // Connect to the X server.
    int scrnum;
    xcb = xcb_connect(NULL, &scrnum);
    if (xcb_connection_has_error(xcb)) {
        die("X connection failed");
    }

    // Get the default screen and use it.
    const xcb_setup_t *setup = xcb_get_setup(xcb);
    xcb_screen_iterator_t iter = xcb_setup_roots_iterator(setup);
    for (int i = 0; i < scrnum; i++) {
        xcb_screen_next(&iter);
    }
    screen = iter.data;
    screen_width = screen->width_in_pixels;
    screen_height = screen->height_in_pixels;
    printf("WxH: %i x %i\n", screen_width, screen_height);

    // Perform setup.
    mg_init();

    // Handle events.
    while (1) {
        int code = mg_handle_event();
        if (code > 0) {
            mg_fini();
            return code;
        }
        if (please_quit) {
            break;
        }
    }

    // Cleanup and exit.
    mg_fini();
    printf("Exiting\n");
    return 0;
}
