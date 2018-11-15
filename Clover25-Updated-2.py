# Author: Mobin Anandwala
# Date Created: 3/28/2017
# Purpose: To Log current and voltage using the explorerhat
# Update from Clover24.py change thresholds and logic
# Date Updated: 3/29/2017 added Exosite functionality using original functions and also added stuck logic based on CLOVER20.py code
# Date Updated: 3/31/2017 added genstring and write string functions to record stuck

import explorerhat as eh
from csv_api import generate_filename, generate_filename_backup, create_log_file, create_backup_log, write_data, set_backup, genLogString, writeLogString
from exosite_upload_api import genPiNumber, uploadData, generateParams
from time import sleep
from datetime import date, datetime, timedelta
from os import path

# turn off LED
eh.light.off()
gain = 100
sample_rate = 10

# Generate Log file names
log_file_name = generate_filename()
log_file_name_backup = generate_filename_backup()

# Set Pi Number
PiNumber = 1

# Thresholds

# Radio current threshold
radio_on_min = 35.0
radio_on_max = 40.0

# Cloud write thresholds
cloud_write_min = 75.0
cloud_write_max = 120.0

if path.exists(log_file_name):
    print('log exists')
    pass
else:
    print('Generating new log!')
    log_file = create_log_file()


# set delay delta
stuck_delay = 30
stuck_delta = timedelta(seconds=30)

# Stuck Variable
is_stuck = False # default is not stuck

# set statuses
radio_on = 'RADIO'
cloud_write = 'CLOUD_WRITE'

# Current read function
def read_current():
    for i in range(sample_rate):
        data = eh.analog.read()
    current = data['one']*gain
    return current

# Voltage read function
def read_voltage():
    for i in range(sample_rate):
        data = eh.analog.read()
    voltage = data['two']*10 # Hardware design
    return voltage

while True:
    eh.light.toggle()

    # Get current system time
    system_time = datetime.time(datetime.now())
    #print('Time is ' + system_time.strftime('%H:%M:%S'))

    c1 = read_current()
    print('Current is = ' + str(c1))
    sleep(1)

    v1 = read_voltage()
    print('Voltage is = ' + str(v1))
    sleep(1)

    if (c1 >= radio_on_min and c1 <= radio_on_max):
        if path.exists(log_file_name):
            write_data(datetime.now().replace(microsecond=0),v1,c1,log_file_name,radio_on)
            params = generateParams(PiNumber,c1,v1,radio_on)
            try:
                response = uploadData(params)
            except Exception,e:
                str(e)
                print(str(e))
                print('Lost Connection')
                set_backup(log_file_name_backup)

        else:
            write_data(datetime.now().replace(microsecond=0),v1,c1,log_file_name,radio_on)
            params = generateParams(PiNumber,c1,v1,radio_on)
            try:
                response = uploadData(params)
            except Exception,e:
                str(e)
                print(str(e))
                print('Lost Connection')
                set_backup(log_file_name_backup)

    if (c1 >= cloud_write_min and c1 <= cloud_write_max):
        if path.exists(log_file_name):
            write_data(datetime.now().replace(microsecond=0),v1,c1,log_file_name,cloud_write)
            params = generateParams(PiNumber,c1,v1,cloud_write)
            try:
                response = uploadData(params)
            except Exception,e:
                str(e)
                print(str(e))
                print('Lost Connection')
                set_backup(log_file_name_backup)

        else:
            write_data(datetime.now().replace(microsecond=0),v1,c1,log_file_name,cloud_write)
            params = generateParams(PiNumber,c1,v1,cloud_write)
            try:
                response = uploadData(params)
            except Exception,e:
                str(e)
                print(str(e))
                print('Lost Connection')
                set_backup(log_file_name_backup)


    else:
        print('Normal!')
        if path.exists(log_file_name):
            write_data(datetime.now().replace(microsecond=0),v1,c1,log_file_name,'Nothing to report')
            params = generateParams(PiNumber,c1,v1,'Nothing to report')
            try:
                response = uploadData(params)
            except Exception,e:
                str(e)
                print(str(e))
                print('Lost Connection')
                set_backup(log_file_name_backup)

        else:
            write_data(datetime.now().replace(microsecond=0),v1,c1,log_file_name,'Nothing to report')
            params = generateParams(PiNumber,c1,v1,'Nothing to report')
            try:
                response = uploadData(params)
            except Exception,e:
                str(e)
                print(str(e))
                print('Lost Connection')
                set_backup(log_file_name_backup)

    # Stuck check (if current is within range for 30 seconds or longer)
