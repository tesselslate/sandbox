/*
 *  A basic SDL application to measure input latency on the desktop with a slow
 *  motion camera.
 */

#include <SDL2/SDL.h>
#include <SDL2/SDL_render.h>
#include <stdio.h>
#include <time.h>

#define SCREEN_WIDTH 640
#define SCREEN_HEIGHT 480

int
main(int argc, char *args[]) {
    SDL_Window *window = NULL;
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        fprintf(stderr, "could not initialize sdl2: %s\n", SDL_GetError());
        return 1;
    }
    window = SDL_CreateWindow("hello_sdl2", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
                              SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    if (window == NULL) {
        fprintf(stderr, "could not create window: %s\n", SDL_GetError());
        return 1;
    }

    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    SDL_Event evt;
    int frame = 0;
    int key = 0;
    struct timespec ts1;
    struct timespec ts2;
    clock_gettime(CLOCK_MONOTONIC, &ts1);
    while (1) {
        clock_gettime(CLOCK_MONOTONIC, &ts2);
        uint64_t t1 = ts1.tv_sec * 1000000000 + ts1.tv_nsec;
        uint64_t t2 = ts2.tv_sec * 1000000000 + ts2.tv_nsec;
        if (t2 - t1 >= 1000000000 / 165) {
            while (SDL_PollEvent(&evt) != 0) {
                if (evt.type == SDL_KEYDOWN) {
                    key = 1;
                } else if (evt.type == SDL_KEYUP) {
                    key = 0;
                } else if (evt.type == SDL_QUIT) {
                    goto end;
                }
            }
            frame = (frame + 1) % 4;

            if (key) {
                SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
                SDL_RenderClear(renderer);
            } else {
                SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
                SDL_RenderClear(renderer);
                SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255);
                SDL_Rect rect = {0, 0, 100, 100};
                rect.x = frame * 100;
                SDL_RenderFillRect(renderer, &rect);
            }
            SDL_RenderPresent(renderer);
            uint64_t delta = t2 - t1;
            ts1 = ts2;
            printf("fps: %lf\t%" PRIu64 "\t%" PRIu64 "\n", 1000000000.0 / (double)delta,
                   ts2.tv_nsec, ts1.tv_nsec);
        }
    }
end:
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
