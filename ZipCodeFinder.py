import csv
import requests
import json
import time
import logging
import ctypes
import logging

# output "logging" messages to DbgView via OutputDebugString (Windows only!)
OutputDebugString = ctypes.windll.kernel32.OutputDebugStringW

class DbgViewHandler(logging.Handler):
    def emit(self, record):
        OutputDebugString(self.format(record))

log = logging.getLogger("output.debug.string.example")

def config_logging():
    # format
    fmt = logging.Formatter(fmt='%(asctime)s.%(msecs)03d [%(thread)5s] %(levelname)-8s %(funcName)-20s %(lineno)d %(message)s', datefmt='%Y:%m:%d %H:%M:%S')
 
    log.setLevel(logging.DEBUG)

    # "OutputDebugString\DebugView"
    ods = DbgViewHandler()
    ods.setLevel(logging.DEBUG)
    ods.setFormatter(fmt)
    log.addHandler(ods)
  
    # "Console"
    con = logging.StreamHandler()
    con.setLevel(logging.DEBUG)
    con.setFormatter(fmt)
    log.addHandler(con)
    log.propagate = False

def main():
    #http://maps.googleapis.com/maps/api/geocode/json?address=10579+Pekin+Rd,+Newbury,+OH&sensor=true_or_false        
    fileReader = csv.reader(open("Applicants.csv"), delimiter=",")
    
    # Read out the header field, fields are aligned as follows
    # FirstName = 0
    # LastName = 1
    # Address = 2
    # City = 3
    # Phone = 5
    # Email = 6
    # Venue = 7
    readHeader = next(fileReader)
    
    # Print out the header for the new file
    print ("FirstName,LastName,Address,City,State,Zip,Phone,Email,Group,Group")
    
    
    for row in fileReader:
            
        time.sleep(3)
        # Get all address information from what we have now, request json from google that will include the zip, and output it to the console
        address = row[2]
        address.replace(" ", "+")
        
        city = row[3]
        city.replace(" ", "+")
        
        state = 'OH'
        
        requestUrl = 'http://maps.googleapis.com/maps/api/geocode/json?address=%street%,+%city%,+%state%&sensor=true_or_false'
        requestUrl = requestUrl.replace('%street%', address)
        requestUrl = requestUrl.replace('%city%', city)
        requestUrl = requestUrl.replace('%state%', state)
        log.warn((requestUrl))
        r = requests.get(requestUrl);
        
        zip = '44118'
        
        jsonObject = r.json()
        
        # Access data returned to us in json by iterating through the address_components and finding the postal_code element
        # so that we can assign it to the zip value. If google rejects our request, wait 10 seconds and then try again
        # (requests are time limited without an api key)
        while (len(jsonObject['results']) == 0):
            log.warn((jsonObject))
            log.warn((jsonObject['status']));
            
            if jsonObject['status'] == 'OVER_QUERY_LIMIT':
                time.sleep(10)
                r = requests.get(requestUrl);
                jsonObject = r.json() 
            if jsonObject['status'] == 'ZERO_RESULTS':            
                time.sleep(5)
                print('WARNING Next record may have an incorrect zip code!')
                break
                
        if len(jsonObject['results']) > 0:
            for element in jsonObject['results'][0]['address_components']:
                if element['types'][0] == 'postal_code':
                    zip = element['short_name']
        
        # Output the address information including the zip code!
        log.warn((row[0] + ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + state + ',' + zip + ',' + row[5] + ',' + row[6] + ',' + 'Artist,Triennial Applicant'))
        print (row[0] + ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + state + ',' + zip + ',' + row[5] + ',' + row[6] + ',' + 'Artist,Triennial Applicant')


if __name__ == '__main__':
    config_logging()
  
main()