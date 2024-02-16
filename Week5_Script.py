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

run_time = 10
run_time = int(sys.argv[1])

filename = 'data.csv'
filename = sys.argv[2]
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
             "PM10"]
writer.writerow(meta_data)

now = start_time #time.time()
while (now-start_time) < run_time:
    time.sleep(1)
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
                 aqdata['pm100 standard']]
    print(data_list)
    writer.writerow(data_list)
    
file.close()

