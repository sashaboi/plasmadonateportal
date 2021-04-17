from django.test import TestCase
from geopy.geocoders import Nominatim
from geopy import distance
import folium 

m = folium.Map(location =[18.456079, 73.786037], zoom_start = 7)
folium.Marker(location =[18.456079, 73.786037]).add_to(m)
folium.Marker(location =[19.456079, 74.786037]).add_to(m)
m.save('map.html')

