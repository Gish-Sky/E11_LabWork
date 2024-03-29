import RPi.GPIO as GPIO
import time
import csv
import sys

counts = 0
timing = 120
interval = 10
start = time.time()
dif = 0

filename = sys.argv[1]
file = open(filename, "w", newline = '')
writer = csv.writer(file)
writer.writerow(["Timestamp", "Counts"])

def my_callback(channel):
    print(f"There was a count detected at {time.time()}" )
    global counts
    counts=counts+1
    
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback)

while dif<timing:
    time.sleep(interval)  # wait 10 ms to give CPU chance to do other things
    print(f"Number of Counts is {counts}")
    timestamp = time.time()
    dif = timestamp-start
    writer.writerow([counts, timestamp])

file.close()