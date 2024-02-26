#include <stdint.h>
#include <stdio.h>
#include <time.h>

int
main() {
    static const size_t N = 1000000000;

    struct timespec ts, start, end;

    clock_gettime(CLOCK_MONOTONIC, &start);
    for (size_t i = 0; i < N; i++) {
        clock_gettime(CLOCK_MONOTONIC, &ts);
    }
    clock_gettime(CLOCK_MONOTONIC, &end);

    uint64_t start_us = start.tv_sec * 1000000 + start.tv_nsec / 1000;
    uint64_t end_us = end.tv_sec * 1000000 + end.tv_nsec / 1000;
    double seconds = (double)(end_us - start_us) / 1000000;
    printf("%lf (%lf/sec)\n", seconds, (double)N / seconds);
}
