from __future__ import division
import time

import pygame
import led_tools as lt
import mappings
import guitarsounds as sounds
import evdev
from sys import subprocess

guitar = evdev.InputDevice('/dev/input/event0')
pygame.init()

lt.init_matrix()

lt.set_pixel((0,2))
lt.set_pixel_clr((0,2), lt.WS_GREEN)

KEY_STRUM = 0
KEY_GREEN = 0
KEY_RED = 0
KEY_YELLOW = 0
KEY_BLUE = 0
KEY_ORANGE = 0

COLOR_KEYS = {
    str(KEY_GREEN): False,
    str(KEY_RED): False,
    str(KEY_YELLOW): False,
    str(KEY_BLUE): False,
    str(KEY_ORANGE): False
    }
# Currently pushed keys
PUSHED_KEYS = {}

PLAYING_SOUNDS = {}

map_selected = mappings.get_map('hero')
map_steps = 0
game_slowness = 200
ticks = 0


# Main Game Loop
while True:

    # Update LED-Matrix
    for x in range(0, lt.PXL_CNT/lt.PXL_COL_CNT):
        for y in range(0, lt.PXL_COL_CNT):
            # First row, draw new pixels
            if x == 0:
                if map_selected[x, y + map_steps] > 0:
                    lt.set_pixel((x, y))
            else:
                lt.drop_pixel((x, y))

    # Check Input
    keys = guitar.active_keys()

    # Print input every 50 ticks
    if ((ticks % 50) == 0):
        print_keys()

    # Register new keys
    TEMP_KEYS = {}
    for(k in range(0, len(KEYS))):
        if KEYS[k] in keys:
            TEMP_KEYS[k] = True
    
    # Check which keys are no longer held
    for(k in PUSHED_KEYS):
        if k not in TEMP_KEYS:
            # Key released
            if(str(k) in COLOR_KEYS):
                COLOR_KEYS[str(k)] = False
                lt.button_pixel_off(key_to_x(k))
    
    # Check which keys that are triggered this cycle
    for(k in TEMP_KEYS):
        if k not in PUSHED_KEYS:
            # New keys pressed
            if(str(k) in COLOR_KEYS):
                COLOR_KEYS[str(k)] = True
                lt.button_pixel_on(key_to_x(k))


    #sounds.stop_tone(PLAYING_SOUNDS[k])
    
    # Play Sounds
    #s = sounds.play_tone('a#', oct=4)
    #sounds.stop_tone(s)
    
    ticks += 1

    # Move the map a step, or finish if it's done
    if ticks >= game_slowness:
        if map_steps < len(map_selected[0]):
            map_steps += 1
        else
            # Map finished
            return
        ticks = 0

def print_keys():
    try:
        subprocess('clear')
    except Exception as e:
        print(e)

    print("Color keys: \n")
    print("Green: " + str(COLOR_KEYS[KEY_GREEN]))
    print("Red: " + str(COLOR_KEYS[KEY_RED]))
    print("Yellow: " + str(COLOR_KEYS[KEY_YELLOW]))
    print("Blue: " + str(COLOR_KEYS[KEY_BLUE]))
    print("Orange: " + str(COLOR_KEYS[KEY_ORANGE]))

    print("All pushed keys:")
    print(keys)

    
def key_to_x(key):
    if key == KEY_GREEN:
        return 0
    elif key == KEY_RED:
        return 1
    elif key == KEY_YELLOW:
        return 2
    elif key == KEY_BLUE:
        return 3
    elif key == KEY_ORANGE:
        return 4

    return -1


