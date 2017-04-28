from googleplaces import GooglePlaces, types, lang
from pprint import pprint
import sys
import utils

YOUR_API_KEY = "AIzaSyCQENSbRFfd9_lGuqoXf2icRgtSvED-WHI"
RADIUS = 10000 # in meters

google_places = GooglePlaces(YOUR_API_KEY)


def get_gplaces_results(place, city, state):
    # You may prefer to use the nearby_search API, instead.
    city_state = city + ", " + state
    query_result = google_places.text_search(query=place, location=city_state, radius=RADIUS)
    # If types param contains only 1 item the request to Google Places API
    # will be send as type param to fullfil:
    # http://googlegeodevelopers.blogspot.com.au/2016/02/changes-and-quality-improvements-in_16.html

    #pprint(query_result.places)
    if len(query_result.places) == 0:
        return None     #No such places within RADIUS km of city
    else:
        places_in_city = list()
        for place in query_result.places:
            place_d = dict()

            # The following method has to make a further API call.
            place.get_details()
            if (utils.state_to_abbr[state] in place.formatted_address) and (city in place.formatted_address):
                place_d['lat'] = float(place.geo_location['lat'])
                place_d['long'] = float(place.geo_location['lng'])
                place_d['google_places_id'] = place.place_id
                place_d['address'] = place.formatted_address
                place_d['name'] = place.name
                places_in_city.append(place_d)
                break

        if len(places_in_city) == 0:
            return None     #No such places in city but are within RADIUS km
        else:
            return places_in_city[0]
        
