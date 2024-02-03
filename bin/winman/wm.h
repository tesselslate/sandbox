#ifndef __WM_H_GUARD

#define __WM_H_GUARD

#include <stdint.h>
#include <xcb/xcb.h>

#define WIN_FLOATING (1 << 0)
#define WIN_FULLSCREEN (1 << 1)

typedef enum {
    ATOM_DELETE_WINDOW,
    ATOM_NET_ACTIVE_WINDOW,
    ATOM_NET_CLIENT_LIST,
    ATOM_NET_CLOSE_WINDOW,
    ATOM_NET_SUPPORTED,
    ATOM_NET_SUPPORTING_WM_CHECK,
    ATOM_NET_WM_NAME,
    ATOM_NET_WM_WINDOW_TYPE,
    ATOM_NET_WM_WINDOW_TYPE_DIALOG,
    ATOM_UTF8_STRING,
    ATOM_WM_CLASS,
    ATOM_WM_NAME,
    ATOM_WM_NORMAL_HINTS,
    ATOM_WM_PROTOCOLS,
    ATOM_WM_TAKE_FOCUS,
    ATOM_WM_TRANSIENT_FOR,
    ATOM_COUNT
} Atom;

typedef enum { LocTag, LocWin } ButtonLocation;

typedef enum { BorderActive, BorderInactive, COLOR_COUNT } Color;

typedef enum { CursorNormal, CursorMove, CursorResize, CURSOR_COUNT } Cursor;

typedef struct {
    uint32_t flags;
    uint32_t _pad[4];
    int32_t min_width;
    int32_t min_height;
    int32_t max_width;
    int32_t max_height;
    int32_t width_inc;
    int32_t height_inc;
    int32_t min_aspect;
    int32_t max_aspect;
    int32_t base_width;
    int32_t base_height;
    int32_t win_gravity;
} SizeHints;

struct Window {
    xcb_window_t win;
    int16_t x, y, w, h;
    int16_t flags;
    int16_t minw, maxw, minh, maxh;

    struct Window *prev;
    struct Window *next;
};

typedef struct Window Window;

typedef struct {
    ButtonLocation loc;
    uint16_t mod;
    xcb_button_t button;
    void (*func)(Window *);
} Button;

typedef struct {
    uint16_t mod;
    xcb_keysym_t sym;
    void (*func)();
} Key;

typedef struct {
    const char *name;
    const char *class;
    int16_t flags;
} Rule;

static void die(const char *text);
static xcb_keycode_t get_keycode(xcb_keysym_t sym);
static char *get_string_property(xcb_window_t win, Atom property);
static int is_protocol_supported(xcb_window_t win, xcb_atom_t protocol);
static void parse_rgb(const char *rgb, unsigned int *r, unsigned int *g,
                      unsigned int *b);
static void print_xcb_error(xcb_generic_error_t *err);

static int comp_tiled(Window *win);

static void evt_button_press(xcb_button_press_event_t *evt);
static void evt_client_message(xcb_client_message_event_t *evt);
static void evt_config_request(xcb_configure_request_event_t *evt);
static void evt_destroy_notify(xcb_destroy_notify_event_t *evt);
static void evt_key_press(xcb_key_press_event_t *evt);
static void evt_mapping_notify(xcb_mapping_notify_event_t *evt);
static void evt_map_request(xcb_map_request_event_t *evt);
static void evt_property_notify(xcb_property_notify_event_t *evt);
static void evt_unmap_notify(xcb_unmap_notify_event_t *evt);

static void ewmh_update_client_list();

static void func_close();
static void func_focus_next();
static void func_focus_prev();
static void func_make_fullscreen();
static void func_make_tiling();
static void func_master_inc();
static void func_master_dec();
static void func_move_stack_up();
static void func_move_stack_down();
static void func_restart();
static void func_spawn_terminal();
static void func_quit();

static Window *mg_add_window(xcb_window_t win);
static void mg_close_window(xcb_window_t win);
static void mg_del_window(xcb_window_t win);
static void mg_fini();
static void mg_focus_window(Window *win);
static void mg_grab_buttons(Window *win, int focused);
static void mg_grab_keys();
static int mg_handle_event();
static void mg_init();
static void mg_layout();
static void mg_resize_padded(Window *win, uint16_t x, uint16_t y, uint16_t w,
                             uint16_t h, char pad_left, char pad_top,
                             char pad_right, char pad_bottom);
static void mg_resize_window(Window *win, uint16_t x, uint16_t y, uint16_t w,
                             uint16_t h);
static void mg_spawn(const char *cmd, const char *argv[]);
static void mg_update_size_hints(Window *win);
static void mg_update_type(Window *win);

static void mouse_handle_events(Window *win,
                                void (*func)(Window *, int16_t, int16_t));
static void mouse_move(Window *win);
static void mouse_move_loop(Window *win, int16_t x, int16_t y);
static void mouse_resize(Window *win);
static void mouse_resize_loop(Window *win, int16_t x, int16_t y);

static Window *winlist_add(Window win);
static int winlist_count(int (*comparator)(Window *));
static void winlist_del(Window *win);
static Window *winlist_find(xcb_window_t win);
static Window *winlist_get(Window *win, int (*comparator)(Window *));
static Window *winlist_last();
static void winlist_swap(Window *a, Window *b);

#endif // __WM_H_GUARD
