import csv
import time
meta_data = ["Time", "PM2.5", "PM10"] #this is our column values
file = open("aq_data.csv", "w", newline='')
writer = csv.writer(file)
writer.writerow(meta_data)
while True:
    now = time.time()
    data = pm25.read()
    data_out [now, data["pm 2.5"], data ['pm 10']]
    writer.writerow(data_out)