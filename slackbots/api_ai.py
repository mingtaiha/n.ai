import os.path
import sys
import json
import apiai
import pprint


CART_ONLINE_CLIENT_ACCESS_TOKEN = os.environ['SHOPPING_CART_ONLINE_APIAI_TOKEN']
CART_OFFLINE_CLIENT_ACCESS_TOKEN = os.environ['SHOPPING_CART_OFFLINE_APIAI_TOKEN']

ai_online = apiai.ApiAI(CART_ONLINE_CLIENT_ACCESS_TOKEN)
ai_offline = apiai.ApiAI(CART_OFFLINE_CLIENT_ACCESS_TOKEN)


def query_apiai(query_str, session_id, cart_intent):
	
	if cart_intent == "online":
		request = ai_online.text_request()
	elif cart_intent == "offline":
		request = ai_offline.text_request()
	else:
		return None

	request.lang = 'en'
	request.session_id = session_id
	request.query = query_str

	response = request.getresponse()
	resp_read = response.read()
	resp_dict = json.loads(resp_read)
	return resp_dict

def parse_cart_items_buy(response, cart_intent):
    
    if cart_intent == "online":
        resp_data = response['result']['parameters']['items_online']
    elif cart_intent == "offline":
        resp_data = response['result']['parameters']['items_offline']
    else:
        return None
    return resp_data

def parse_result(response, cart_intent):
    
    if response['result']['action'] == 'cart_online':
        print "buy_online\n"
        return parse_cart_items_buy(response, cart_intent)
    elif response['result']['action'] == 'cart_offline':
        print "buy_offline\n"
        return parse_cart_items_buy(response, cart_intent)
    else:
        print "Not yet defined"
        return None
    
