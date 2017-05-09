import os.path
import sys
import json
import apiai
import pprint


CLIENT_ACCESS_TOKEN = os.environ['ROUTE_PLANNER_APIAI_TOKEN']

ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)


def query_apiai(query_str, session_id):
    request = ai.text_request()
    request.lang = 'en'
    request.session_id = session_id
    request.query = query_str

    response = request.getresponse()
    resp_read = response.read()
    resp_dict = json.loads(resp_read)
    return resp_dict

def parse_find_place(response):
    
    resp_data = response['result']['parameters']
    place = dict()
    place['place'] = resp_data['place_and_city']['place_generic']
    place['city'] = resp_data['place_and_city']['geo-city']
    place['state'] = resp_data['place_and_city']['geo-state-us']

    return place

def parse_plan_action(response):
    
    resp_data = response['result']['parameters']
    output_d = dict()

    output_d['start_addr'] = resp_data['start_place']['address']
    output_d['end_addr'] = resp_data['end_place']['address']

    inter_list = list()
    if 'no_stops' in resp_data['inter_places'][0]:
        return output_d

    num_inter = len(resp_data['inter_places'])
    if num_inter > 0:
        pprint.pprint(resp_data['inter_places'])
        for inter in resp_data['inter_places']:
            place_d = dict()
            place_d['city'] = inter['geo-city']
            place_d['place'] = inter['place_generic']
            place_d['state'] = inter['geo-state-us']
            inter_list.append(place_d) 
    output_d['inter_places'] = inter_list
    
    return output_d


def parse_result(response):
    
    if response['result']['action'] == "plan_route":
        print "plan_route"
        return parse_plan_action(response)
    elif response['result']['action'] == "find_place":
        print "find_place"
        return parse_find_place(response)
    else:
        print "Not yet defined"
        return None
    
