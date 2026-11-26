#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct {
    uint32_t type, timestamp, window;
    union {
        char text[32];
        struct { uint32_t which; uint8_t button, state, clicks, pad; int x, y; } mouse;
        struct { uint8_t state, repeat, pad[2]; int scan, key; uint16_t mod; } keyboard;
    } data;
} input_event;

int SDL_PollEvent(void *event) {
    static int (*poll_event)(void *);
    static FILE *commands;
    static long long ready;
    static char command[4096];
    static size_t remaining, offset;
    static int initialized, finished, click;
    if (!poll_event) poll_event = dlsym(RTLD_NEXT, "SDL_PollEvent");
    int result = poll_event(event);
    if (result || !event || finished) return result;
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    long long now = ts.tv_sec * 1000LL + ts.tv_nsec / 1000000;
    if (!initialized) {
        initialized = 1;
        ready = now + 2000;
        commands = fopen(getenv("SKRAUN_COMMANDS"), "r");
        if (!commands) finished = 1;
    }
    if (finished || now < ready) return 0;
    if (click < 2) {
        input_event *input = event;
        memset(input, 0, sizeof *input);
        input->window = 1;
        input->type = click == 0 ? 0x401 : 0x402;
        input->data.mouse.button = 1;
        input->data.mouse.state = click == 0;
        input->data.mouse.clicks = 1;
        input->data.mouse.x = 155;
        input->data.mouse.y = 650;
        ++click;
        ready = now + 40;
        return 1;
    }
    if (!offset && !remaining) {
        if (!fgets(command, sizeof command, commands)) {
            finished = 1;
            fclose(commands);
            return 0;
        }
        remaining = strcspn(command, "\r\n");
        fprintf(stderr, "command: %s", command);
    }
    input_event *input = event;
    memset(input, 0, sizeof *input);
    input->window = 1;
    if (remaining) {
        size_t size = 1;
        input->type = 0x303; /* SDL_TEXTINPUT */
        memcpy(input->data.text, command + offset, size);
        remaining -= size;
        offset += size;
    } else {
        input->type = 0x300; /* SDL_KEYDOWN */
        input->data.keyboard.state = 1;
        input->data.keyboard.scan = 40;
        input->data.keyboard.key = '\r';
        offset = 0;
        ready = now + 35;
    }
    return 1;
}
