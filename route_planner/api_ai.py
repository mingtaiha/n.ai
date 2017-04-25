import os.path
import sys
import json
import apiai


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


def parse_plan_action(response):
    
    resp_data = response['result']['parameters']
    output_d = dict()

    output_d['start_addr'] = resp_data['start_place']['address']
    output_d['end_addr'] = resp_data['end_place']['address']

    inter_list = list()
    num_inter = len(resp_data['inter_places'])
    if num_inter > 0:
        for inter in resp_data['inter_places']:
            city = inter['place_and_city']['geo-city']
            place = inter['place_and_city']['place_generic']
            inter_list.append(place + " in " + city) 
    output_d['inter_places'] = inter_list
    
    return output_d


def parse_result(response):
    
    if response['result']['action'] == "plan_route":
        print "plan_route"
        return parse_plan_action(response)
    else:
        print "Not yet defined"
        return None
    
