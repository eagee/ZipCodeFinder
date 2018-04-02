# ZipCodeFinder
A dinky little python script to obtain the missing zip code from a set of CSV data and output new CSV data to the console.
The script uses the google maps api to make periodic requests using the address information available,
and then populates console output (which can be redirected to a new csv file) with the new zip and fields
we wish to format or use.

Python 3 is required to run this script along with the 'requests' library available here: http://docs.python-requests.org/

Usage:
py ZipCodeFinder.py > Output.csv
