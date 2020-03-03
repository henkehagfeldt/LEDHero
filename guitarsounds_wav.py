import pygame
import numpy
import os 

#pygame.mixer.init()
midi_tones = {}
filetype = 'wav'
mode = 'Acoustic'
notes = ['A3', 'A3#_B3b', 'B3', 'C3', 'C3#_D3b', 'D3', 'D3#_E3b', 'E3', 'F3', 'F3#_G3b', 'G3', 'G3#_A3b']
def init_tones():
    pygame.mixer.init(44100, -16, 1, 512)
    #pygame.mixer.init()
    #pygame.init()
    midi_tones['a'] = pygame.mixer.Sound(filetype+'/'+mode+'/'+notes[0]+'.'+filetype)
    midi_tones['a#'] = pygame.mixer.Sound(filetype+'/'+mode+'/'+notes[1]+'.'+filetype)
    midi_tones['b'] = pygame.mixer.Sound(filetype+'/'+mode+'/'+notes[2]+'.'+filetype)
    midi_tones['c'] = pygame.mixer.Sound(filetype+'/'+mode+'/'+notes[3]+'.'+filetype)
    midi_tones['c#'] = pygame.mixer.Sound(filetype+'/'+mode+'/'+notes[4]+'.'+filetype)
    midi_tones['d'] = pygame.mixer.Sound(filetype+'/'+mode+'/'+notes[5]+'.'+filetype)
    midi_tones['d#'] = pygame.mixer.Sound(filetype+'/'+mode+'/'+notes[6]+'.'+filetype)
    midi_tones['e'] = pygame.mixer.Sound(filetype+'/'+mode+'/'+notes[7]+'.'+filetype)
    midi_tones['f'] = pygame.mixer.Sound(filetype+'/'+mode+'/'+notes[8]+'.'+filetype)
    midi_tones['f#'] = pygame.mixer.Sound(filetype+'/'+mode+'/'+notes[9]+'.'+filetype)
    midi_tones['g'] = pygame.mixer.Sound(filetype+'/'+mode+'/'+notes[10]+'.'+filetype)
    midi_tones['g#'] = pygame.mixer.Sound(filetype+'/'+mode+'/'+notes[11]+'.'+filetype)


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
