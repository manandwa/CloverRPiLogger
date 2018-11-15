# Author: Mobin Anandwala
# Date created: 3/17/2017
# Purpose: Log current for Onelink Smoke and Carbon Monoxide Alarm
# Note: This logger code will not display on the exosite dashboard

import explorerhat as eh
from csv_api import generate_filename, create_log_file, write_data
from time import sleep
from datetime import date, datetime
import os

# Generate log file names
log_file_name = generate_filename()

# Setup thresholds
low_sector = 3
medium_sector = 20
high_sector = 90

# Setup Status
low_status = 'LOW'
med_status = 'MED'
high_status = 'HIGH'

# gain from op amp current logging circuit and reset LED
gain = 100
eh.light.off()

# sample rate
sample_rate = 10

# Check for existance of earlier log (Comment out the print statements for final deployment)
if os.path.exists(log_file_name):
    print('Log Exists!')
    pass
else:
    print('No Log Exists!')
    print('Generating new log')
    log_file = create_log_file()

# Current Read function
def read_current():
    for i in range(sample_rate):
        data = eh.analog.read()
    current = data['one']*gain
    return current

# Voltage Read function
def read_voltage():
    for i in range(sample_rate):
        data = eh.analog.read()
    voltage = data['two']*10 # This is to account for circuit design
    return voltage

# start logging
print('Start Logging')
eh.light.on()

# Main loop
while True:
    eh.light.toggle()
    sleep(0.5)
    now = datetime.now()
    c1 = read_current()
    v1 = read_voltage()
    print('Current is = ' + str(c1) + ' mA')
    print('Voltage is = ' + str(v1) + ' V')
    sleep(1)
    if (c1 < low_sector):
        if os.path.exists(log_file_name):
            write_data(now,v1,c1,log_file_name,status='Nothing to report')
        else:
            write_data(now,v1,c1,log_file,status='Nothing to report')
    while (c1 < low_sector):
        eh.light.on()
        sleep(1)
        break
    if (c1 >= low_sector and c1 < medium_sector):
        if os.path.exists(log_file_name):
            write_data(now,v1,c1,log_file_name,low_status)
        else:
            write_data(now,v1,c1,log_file,low_status)
    while (c1 >= low_sector and c1 < medium_sector):
        eh.light.on()
        sleep(1)
        break
    if (c1 >= medium_sector and c1 < high_sector):
        if os.path.exists(log_file_name):
            write_data(now,v1,c1,log_file_name,med_status)
        else:
            write_data(now,v1,c1,log_file,med_status)
    while (c1 >= medium_sector and c1 < high_sector):
        eh.light.on()
        sleep(1)
        break
    if (c1 >= high_sector):
        if os.path.exists(log_file_name):
            write_data(now,v1,c1,log_file_name,high_status)
        else:
            write_data(now,v1,c1,log_file,high_status)
    while (c1 >= high_sector):
        eh.light.on()
        sleep(1)
        break
    
        
        




