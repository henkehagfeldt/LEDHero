import pygame, pygame.sndarray
import numpy

pygame.init()

def get_tone(tone, octave):
    r_tone = 0
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

    return 440
sample_rate = 44100


'''
def play_for(sample_wave, ms):
    """Play the given NumPy array, as a sound, for ms milliseconds."""
    sound = pygame.sndarray.make_sound(sample_wave)
    sound.play(-1)
    pygame.time.delay(ms)
    sound.stop()
'''

def play_tone(tone):
    tone = get_tone(tone, oct)
    sample_wave = sine_wave(tone, 4096, 1000)
    """Play the given NumPy array, as a sound, for ms milliseconds."""
    sound = pygame.sndarray.make_sound(sample_wave)
    sound.play(-1)
    return sound
    
def stop_tone(sound):
    try:
        sound.stop()
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

def square_wave(hz, peak, duty_cycle=.5, n_samples=sample_rate):
    """Compute N samples of a sine wave with given frequency and peak amplitude.
       Defaults to one second.
    """
    t = numpy.linspace(0, 1, 500 * 440/hz, endpoint=False)
    wave = scipy.signal.square(2 * numpy.pi * 5 * t, duty=duty_cycle)
    wave = numpy.resize(wave, (n_samples,))
    return (peak / 2 * wave.astype(numpy.int16))

# Play A (440Hz) for 1 second as a sine wave:
play_for(sine_wave(440, 4096), 1000)

# Play A-440 for 1 second as a square wave:
play_for(square_wave(440, 4096), 1000)