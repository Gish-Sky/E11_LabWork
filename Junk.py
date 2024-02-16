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

print(sys.argv)

start_time = time.time()
run_time = 10
run_time = int(sys.argv[1])

filename = 'data.csv'
filename = sys.argv[2]
file = open(filename, "w", newline = '')
writer = csv.writer(file)

meta_data = ["Time", "Data"]
writer.writerow(meta_data)

now = time.time()
while (now-start_time) < run_time:
    time.sleep(1)
    now = time.time()
    data_list = [now,data_out]
    print(data_list)
    writer.writerow(data_list)