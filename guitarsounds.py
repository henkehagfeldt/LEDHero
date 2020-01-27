import pygame, pygame.sndarray
import numpy
import scipy.signal


def get_tone(tone, octave):
    r_tone = 0
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

    return r_tone*octave

def play_for(sample_wave, ms):
    """Play the given NumPy array, as a sound, for ms milliseconds."""
    sound = pygame.sndarray.make_sound(sample_wave)
    sound.play(-1)
    pygame.time.delay(ms)
    sound.stop()

sample_rate = 44100

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