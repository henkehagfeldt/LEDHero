import pygame
import numpy
import os 

#pygame.mixer.init()
midi_tones = {}

def init_tones():
    pygame.mixer.init(44100, -16, 1, 1024)
    #pygame.mixer.init()
    #pygame.init()
    midi_tones['a'] = pygame.mixer.Sound('midi/Long/A3.wav')
    midi_tones['a#'] = pygame.mixer.Sound('midi/Long/A3#_B3b.wav')
    midi_tones['b'] = pygame.mixer.Sound('midi/Long/B3.wav')
    midi_tones['c'] = pygame.mixer.Sound('midi/Long/C3.wav')
    midi_tones['c#'] = pygame.mixer.Sound('midi/Long/C3#_D3b.wav')
    midi_tones['d'] = pygame.mixer.Sound('midi/Long/D3.wav')
    midi_tones['d#'] = pygame.mixer.Sound('midi/Long/D3#_E3b.wav')
    midi_tones['e'] = pygame.mixer.Sound('midi/Long/E3.wav')
    midi_tones['f'] = pygame.mixer.Sound('midi/Long/F3.wav')
    midi_tones['f#'] = pygame.mixer.Sound('midi/Long/F3#_G3b.wav')
    midi_tones['g'] = pygame.mixer.Sound('midi/Long/G3.wav')
    midi_tones['g#'] = pygame.mixer.Sound('midi/Long/G3#_A3b.wav')


def play_tone(tone):
    print("Play sound")
    if tone in midi_tones:
        midi_tones[tone].play(loops=-1, maxtime=1000,fade_ms=200)
        midi_tones[tone].fadeout(1600)
        
    
def stop_tone(tone):
    try:
        midi_tones[tone].stop()
    except Exception as e:
        print("Sound can't be stopped.")
        print(e) 
