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
import math

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
    'weird': lt.WS_ORANGE,
    'star': 'rainbow'
}

FIGURES = {
    'cross': [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [2, 0, 0, 0, 2],
        [0, 2, 0, 2, 0],
        [0, 0, 2, 0, 0],
        [0, 2, 0, 2, 0],
        [2, 0, 0, 0, 2],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]],
    'arrow_up': [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]],
    'arrow_down': [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [3, 0, 0, 0, 3],
        [3, 3, 0, 3, 3],
        [0, 3, 3, 3, 0],
        [0, 0, 3, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]]
}
strum_state = 0

# Currently pushed keys
PUSHED_KEYS = {}

PLAYING_SOUNDS = {}
current_sound = None
map_list = mappings.get_map_list()

map_steps = 0
map_update = True
game_slowness = 60
ticks = 0

class state(object):
    map_index = 0
    map_name = map_list[map_index]
    map_selected = mappings.get_map(map_name)
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
    menu = True
    done = False
    score = 0
    speed = 5
    game_speed = 400
    led_millis = 0


def play_tones(color_keys):
    # Plays the sound associated with the set buttons in color_keys
    return sounds.play_tone(keys_to_tones(color_keys))

def stop_tones(sound):
    sounds.stop_tone(sound)

def keys_to_tones(keys):
    # Converts Dict values to binary strings
    # Then converts to corresponding tone e.g 'f'
    binary_keys = ""
    binary_keys += str(int(keys[str(KEY_GREEN)])) 
    binary_keys += str(int(keys[str(KEY_RED)])) 
    binary_keys += str(int(keys[str(KEY_YELLOW)])) 
    binary_keys += str(int(keys[str(KEY_BLUE)])) 
    binary_keys += str(int(keys[str(KEY_ORANGE)])) 
    
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
            if state.map_selected[map_steps + 2][x] > 0:
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
            if state.map_selected[y + map_steps][x] > 0:
                lt.drop_pixel(x, y)

    map_update = False

def checkForHit():
    hit = True
    for (k, v) in state.COLOR_KEYS.items():
        x = key_to_x(int(k))
        if state.map_selected[map_steps + 2][x] > 0 and not v:
            # Note missed
            hit = False
            lt.miss_led(x)
        elif not state.map_selected[map_steps + 2][x] > 0 and v:
            # Hit nothing
            hit = False
            lt.miss_led(x)
        elif state.map_selected[map_steps + 2][x] > 0 and v:
            lt.hit_led(x)

    if hit:
        state.score += 1
        state.current_sound = play_tones(state.COLOR_KEYS)
    else:
        state.score -= 1
        if state.score < 0:
            state.score = 0
        state.current_sound = sounds.play_miss()

def change_speed(direction):
    state.led_millis = get_millis()

    if direction == 1:
        if state.speed < 10:
            state.speed += 1
            draw("arrow_up")
        else:
            draw("cross")

    elif direction == -1:
        # Speed Down
        if state.speed > 0:
            state.speed -= 1
            draw("arrow_down")
        else:
            draw("cross")

def x_to_color(x):
    col = lt.WS_CLEAR
    if x == 1:
        col = lt.WS_GREEN
    elif x == 2:
        col = lt.WS_RED
    elif x == 3:
        col = lt.WS_YELLOW
    elif x == 4:
        col = lt.WS_BLUE
    elif x == 5:
        col = lt.WS_ORANGE
    return col

