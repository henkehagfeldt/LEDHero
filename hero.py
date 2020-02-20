from __future__ import division
import time

import pygame
import led_tools as lt
import mappings
import guitarsounds_scipy as sounds
from evdev import *
import subprocess
import asyncio
import threading

#guitar = InputDevice('/dev/input/event0')
lt.init_matrix()

KEY_STRUM = 17
KEY_GREEN = 305
KEY_RED = 306
KEY_YELLOW = 304
KEY_BLUE = 307
KEY_ORANGE = 308


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
map_update = True
game_slowness = 3
ticks = 0

class state(object):
    current_sound = None
    keys = []
    strum_state = 0
    COLOR_KEYS = {
        str(KEY_GREEN): False,
        str(KEY_RED): False,
        str(KEY_YELLOW): False,
        str(KEY_BLUE): False,
        str(KEY_ORANGE): False
    }
    valid_colors = [KEY_GREEN, KEY_RED, KEY_YELLOW, KEY_BLUE, KEY_ORANGE]


def play_tones(color_keys):
    return sounds.play_tone(keys_to_tones(color_keys), oct=12)

def stop_tones(sound):
    sounds.stop_tone(sound)

def keys_to_tones(keys):
    binary_keys = ""
    binary_keys += str(int(state.COLOR_KEYS[str(KEY_GREEN)])) 
    binary_keys += str(int(state.COLOR_KEYS[str(KEY_RED)])) 
    binary_keys += str(int(state.COLOR_KEYS[str(KEY_YELLOW)])) 
    binary_keys += str(int(state.COLOR_KEYS[str(KEY_BLUE)])) 
    binary_keys += str(int(state.COLOR_KEYS[str(KEY_ORANGE)])) 
    
    return KEY_TONES[binary_keys]

def print_keys():
    try:
        subprocess.call('clear')
    except Exception as e:
        print(e)

    print("Color keys: \n")
    print("Green: " + str(state.COLOR_KEYS[str(KEY_GREEN)]))
    print("Red: " + str(state.COLOR_KEYS[str(KEY_RED)]))
    print("Yellow: " + str(state.COLOR_KEYS[str(KEY_YELLOW)]))
    print("Blue: " + str(state.COLOR_KEYS[str(KEY_BLUE)]))
    print("Orange: " + str(state.COLOR_KEYS[str(KEY_ORANGE)]))

    print("All pushed keys:")
    print(state.keys)

def set_button_leds():
    for (k, v) in state.COLOR_KEYS.items():
        if v:
            lt.button_pixel_on(key_to_x(k))
        else:
            lt.button_pixel_off(key_to_x(k))

def x_to_key(x):
    if x == 0:
        return KEY_GREEN
    elif x == 1:
        return KEY_RED
    elif x == 2:
        return KEY_YELLOW
    elif x == 3:
        return KEY_BLUE
    elif x == 4:
        return KEY_ORANGE
    return -1
    
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

def smart_led_update():
    print("I'm Better, hopefully")

def color_active(x):
    return state.COLOR_KEYS[str(x_to_key(x))]

def stupid_led_update():
    # Update LED-Matrix
    for x in range(0, 5):
        for y in range(0, 10):
            # First row, draw new pixels
            if map_selected[y + map_steps][x] > 0:
                lt.drop_pixel(x, y)
                #if y == 1:
                #    lt.drop_pixel(x, y, state.COLOR_KEYS[str(x_to_key(x))])
                #else:   
                #    lt.drop_pixel(x, y, False)
    map_update = False
'''
def getKey():
    for event in guitar.read_loop():
        if event.type == ecodes.EV_KEY or event.type == 3:
            if event.value == 0:
            else:
                

            e = categorize(event)
            yield e.keycode
'''

class guitarThread(threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        guitar = InputDevice('/dev/input/event0')

        for event in guitar.read_loop():
            if event.type == ecodes.EV_KEY or event.type == 3:
                # Key active
                if event.value != 0:
                    if not (event.code in state.keys):
                        state.keys.append(event.code)
                    # Color buttons
                    if event.code in state.valid_colors:
                        state.COLOR_KEYS[str(event.code)] = True
                        lt.button_pixel_on(key_to_x(event.code))
                    # Strum
                    if event.code == KEY_STRUM and (event.value == 1 or event.value == -1):
                        # New strum from neutral
                        if state.strum_state == 0:
                            state.strum_state = 1
                            state.current_sound = play_tones(state.COLOR_KEYS)
                        # Still strumming from last cycle
                        elif state.strum_state == 1:
                            state.strum_state = 2
                # Key inactive
                else:
                    if event.code in state.valid_colors:
                        state.COLOR_KEYS[str(event.code)] = False
                        lt.button_pixel_off(key_to_x(event.code))
                    elif event.code == KEY_STRUM:
                        state.strum_state = 0
                        if state.current_sound != None:
                            stop_tones(state.current_sound)

        '''
        async def key_logger(dev):
            async for ev in dev.async_read_loop():
                #if ev.keycode in VALID_KEYS:
                print(repr(ev))
                #state.keys.append(ev.keycode)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(key_logger(guitar))
        '''


g_thread = guitarThread(1, "Thread-1")
g_thread.daemon = True

# Run the guitar-input thread
g_thread.start()



# Main Game Loop
while True:

    if map_update == True:
        stupid_led_update()
    
    first_input = None
    # Check Input
    '''for event in getKey():
        next_key = next(getKey())
        if next_key in state.keys:
            break 
        else:
            state.keys.append(next_key)
'''
    #state.keys = guitar.active_keys()

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
    set_button_leds()
    lt.write_leds()
    ticks += 1

    # Move the map a step, or finish if it's done
    if ticks >= game_slowness:
        if (map_steps + 10) < len(map_selected):
            map_steps += 1
            map_update = True
        else:
            map_steps = 0
            # Map finished
            #break
        ticks = 0
