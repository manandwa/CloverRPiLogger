# Mobin Anandwala
# 3/15/2017
# This script will test generating the csv files and overwriting them
# Updated 3/16/2017 with date added on to file

import csv
import datetime as dt

def generate_filename():
    file_name = '/home/pi/log'
    today = dt.date.today()
    us_date = dt.datetime.strftime (today,'%m-%d-%Y')
    log_file = file_name + '-' + us_date + '-' + 'CLOVER' + '.csv'
    return log_file

def generate_filename_backup():
    file_name = '/home/pi/log'
    today = dt.date.today()
    us_date = dt.datetime.strftime (today,'%m-%d-%Y')
    log_file_backup = file_name + '-' + us_date + '-' + 'CLOVER' + '[BACKUP]' + '.csv'
    return log_file_backup

def create_log_file():
    log_type = generate_filename()
    log_file = open(log_type,'w')
    log_file_writer = csv.writer(log_file)
    log_file_writer.writerow(['Time','Voltage','Curremt','Status','Notes'])
    return log_type

def create_backup_log():
    log_file_backup = generate_filename_backup()
    log_file_backup_writer = csv.writer(log_file_backup)
    log_file_backup_writer.writerow(['Time','Voltage','Curremt','Status','Notes'])
    return log_type_backup

def set_backup(log_type_backup):
    backup_is_on = True
    log_file_backup = open(log_type_backup,'w')
    log_file_backup_csv = csv.writer(log_file_backup)
    log_file_backup_csv.writerow(['BACKUP ON'])
    log_file_backup_csv.writerow(['Time','Voltage','Curremt','Status','Notes'])

def write_data(now,v1,c1,log_type,status):
    log_file = open(log_type,'a')
    writer = csv.writer(log_file)
    writer.writerow([str(now),str(v1),str(c1),status,'Testing Device'])

