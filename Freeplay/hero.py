from __future__ import division
import time
import pygame
import guitarsounds_scipy as sounds
from evdev import *
import subprocess
import asyncio
import threading

#guitar = InputDevice('/dev/input/event0')

sounds.init_tones()

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
    '00011': 'g',

    '00100': 'c',
    '00101': 'd',
    '00110': 'e',
    '00111': 'c#',

    '01000': 'd',
    '01001': 'f#',
    '01010': 'g#',
    '01011': 'c',

    '01100': 'd',
    '01101': 'g#',
    '01110': 'f',
    '01111': 'e',

    '10000': 'b',
    '10001': 'a',
    '10010': 'a#',
    '10011': 'a',
    
    '10100': 'c#',
    '10101': 'a',
    '10110': 'f',
    '10111': 'f#',

    '11000': 'a',
    '11001': 'g',
    '11010': 'b',
    '11011': 'g#',

    '11100': 'd#',
    '11101': 'a',
    '11110': 'f#',
    '11111': 'g#'
}

strum_state = 0

# Currently pushed keys
PUSHED_KEYS = {}



ticks = 0

class state(object):
    current_sound = None
    keys = []
    strum_state = 0
    PLAYING_SOUNDS = {}
    COLOR_KEYS = {
        str(KEY_GREEN): False,
        str(KEY_RED): False,
        str(KEY_YELLOW): False,
        str(KEY_BLUE): False,
        str(KEY_ORANGE): False
    }
    valid_colors = [KEY_GREEN, KEY_RED, KEY_YELLOW, KEY_BLUE, KEY_ORANGE]


def play_tones(color_keys):
    print("PLAY TONE")
    return sounds.play_tone(keys_to_tones(color_keys))

def stop_tones(sound):
    print("STOP TONE")
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

class guitarThread(threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        guitar = InputDevice('/dev/input/event0')
        print("Initialized")
        for event in guitar.read_loop():
            if event.type == ecodes.EV_KEY or event.type == 3:
                # Key active
                if event.value != 0:
                    if not (event.code in state.keys):
                        state.keys.append(event.code)
                    # Color buttons
                    if event.code in state.valid_colors:
                        state.COLOR_KEYS[str(event.code)] = True
                    # Strum
                    if event.code == KEY_STRUM and (event.value == 1 or event.value == -1):
                        # New strum from neutral
                        print("Strum")
                        if state.strum_state == 0:
                            state.strum_state = 1
                            stop_tones(state.current_sound)
                            state.current_sound = play_tones(state.COLOR_KEYS)
                        # Still strumming from last cycle
                        elif state.strum_state == 1:
                            state.strum_state = 2
                # Key inactive
                else:
                    print("Key Deactived")
                    if event.code in state.valid_colors:
                        state.COLOR_KEYS[str(event.code)] = False
                        #stop_tones(state.current_sound)
                        #state.current_sound = play_tones(state.COLOR_KEYS)
                    elif event.code == KEY_STRUM:
                        state.strum_state = 0
                        #if state.current_sound != None:
                        #    stop_tones(state.current_sound)

g_thread = guitarThread(1, "Thread-1")
g_thread.daemon = True

# Run the guitar-input thread
g_thread.start()

# Main Game Loop
while True:
    
    first_input = None

    # Print input every 50 ticks
    #if ((ticks % 5) == 0):
    #    print_keys()
    ticks += 1