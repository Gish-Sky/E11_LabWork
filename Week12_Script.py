import adafruit_bme680
import time
import board
import board
import busio
import sys
import random
import time
import csv
import serial
import RPi.GPIO as GPIO

counts = 0
timing = 120
interval = 2
start = time.time()
dif = 0

#Weather Sensor Data

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()   # uses board.SCL and board.SDA
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25
start_time = time.time() #used to be yeet

#Air Quality Sensor Data

reset_pin = None

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)

filename = 'data.csv'
filename = sys.argv[1]
file = open(filename, "w", newline = '')
writer = csv.writer(file)

meta_data = ["Time", 
             "Temperature", 
             "Gas",
             "Relative_Humididty",
             "Pressure",
             "Altitude",
             "PM1", 
             "PM2.5", 
             "PM10",
             "Counts"]
writer.writerow(meta_data)

now = start_time #time.time()
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
    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue
    now = time.time()
    data_list = [now, 
                 bme680.temperature, 
                 bme680.gas, 
                 bme680.relative_humidity, 
                 bme680.pressure, 
                 bme680.altitude, 
                 aqdata["pm10 standard"], 
                 aqdata['pm25 standard'], 
                 aqdata['pm100 standard'],
                 counts]
    print(data_list)
    writer.writerow(data_list)
file.close()