##    start_time = datetime.now().replace(microsecond=0) # Get current system time
##    final_time = start_time + stuck_delta
    # Read current and voltage again
    c1 = read_current()
    print('Checking current c1 = ' + str(c1))
    sleep(1)
    v1 = read_voltage()
    print('Checking voltage v1 = ' + str(v1))
    sleep(1)
    for i in range(stuck_delay): # counter to determine if current lasted long enough
        if (c1 >= radio_on_min and c1 <= radio_on_max):
            write_data(datetime.now().replace(microsecond=0),v1,c1,log_file_name,radio_on)
            params = generateParams(PiNumber,c1,v1,radio_on)
            try:
                response = uploadData(params)
            except Exception,e:
                str(e)
                print(str(e))
                print('Lost Connection')
                set_backup(log_file_name_backup)

                # the previous section uploaded the values to exosite (based on CLOVER20.py logic loop)
            sleep(1)

            # Stuck
            is_stuck = True
            c1 = read_current()
            v1 = read_voltage()
        else:
            is_stuck = False

    # Note time here
    start_time = datetime.now().replace(microsecond=0)
    # Stuck now
    while (is_stuck and (c1 >= radio_on_min and c1 <= radio_on_max)):
        eh.light.on()

        # read inputs
        c1 = read_current()
        v1 = read_voltage()

        write_data(datetime.now().replace(microsecond=0),v1,c1,log_file_name,'STUCK RADIO')
        params = generateParams(PiNumber,c1,v1,'STUCK RADIO')
        try:
            response = uploadData(params)
        except Exception,e:
            str(e)
            print(str(e))
            print('Lost Connection')
            set_backup(log_file_name_backup)

        if (c1 <= radio_on_min or c1 >= radio_on_max):
            break

    # Note final time
    final_time = datetime.now().replace(microsecond=0)
    stuck_diff = final_time - start_time

    if (stuck_diff < stuck_delta):
        pass
    else:
         logstring_stuck = genLogString('','','',('STUCK RADIO ' + str(stuck_diff)),'RADIO STUCK')
         writeLogString(logstring_stuck,log_file_name)
         params = generateParams(PiNumber,c1,v1,('STUCK RADIO FOR ' + str(stuck_diff)))
         try:
             response=uploadData(params)
         except Exception,e:
             str(e)
             print(str(e))
             print('Lost Connection')
             set_backup(log_file_name_backup)


    is_stuck = False
    eh.light.off()

# Adding same logic for cloud write
# Read current and voltage again
c1 = read_current()
print('Checking current c1 = ' + str(c1))
sleep(1)
v1 = read_voltage()
print('Checking voltage v1 = ' + str(v1))
sleep(1)
for i in range(stuck_delay): # counter to determine if current lasted long enough
    if (c1 >= cloud_write_min and c1 <= cloud_write_max):
        write_data(datetime.now().replace(microsecond=0),v1,c1,log_file_name,radio_on)
        params = generateParams(PiNumber,c1,v1,cloud_write)
        try:
            response = uploadData(params)
        except Exception,e:
            str(e)
            print(str(e))
            print('Lost Connection')
            set_backup(log_file_name_backup)

            # the previous section uploaded the values to exosite (based on CLOVER20.py logic loop)
        sleep(1)

        # Stuck
        is_stuck = True
        c1 = read_current()
        v1 = read_voltage()
    else:
        is_stuck = False

# Note time here
start_time = datetime.now().replace(microsecond=0)
# Stuck now
while (is_stuck and (c1 >= cloud_write_min and c1 <= cloud_write_max)):
    eh.light.on()

    # read inputs
    c1 = read_current()
    v1 = read_voltage()

    write_data(datetime.now().replace(microsecond=0),v1,c1,log_file_name,'STUCK CLOUD WRITE')
    params = generateParams(PiNumber,c1,v1,'STUCK CLOUD WRITE')
    try:
        response = uploadData(params)
    except Exception,e:
        str(e)
        print(str(e))
        print('Lost Connection')
        set_backup(log_file_name_backup)

    if (c1 <= cloud_write_min or c1 >= cloud_write_max):
        break

# Note final time
final_time = datetime.now().replace(microsecond=0)
stuck_diff = final_time - start_time

if (stuck_diff < stuck_delta):
    pass
else:
     logstring_stuck = genLogString('','','',('STUCK CLOUD WRITE ' + str(stuck_diff)),'CLOUD WRITE STUCK')
     writeLogString(logstring_stuck,log_file_name)
     params = generateParams(PiNumber,c1,v1,('STUCK CLOUD WRITE FOR ' + str(stuck_diff)))
     try:
         response=uploadData(params)
     response = uploadData(params)


is_stuck = False
eh.light.off()










##    while (c1 >= radio_on_min and c1 <= radio_on_max and (final_time > datetime.now())):
##        write_data(datetime.now().replace(microsecond=0),v1,c1,log_file_name,'STUCK RADIO')
##        if (c1 <= radio_on_min or c1 >= radio_on_max):
##            break
