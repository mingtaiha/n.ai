import os.path
import sys
import json
import apiai
import pprint


CLIENT_ACCESS_TOKEN = os.environ['AMAZON_BUYER_APIAI_TOKEN']

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

def parse_buy_items(response):
    
    resp_data = response['result']['parameters']['item']
    return resp_data

def parse_result(response):
    
    if response['result']['action'] == "buy_items":
        print "buy_items\n"
        return parse_plan_action(response)
    else:
        print "Not yet defined"
        return None
    
