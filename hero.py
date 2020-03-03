from __future__ import division
import time

import pygame
import led_tools as lt
import mappings
import guitarsounds_wav as sounds
from evdev import *
import subprocess
import asyncio
import threading

#guitar = InputDevice('/dev/input/event0')
lt.init_matrix()
sounds.init_tones()

KEY_STRUM = 17
KEY_GREEN = 305
KEY_RED = 306
KEY_YELLOW = 304
KEY_BLUE = 307
KEY_ORANGE = 308


VALID_KEYS = {KEY_STRUM, KEY_GREEN, KEY_RED, KEY_YELLOW, KEY_BLUE, KEY_ORANGE}
KEY_TONES = {
    '00000': 'notone',
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

MAP_COLORS = {
    'star': 'rainbow'
}

strum_state = 0

# Currently pushed keys
PUSHED_KEYS = {}

PLAYING_SOUNDS = {}
current_sound = None

map_name = 'star'
map_selected = mappings.get_map(map_name)
map_steps = 0
map_update = True
game_slowness = 60
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
    previewing = None
    preview_step = 0


def play_tones(color_keys):
    # Plays the sound associated with the set buttons in color_keys
    return sounds.play_tone(keys_to_tones(color_keys))

def stop_tones(sound):
    sounds.stop_tone(sound)

def keys_to_tones(keys):
    # Converts Dict values to binary strings
    # Then converts to corresponding tone e.g 'f'
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
        x = key_to_x(int(k))
        if v:
            lt.button_pixel_on(x)
        else:
            # Check if button is on according to map
            if map_selected[map_steps + 2][x] > 0:
                lt.set_pixel(x, 1)
            else:
                # Else turn pixel off
                lt.button_pixel_off(x)

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
    else:
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
    else:
        return -1

def smart_led_update():
    print("I'm Better, hopefully")

def color_active(x):
    return state.COLOR_KEYS[str(x_to_key(x))]

def stupid_led_update():
    # Update LED-Matrix
    for x in range(0, 5):
        for y in range(0, 11):
            if map_selected[y + map_steps][x] > 0:
                lt.drop_pixel(x, y)

    map_update = False

def checkForHit():
    hit = True
    for (k, v) in state.COLOR_KEYS.items():
        x = key_to_x(int(k))
        if map_selected[map_steps + 2][x] > 0 and not v:
            # Note missed
            hit = False
            lt.miss_led(x)
        elif not map_selected[map_steps + 2][x] > 0 and v:
            # Hit nothing
            hit = False
            lt.miss_led(x)
        elif map_selected[map_steps + 2][x] > 0 and v:
            lt.hit_led(x)

    if hit:
        state.current_sound = play_tones(state.COLOR_KEYS)
    else:
        state.current_sound = sounds.play_miss()

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

                    # Strum
                    if event.code == KEY_STRUM and (event.value == 1 or event.value == -1):

                        # New strum from neutral
                        if state.strum_state == 0:
                            state.strum_state = 1
                            if not menu:
                                checkForHit()

                        # Still strumming from last cycle
                        elif state.strum_state == 1:
                            state.strum_state = 2

                # Key inactive
                else:
                    if event.code in state.valid_colors:
                        state.COLOR_KEYS[str(event.code)] = False
                    elif event.code == KEY_STRUM:
                        state.strum_state = 0
 

def get_millis():
    return int(round(time.time() * 1000))

def preview_song_music(song):
    if not state.previewing == song:
        state.previewing = song
        state.preview_step = 0

    elif (state.preview_step + 11) < len(map_selected):
        state.preview_step += 1

    fake_keys = {
        str(KEY_GREEN): map_selected[state.preview_step][0] > 0,
        str(KEY_RED): map_selected[state.preview_step][1] > 0,
        str(KEY_YELLOW): map_selected[state.preview_step][2] > 0,
        str(KEY_BLUE): map_selected[state.preview_step][3] > 0,
        str(KEY_ORANGE): map_selected[state.preview_step][4] > 0,
    }

    play_tones(fake_keys)

def preview_song_leds(song):
    for x in range(0,5):
        for y in range(0,10):
            lt.set_pixel_clr(x, y, MAP_COLORS[song])
    
    

g_thread = guitarThread(1, "Thread-1")
g_thread.daemon = True

# Run the guitar-input thread
g_thread.start()

millis = get_millis()
game_time = 400
diff_time = 20
menu = True


# Main Game Loop
while True:
    
    # In menu
    if menu:
        preview_song_leds(map_name)
        if (get_millis() - millis) >= (game_time - diff_time):
            millis = get_millis()
            preview_song_music(map_name)
    # In game
    else:
        # Check if the led matrix should move a step
        if map_update:
            stupid_led_update()

        # Set the LEDs for which buttons are pressed
        set_button_leds()

        # Move the map a step, or finish if it's done
        if (get_millis() - millis) >= (game_time - diff_time):
            millis = get_millis()

            if (map_steps + 11) < len(map_selected):
                map_steps += 1
                map_update = True
            else:
                # Map finished
                map_steps = 0
                
        
            ticks = 0
            lt.clear_hits()
            sounds.play_pace()
            print_keys()
    lt.write_leds()
