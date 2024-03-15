import RPi.GPIO as GPIO
import time

counts = 0

def my_callback(channel):
    print(f"There was a count detected at {time.time()}" )
    global counts
    counts = counts + 1
    
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback)

while True:
    time.sleep(10)  # wait 10 ms to give CPU chance to do other things
    print(f"Number of Counts is {counts}")




