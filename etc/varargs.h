#define _argc_rev() 8, 7, 6, 5, 4, 3, 2, 1, 0
#define _argc_int(a0, a1, a2, a3, a4, a5, a6, a7, num, ...) num
#define _argc2(...) _argc_int(__VA_ARGS__)
#define _argc(...) _argc2(__VA_ARGS__ __VA_OPT__(, ) _argc_rev())

static_assert(0 == _argc()); // 0 arguments works in C23 (needs __VA_OPT__)
static_assert(1 == _argc(0));
static_assert(2 == _argc(0, 0));
static_assert(3 == _argc(0, 0, 0));
static_assert(4 == _argc(0, 0, 0, 0));
static_assert(5 == _argc(0, 0, 0, 0, 0));
static_assert(6 == _argc(0, 0, 0, 0, 0, 0));
static_assert(7 == _argc(0, 0, 0, 0, 0, 0, 0));
static_assert(8 == _argc(0, 0, 0, 0, 0, 0, 0, 0));
