from pprint import pprint
import googlemaps
import time


def gen_distance_matrix(start, stores, depart_delay):

    # :param start: Address as a string. 
    #   E.g. '1600 Pennsylvania Ave NW, Washington, DC 20006'

    # :param stores: List of Addresses, each element as a string

    # :depart_delay: A nonnegative amount of time (in seconds)
    #       and used to query traffic conditions of when user
    #       leaves relative to when the function is called

    # Generates a distance and time matrix between start locations and stores
    # Matrix is represented as a matrix of (duration_in_traffic, distance)
    # The rows represent starting locations, the columns represent ending
    # locations. The indexing format always follows [start, *stores]

    # Create Google Maps client with Server Key
    gmaps = googlemaps.Client(key='AIzaSyC7gFkRVm3oUKLC3ZTNmuSAxSnXxXhGh0M')

    # Create list of lat/lng for start location and stores
    loc_list = list()
    gcode_start = gmaps.geocode(start)
    loc_list.append(gcode_start[0]['geometry']['location'])

    for store in stores:
        gcode_store = gmaps.geocode(store)
        loc_list.append(gcode_store[0]['geometry']['location'])

    pprint(loc_list)

    # Setting Departure Time
    depart_time = int(time.time()) + depart_delay

    # Get Google Maps client to make distance matrix
    d_mat = gmaps.distance_matrix(loc_list, loc_list, departure_time=depart_time, mode='driving', units='miles')

    pprint(d_mat)

    # Cleaning distance matrix to be a list of list of (duration_in_traffic, distance)
    distance_matrix = list()
    for src in range(len(d_mat['rows'])):
        tmp_list = list()
        for dst in range(len(d_mat['rows'][src]['elements'])):
            tmp_list.append((d_mat['rows'][src]['elements'][dst]['duration_in_traffic']['value'] / 60., \
                            d_mat['rows'][src]['elements'][dst]['distance']['value'] / 1000.))
        distance_matrix.append(tmp_list)

    return distance_matrix


if __name__ == "__main__":

    print "OK"
