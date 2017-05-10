import os.path
import sys
import json
import apiai
import pprint


CLIENT_ACCESS_TOKEN = os.environ['NUTRITION_AI_APIAI_TOKEN']

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

def parse_recipe_fields(response):
    
    protein_cuisine_dict = dict()
    protein_cuisine_dict['protein'] = response['result']['parameters']['protein']
    if response['result']['parameters']['cuisine']:
        protein_cuisine_dict['cuisine'] = response['result']['parameters']['cuisine']
    return protein_cuisine_dict

def parse_result(response):
    
    if response['result']['action'] == "get_recipe":
        print "get_recipe\n"
        return parse_recipe_fields(response)
    else:
        print "Not yet defined"
        return None
    
