#!/usr/bin/python

import sqlite3
from geopy.geocoders import Nominatim
def position():

    #conn = sqlite3.connect('travel.db')


    geolocator = Nominatim()
    location = geolocator.geocode(raw_input('enter address'))
    print(location.address)
#Flatiron Building, 175, 5th Avenue, Flatiron, New York, NYC, New York, ...
    print((location.latitude, location.longitude))
    lat= location.latitude
    lon= location.longitude

    conn.execute('''CREATE TABLE position6
        (
        latitude           TEXT    NOT NULL,
        longitude           text     NOT NULL);''')
	   
    conn.execute("INSERT INTO position6 (latitude,longitude) \
      VALUES (?,?)", (lat,lon));

    conn.commit()

    cursor = conn.execute("SELECT latitude,longitude  from position6")
    for row in cursor:
       print "latitude = ", row[0]
       print "longitude = ", row[1]
  


    conn.close()
