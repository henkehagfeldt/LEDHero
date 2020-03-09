import alsaaudio
import RPi.GPIO as GPIO
import time

mixer = alsaaudio.Mixer('PCM')

volume_pin = 4
volume = 50
GPIO.setmode(GPIO.BCM)
GPIO.setup(volume_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    state = GPIO.input(volume_pin) == False
    if state:
        volume = (volume + 10) % 110
        mixer.setvolume(volume)
        print("Setting volume to"+str(volume))
        time.sleep(0.5)