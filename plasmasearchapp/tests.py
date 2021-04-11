from django.test import TestCase
from geopy.geocoders import Nominatim
from geopy import distance





def distancebetween(place1,place2):
    
    dist = distance.distance(place1, place2).km , "kms"

    return dist