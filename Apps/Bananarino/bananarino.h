#pragma once

#define SCREEN_WIDTH  128
#define SCREEN_HEIGHT 64
#define MARGIN        3

#define TAG "Banana"


typedef struct {
    uint32_t counter;
    uint32_t d_counter;
    uint32_t msg_count;
    bool dingus;
    bool inverted;
} GameState;

enum MenuId {
    START,
    ABOUT,
    EXIT,
    RESETPROG,
};

enum AppStatus {
    MENU,
    PLAYING,
    INFO,
    RESETTING,
};

typedef struct {
    uint8_t id;
    char* name;
} Menu;

typedef struct {
    FuriMutex* mutex;
    GameState* game_state;
    uint8_t app_status;
    uint8_t menu_selected;
} AppState;
