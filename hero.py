from __future__ import division
import time

import pygame
import led_tools as lt
import mappings
#import guitarsounds as sounds
import evdev
import subprocess

guitar = evdev.InputDevice('/dev/input/event0')
pygame.init()

lt.init_matrix()

KEY_STRUM = 17
KEY_GREEN = 305
KEY_RED = 306
KEY_YELLOW = 304
KEY_BLUE = 307
KEY_ORANGE = 308

COLOR_KEYS = {
    str(KEY_GREEN): False,
    str(KEY_RED): False,
    str(KEY_YELLOW): False,
    str(KEY_BLUE): False,
    str(KEY_ORANGE): False
}

VALID_KEYS = {KEY_STRUM, KEY_GREEN, KEY_RED, KEY_YELLOW, KEY_BLUE, KEY_ORANGE}
KEY_TONES = {
    '00000': 'f',
    '00001': 'a',
    '00010': 'b',
    '00011': 'a',

    '00100': 'c',
    '00101': 'a',
    '00110': 'a',
    '00111': 'a',

    '01000': 'd',
    '01001': 'a',
    '01010': 'a',
    '01011': 'a',

    '01100': 'a',
    '01101': 'a',
    '01110': 'a',
    '01111': 'a',

    '10000': 'e',
    '10001': 'a',
    '10010': 'a',
    '10011': 'a',
    
    '10100': 'a',
    '10101': 'a',
    '10110': 'a',
    '10111': 'a',

    '11000': 'a',
    '11001': 'a',
    '11010': 'a',
    '11011': 'a',

    '11100': 'a',
    '11101': 'a',
    '11110': 'a',
    '11111': 'a'
}
strum_state = 0

# Currently pushed keys
PUSHED_KEYS = {}

PLAYING_SOUNDS = {}
current_sound = None

map_selected = mappings.get_map('hero')
map_steps = 0
game_slowness = 50
ticks = 0


'''
def play_tones(color_keys):
    return sounds.play_tone(keys_to_tones(color_keys), oct=4)

def stop_tones(sound):
    sounds.stop_tone(sound)
'''
def keys_to_tones(keys):
    binary_keys = ""
    binary_keys += str(int(COLOR_KEYS[str(KEY_GREEN)])) 
    binary_keys += str(int(COLOR_KEYS[str(KEY_RED)])) 
    binary_keys += str(int(COLOR_KEYS[str(KEY_YELLOW)])) 
    binary_keys += str(int(COLOR_KEYS[str(KEY_BLUE)])) 
    binary_keys += str(int(COLOR_KEYS[str(KEY_ORANGE)])) 
    
    return KEY_TONES[binary_keys]

def print_keys():
    try:
        subprocess.call('clear')
    except Exception as e:
        print(e)

    print("Color keys: \n")
    print("Green: " + str(COLOR_KEYS[str(KEY_GREEN)]))
    print("Red: " + str(COLOR_KEYS[str(KEY_RED)]))
    print("Yellow: " + str(COLOR_KEYS[str(KEY_YELLOW)]))
    print("Blue: " + str(COLOR_KEYS[str(KEY_BLUE)]))
    print("Orange: " + str(COLOR_KEYS[str(KEY_ORANGE)]))

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

y = 9
# Main Game Loop
while True:

    
    # Update LED-Matrix
    for x in range(0, 5):
        for y in range(0, 10):
            # First row, draw new pixels
            if map_selected[y + map_steps][x] > 0:
                lt.drop_pixel(x, y)
                #print("Dropping pixel")
            '''
            if y == 9:
                if map_selected[y + map_steps][x] > 0:
                    lt.set_pixel(x, y)
                    print("Setting pixel")
            elif map_selected[y + map_steps][x] > 0:
                lt.drop_pixel(x, y)
            '''
                
    
    # Check Input
    keys = guitar.active_keys()

    # Print input every 50 ticks
    if ((ticks % 5) == 0):
        print_keys()
    '''
    # Register new keys
    TEMP_KEYS = {}
    for k in range(0, len(keys)):
        if keys[k] in VALID_KEYS:
            TEMP_KEYS[k] = True
    
    # Check which keys are no longer held
    for k in PUSHED_KEYS:
        if k not in TEMP_KEYS:
            # Key released
            if(str(k) in COLOR_KEYS):
                COLOR_KEYS[str(k)] = False
                lt.button_pixel_off(key_to_x(k))
            
            if(k == KEY_STRUM):
                strum_state = 0
    
    # Check which keys that are triggered this cycle
    for k in TEMP_KEYS:
        if k not in PUSHED_KEYS:
            # New keys pressed
            if(str(k) in COLOR_KEYS):
                COLOR_KEYS[str(k)] = True
                lt.button_pixel_on(key_to_x(k))
            
            # Check strumbar
            if(k == KEY_STRUM):
                # New strum from neutral
                if strum_state == 0:
                    strum_state = 1
                # Still strumming from last cycle
                elif strum_state == 1:
                    strum_state = 2

    
    #sounds.stop_tone(PLAYING_SOUNDS[k])
    
    # Play Sounds on new strum
    if(strum_state == 1):
        current_sound = play_tones(COLOR_KEYS)


    #s = sounds.play_tone('a#', oct=4)
    #sounds.stop_tone(s)
    
    PUSHED_KEYS = TEMP_KEYS
    '''
    ticks += 1

    # Move the map a step, or finish if it's done
    if ticks >= game_slowness:
        if (map_steps + 10) < len(map_selected):
            map_steps += 1
        else:
            # Map finished
            break
        ticks = 0
