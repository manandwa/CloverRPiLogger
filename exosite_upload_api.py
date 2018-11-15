# Mobin Anandwala
# 3/16/2017
# This will house the exosite upload functions
# The point is that it makes the whole logger code modular

import httplib
import urllib

# Exosite Information
Exosite_Server = 'm2.exosite.com'
Exosite_URL = '/api:v1/stack/alias'
Exosite_CIK = 'f7302c574a9cb0a195100ddbe3ca98cf80d08634'
Exosite_Header = {'X-Exosite-CIK': Exosite_CIK, 'content-type': 'application/x-www-form-urlencoded; charset=utf-8'}

# Generate a pi number to upload data
def genPiNumber(PiNumber):
    ExoPi = 'Pi' + ' ' + str(PiNumber)
    return ExoPi

# Upload your data (based on exosite example python code)
def uploadData(data):
    conn = httplib.HTTPConnection(Exosite_Server)
    conn.request("POST",Exosite_URL,data,Exosite_Header)
    response = conn.getresponse()
    return response

# Generate parameters (based on exosite example python)
def generateParams(PiNumber,Current,Voltage,Event):
    ExoPi = genPiNumber(PiNumber)
    params = urllib.urlencode({(ExoPi + ' ' + 'Current'): Current, (ExoPi + ' ' + 'Voltage'): Voltage, (ExoPi + ' ' + 'Event'): Event})
    return params
