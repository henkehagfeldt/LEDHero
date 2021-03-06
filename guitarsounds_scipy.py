import pygame, pygame.sndarray
import numpy
import os 

pygame.mixer.init(44100, -16, 1, 1024)
#pygame.mixer.init()
midi_tones = {}
init_tones()

def init_tones():
    midi_tones['a'] = pygame.mixer.sound('midi/A3.wav')
    midi_tones['a#'] = pygame.mixer.sound('midi/A3#_B3b.wav')
    midi_tones['b'] = pygame.mixer.sound('midi/B3.wav')
    midi_tones['c'] = pygame.mixer.sound('midi/C3.wav')
    midi_tones['c#'] = pygame.mixer.sound('midi/C3#_D3b.wav')
    midi_tones['d'] = pygame.mixer.sound('midi/D3.wav')
    midi_tones['d#'] = pygame.mixer.sound('midi/D3#_E3b.wav')
    midi_tones['e'] = pygame.mixer.sound('midi/E3.wav')
    midi_tones['f'] = pygame.mixer.sound('midi/F3.wav')
    midi_tones['f#'] = pygame.mixer.sound('midi/F3#_G3b.wav')
    midi_tones['g'] = pygame.mixer.sound('midi/G3.wav')
    midi_tones['g#'] = pygame.mixer.sound('midi/G3#_A3b.wav')

def get_tone(tone, octave):
    r_tone = 0
    '''
    if tone == 'a':
        r_tone = 27.5
    elif tone == 'a#':
        r_tone = 29.14
    elif tone == 'b':
        r_tone = 30.87
    elif tone == 'c':
        r_tone = 16.35
    elif tone == 'c#':
        r_tone = 17.32
    elif tone == 'd':
        r_tone = 18.35
    elif tone == 'd#':
        r_tone = 19.45
    elif tone == 'e':
        r_tone = 20.60
    elif tone == 'f':
        r_tone = 21.83
    elif tone == 'f#':
        r_tone = 23.12
    elif tone == 'g':
        r_tone = 24.50
    elif tone == 'g#':
        r_tone = 25.96
    if tone == 'a':
        r_tone = 440
    elif tone == 'a#':
        r_tone = 466
    elif tone == 'b':
        r_tone = 494
    elif tone == 'c':
        r_tone = 261
    elif tone == 'c#':
        r_tone = 277
    elif tone == 'd':
        r_tone = 294
    elif tone == 'd#':
        r_tone = 311
    elif tone == 'e':
        r_tone = 330
    elif tone == 'f':
        r_tone = 349
    elif tone == 'f#':
        r_tone = 370
    elif tone == 'g':
        r_tone = 392
    elif tone == 'g#':
        r_tone = 415
    '''
    return r_tone


'''
def play_for(sample_wave, ms):
    """Play the given NumPy array, as a sound, for ms milliseconds."""
    sound = pygame.sndarray.make_sound(sample_wave)
    sound.play(-1)
    pygame.time.delay(ms)
    sound.stop()
'''

def play_tone(tone):
    if tone in midi_tones:
        midi_tones[tone].play(-1)


def play_tone(tone, oct):
    tone = get_tone(tone, oct)
    sample_wave = sine_wave(tone, 2048, 100)
    """Play the given NumPy array, as a sound, for ms milliseconds."""
    sound = pygame.sndarray.make_sound(sample_wave)
    sound.play(-1)
    return sound
    
def stop_tone(tone):
    try:
        midi_tones[tone].stop()
    except Exception as e:
        print("Sound can't be stopped.")
        print(e) 

def sine_wave(hz, peak, n_samples=sample_rate):
    """Compute N samples of a sine wave with given frequency and peak amplitude.
       Defaults to one second.
    """
    length = sample_rate / float(hz)
    omega = numpy.pi * 2 / length
    xvalues = numpy.arange(int(length)) * omega
    onecycle = peak * numpy.sin(xvalues)
    return numpy.resize(onecycle, (n_samples,)).astype(numpy.int16)

# Play A (440Hz) for 1 second as a sine wave:
#play_for(sine_wave(440, 4096), 1000)

# Play A-440 for 1 second as a square wave:
#play_for(square_wave(440, 4096), 1000)