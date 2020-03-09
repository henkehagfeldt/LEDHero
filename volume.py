#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
from subprocess import call

volume_pin = 4
volume = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(volume_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    state = GPIO.input(volume_pin) == False
    if state:
        #volume = mixer.getvolume()[0]
        volume = (volume + 10) % 110
        if volume > 100:
            volume = 100
        call(["/usr/bin/amixer", "set", "Master", str(volume)+"%"])
        print("Setting volume to: "+str(volume))
        time.sleep(0.2)