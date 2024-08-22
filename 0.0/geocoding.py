import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyDLNSf4GjXxiL1xnhcKddITADn7AlJLsWY')


# Geocoding an address
geocode_result = gmaps.geocode('Bismillah Tower, Haji market, Balughat, Dhaka')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
print(geocode_result)