def draw(fig):
    figure = FIGURES[fig]
    for x in range(0, 5):
        for y in range(10, 0, -1):
            lt.set_pixel_clr(x, y, x_to_color(figure[y][x]))
    

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

                        # Choose song
                        if state.menu:
                            if KEY_GREEN == event.code:
                                game_on()
                            elif KEY_RED == event.code:
                                # Speed down
                                change_speed(-1)
                                
                            elif KEY_YELLOW == event.code:
                                # Speed up
                                change_speed(1)
                                
                        elif state.done and KEY_GREEN == event.code:
                            state.done = False
                            state.menu = True
                            state.score = 0


                    # Strum
                    if event.code == KEY_STRUM and (event.value == 1 or event.value == -1):

                        # New strum from neutral
                        if state.strum_state == 0:
                            state.strum_state = 1
                            if not state.menu:
                                # Check for a hit if playing a song
                                checkForHit()
                            else:
                                # Switch song preview if in menu
                                change_preview(event.value)

                        # Still strumming from last cycle
                        elif state.strum_state == 1:
                            state.strum_state = 2

                # Key inactive
                else:
                    if event.code in state.valid_colors:
                        state.COLOR_KEYS[str(event.code)] = False
                    elif event.code == KEY_STRUM:
                        state.strum_state = 0
 
def game_on():

    # Clear all LEDs
    for x in range(0, 5):
        for y in range(0, 10):
            lt.set_pixel_clr(x, y, lt.WS_CLEAR)

    # Disable menu mode
    state.menu = False

    # Set game speed
    state.game_speed = 200 + (state.speed * 30) 

def get_millis():
    return int(round(time.time() * 1000))

def preview_song_music(song):

    if not state.previewing == song:
        state.previewing = song

        # Give a head start to skip all initial dead notes
        state.preview_step = 8
    
    if (state.preview_step + 11) < len(state.map_selected):
        state.preview_step += 1
    else:
        # Restart song preview
        state.preview_step = 0

    # Simulate actual correct keys being pressed
    fake_keys = {
        str(KEY_GREEN): state.map_selected[state.preview_step][0] > 0,
        str(KEY_RED): state.map_selected[state.preview_step][1] > 0,
        str(KEY_YELLOW): state.map_selected[state.preview_step][2] > 0,
        str(KEY_BLUE): state.map_selected[state.preview_step][3] > 0,
        str(KEY_ORANGE): state.map_selected[state.preview_step][4] > 0,
    }

    play_tones(fake_keys)

def preview_song_leds(song):
    for x in range(0,5):
        for y in range(0,10):
            lt.set_pixel_clr(x, y, MAP_COLORS[song])

def change_preview(direction):
    if(direction == 1):
        state.map_index = (state.map_index + 1) % len(map_list)
    elif(direction == -1):
        state.map_index = (state.map_index - 1) % len(map_list)
    state.map_name = map_list[state.map_index]
    state.map_selected = mappings.get_map(state.map_name)
    
def show_score(score):
    multiplier = (state.speed - 190) / 30
    actual_score = state.score * multiplier

    for x in range(0, 5):
        # state.score = 123
        s = actual_score % (10**(x+1))
        # s = 3
        s = math.floor(s / (10**x))

        for y in range(0, 10):
            # 123
            if(s >= (y + 1)):
                lt.set_pixel_clr(x, y, 'rainbow')

            
g_thread = guitarThread(1, "Thread-1")
g_thread.daemon = True

# Run the guitar-input thread
g_thread.start()

millis = get_millis()

led_time = 200
diff_time = 20
state.led_millis = get_millis()

# Main Game Loop
while True:
    
    # In menu
    if state.menu:
        if (get_millis() - state.led_millis) >= led_time:
            state.led_millis = get_millis()
            preview_song_leds(state.map_name)

        if (get_millis() - millis) >= (state.game_speed - diff_time):
            millis = get_millis()
            preview_song_music(state.map_name)
    # In game
    elif state.done:
        if (get_millis() - state.led_millis) >= led_time:
            state.led_millis = get_millis()
            show_score(state.score)
    else:
        # Check if the led matrix should move a step
        if map_update:
            stupid_led_update()

        # Set the LEDs for which buttons are pressed
        set_button_leds()

        # Move the map a step, or finish if it's done
        if (get_millis() - millis) >= (state.game_speed - diff_time):
            millis = get_millis()

            if (map_steps + 11) < len(state.map_selected):
                map_steps += 1
                map_update = True
            else:
                # Map finished
                map_steps = 0
                state.done = True
                
            lt.clear_hits()
            sounds.play_pace()
            print_keys()
    lt.write_leds()
