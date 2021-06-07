import face_recognition
import os
import RPi.GPIO as GPIO
from os import listdir
from os.path import isfile, join
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN)
GPIO.setup(5, GPIO.OUT)

gate = 5
button = 3

while True:
    if GPIO.input(button) == GPIO.HIGH:
        os.system("fswebcam -r 1280x720 --no-banner img.jpg")
        # Controllo se ci sono persone che conosco
        found = os.system("face_recognition ./people/ img.jpg | cut -d ',' -f2")
        # Se ci sono apro il cancello
        if found != "no_persons_found":
            os.system("telegram-send \"" + found + "è entrato in casa\"")
            GPIO.output(gate, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(gate, GPIO.LOW)





