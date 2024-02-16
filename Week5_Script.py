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
yeet = time.time()
while (time.time()-yeet) < 30:
    print("\nTemperature: %0.1f C" % bme680.temperature)
    print("Gas: %d ohm" % bme680.gas)
    print("Humidity: %0.1f %%" % bme680.relative_humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude = %0.2f meters" % bme680.altitude)
    print("Start time: " + str(yeet) + ", Current time: " + str(time.time()))

    time.sleep(2)
#____________________________________________________________________________
    
#Air Quality Sensor Data

reset_pin = None

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)

print("Found PM2.5 sensor, reading data...")

# This tracks our time and creates a csv
yeet = time.time()
#this gives our csv file column names
meta_data = ["Time", "PM1", "PM2.5", "PM10"] #this is our column value
#this names the file and sets a standard for when a new line of data is recorded
file = open("aq_data.csv", "w", newline='')
#the following creates a new row/creates the file
writer = csv.writer(file)
writer.writerow(meta_data)
while (time.time()-yeet) < 30:
    time.sleep(1)

    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    print()
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")
    #this records our current time
    now = time.time()
    #this records our data into an object
    data_out = [now, aqdata["pm10 standard"], aqdata['pm25 standard'], aqdata['pm100 standard']]
    #this adds our data to the csv file we made
    writer.writerow(data_out)