
#http://maps.googleapis.com/maps/api/geocode/json?address=10579+Pekin+Rd,+Newbury,+OH&sensor=true_or_false
import csv
import requests
import json
import time

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
     	
    time.sleep(1)
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
    #print((requestUrl))
    r = requests.get(requestUrl);
    
    zip = '44118'
    
    jsonObject = r.json()
    
    # Access data returned to us in json by iterating through the address_components and finding the postal_code element
    # so that we can assign it to the zip value
    while (len(jsonObject['results']) == 0):
        time.sleep(10)
        r = requests.get(requestUrl);
        jsonObject = r.json()
        #print((jsonObject))
    
    if len(jsonObject['results']) > 0:
        for element in jsonObject['results'][0]['address_components']:
            if element['types'][0] == 'postal_code':
                zip = element['short_name']
    
    # convert our json to an object and iterate through it until we find the zip code

    #print ((zip))
    # Output the address information including the zip code!
    print (row[0] + ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + state + ',' + zip + ',' + row[5] + ',' + row[6] + ',' + 'Artist,Triennial Applicant')
