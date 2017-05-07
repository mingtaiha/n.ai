from pprint import pprint
#import app, db
import googlemaps
import time


test_start = "110 Frelinghuysen Road Piscataway, NJ 08854-8019"


test_stores = [ "424 Raritan Ave, Highland Park, NJ 08904",
                "100 Grand Ave, North Brunswick Township, NJ 08902",
                "14 W Prospect St, East Brunswick, NJ 08816"
                ]

test_delay = 0

def get_distance_matrix(start, places, end, depart_delay):

    # :param start: Address as a string.
    #   E.g. '1600 Pennsylvania Ave NW, Washington, DC 20006'

    # :param places: List of Addresses, each element as a string

    # :depart_delay: A nonnegative amount of time (in seconds)
    #       and used to query traffic conditions of when user
    #       leaves relative to when the function is called

    # Generates a distance and time matrix between start locations and stores
    # Matrix is represented as a matrix of (duration_in_traffic, distance)
    # The rows represent starting locations, the columns represent ending
    # locations. The indexing format always follows [start, *stores]

    # Create Google Maps client with Server Key
    #gmaps = googlemaps.Client(key=app.config["GOOGLE_MAPS_API_KEY"])
    GOOGLE_MAPS_API_KEY = "AIzaSyC7gFkRVm3oUKLC3ZTNmuSAxSnXxXhGh0M"
    gmaps = googlemaps.Client(GOOGLE_MAPS_API_KEY)

    # Create list of lat/lng for start location and stores
    start_list = list()
    gcode_start = gmaps.geocode(start)
#    pprint(gcode_start)
    loc_list = list()
    loc_list.append(gcode_start[0]['geometry']['location'])

    print start, places, end
    if len(places) > 0:
        for place in places:
            pprint(place)
            gcode_place = gmaps.geocode(place)
#            pprint(gcode_place)
            loc_list.append(gcode_place[0]['geometry']['location'])

    gcode_end = gmaps.geocode(end)
    loc_list.append(gcode_end[0]['geometry']['location'])

    #pprint(start_list)

    # Setting Departure Time
    depart_time = int(time.time()) + depart_delay

    # Get Google Maps client to make distance matrix
    d_mat = gmaps.distance_matrix(loc_list, loc_list, departure_time=depart_time, mode='driving', units='miles')

    #pprint(d_mat)

    # Cleaning distance matrix to be a list of list of (duration_in_traffic, distance)
    # The row index corresponds to the start address, col index corresponds to end address
    # Matrix is symmetric
    distance_matrix = list()
    for src in range(len(d_mat['rows'])):
        tmp_list = list()
        for dst in range(len(d_mat['rows'][src]['elements'])):
            tmp_list.append((d_mat['rows'][src]['elements'][dst]['duration_in_traffic']['value'] / 60., \
                            d_mat['rows'][src]['elements'][dst]['distance']['value'] / 1000.))
        distance_matrix.append(tmp_list)

#    pprint(distance_matrix)
    return distance_matrix


def get_path(start, places, end, time_delay=0, dist_mat=None):

    # Returns a cycle which starts at `start` and goes to all stores in the stores list
    # Generates shortest Hamiltonian path greedily using nearest neighbors, then adds path
    # from last store visited to start
    
    if dist_mat == None:
        dist_mat = get_distance_matrix(start, places, end, time_delay)
    
    path = [0]
    cost = list()

    num_locations  = len(dist_mat)
    next_loc = 0
    min_dist = 1000000000
    metric = 0      # 0 - Time, 1 - Distance
    src = 0 

    while len(path) < (num_locations - 1):
        #pprint(path)
        #print "Starting at {0}".format(src)
        for dst in range(len(dist_mat) - 1):
            if dst not in path:
                if min_dist > dist_mat[src][dst][metric]:
                    next_loc = dst
                    min_dist = dist_mat[src][dst][metric]
            else:
                pass
                #print "Already looked at {0}".format(dst)
        src = next_loc
        path.append(next_loc)
        cost.append(min_dist)
        next_loc = 0
        min_dist = 1000000000

    path.append(len(dist_mat) - 1)
    cost.append(dist_mat[path[-2]][path[-1]][metric])
    
#    pprint(path)
#    pprint(cost)
    return path, cost




if __name__ == "__main__":

    get_path(test_start, test_stores, time_delay=test_delay, cycle=1)

    print "OK"
