import googlemaps
from datetime import datetime
import folium

gmaps = googlemaps.Client(key='AIzaSyDLNSf4GjXxiL1xnhcKddITADn7AlJLsWY')


# Geocoding an address
geocode_result = gmaps.geocode('Bismillah Tower, Haji market, Balughat, Dhaka')

# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
# print(geocode_result)

def extract_coordinates(data):
    coordinates = []
    for location in data:
        try:
            lat = location['geometry']['location']['lat']
            lng = location['geometry']['location']['lng']
            coordinates.append((lat, lng))
        except KeyError:
            try:
                lat = location['geometry']['bounds']['northeast']['lat']
                lng = location['geometry']['bounds']['northeast']['lng']
                coordinates.append((lat, lng))
            except KeyError:
                continue
    return coordinates



print(extract_coordinates(geocode_result))



def visualize_points(points):
    m = folium.Map(location=[23.8293523, 90.390434], zoom_start=12)

    for point in points:
        folium.CircleMarker([point[0], point[1]], radius=3).add_to(m)

    return m

points = extract_coordinates(geocode_result)
m = visualize_points(points)
m.save('points_map.html')