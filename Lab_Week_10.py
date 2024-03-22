import RPi.GPIO as GPIO
import time
import csv

counts = 0

def my_callback(channel, timing, interval, filename):
    filename = '{filename}.csv'
    filename = sys.argv[2]
    file = open(filename, "w", newline = '')
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Counts"])
    print(f"There was a count detected at {time.time()}" )
    global counts
    while counts<timing:
        counts = counts + 1
        timestamp = time.time()
        print(f"There was a count detected at", timestamp)
        if counts%interval==0:
            actual_count = counts/interval
            writer.writerow([actual_count, timestamp])
    
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback)

while True:
    time.sleep(10)  # wait 10 ms to give CPU chance to do other things
    print(f"Number of Counts is {counts}")




