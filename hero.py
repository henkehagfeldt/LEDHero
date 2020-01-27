from __future__ import division
import time

import pygame
import led_tools as lt
import mappings
import guitarsounds as sounds
import evdev

guitar = evdev.InputDevice('/dev/input/event0')
pygame.init()

lt.init_matrix()

lt.set_pixel((0,2))
lt.set_pixel_clr((0,2), lt.WS_GREEN)

current_map = mappings.get_map('hero')
current_steps = 0
speed = 2

KEY_STRUM = 0
KEY_GREEN = 0
KEY_RED = 0
KEY_YELLOW = 0
KEY_BLUE = 0
KEY_ORANGE = 0

KEYS = [KEY_GREEN, KEY_RED, KEY_YELLOW, KEY_BLUE, KEY_ORANGE]



# Main Game Loop
while True:

    # Update LED-Matrix
    for x in range(0, lt.PXL_CNT/lt.PXL_COL_CNT):
        for y in range(0, lt.PXL_COL_CNT):
            # First row, draw new pixels
            if x == 0:
                if current_map[x, y + current_steps] > 0:
                    lt.set_pixel((x, y))
            else:
                lt.drop_pixel((x, y))

    # Check Input
    keys = guitar.active_keys()
    for(x in range(0, len(KEYS))):
        if KEYS[x] in keys:
            lt.button_pixel(x)
    
    # Play Sounds
    
        

    # Move the map a step, or finish if it's done
    if current_steps < len(current_map[0]):
        current_steps += 1
    else
        return

    # Update frequency
    time.sleep(1/speed)

    



