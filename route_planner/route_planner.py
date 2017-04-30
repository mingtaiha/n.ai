import os
import time
from slackclient import SlackClient
import google_places as gp
import google_maps as gm
import api_ai
import pprint

#from environ variable
BOT_ID = os.environ.get("ROUTE_PLANNER_ID")

#constants
AT_BOT = "<@" + BOT_ID + ">"
BOT_SESSION_ID = "route_planner_bot"


#instantiate Slack client
slack_client = SlackClient(os.environ.get('ROUTE_PLANNER_TOKEN'))


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "I'm not sure what you mean. Can you please repeat that?\n"
    #if command.startswith(CLOSEST_ROUTE):   
    
    apiai_query = command
    print command
    apiai_resp = api_ai.query_apiai(apiai_query, BOT_SESSION_ID) 
    pprint.pprint(apiai_resp)
    
    response = unicode(apiai_resp['result']['fulfillment']['speech'])

    if apiai_resp['result']['metadata']['intentName'] == 'route_plan':
        if apiai_resp['result']['actionIncomplete'] == False:
            data = api_ai.parse_result(apiai_resp)
            pprint.pprint(data)
            #slack_client.api_call("chat.postMessage", channel=channel, text="activating gmaps", as_user=True)
            print "activating google maps\n"
            #response = "Starting address: {0}\n Ending address: {1}\n".format(data['start_addr'], data['end_addr'])
            start_addr = data['start_addr']
            end_addr = data['end_addr']
            inter_addrs = list()
            if 'inter_places' in data:
                for stop in data['inter_places']:
                    inter_result = gp.get_gplaces_results(stop['place'], stop['city'], stop['state'])
                    if inter_result != None:
                        inter_addrs.append(inter_result['address'])
                        print inter_result['address']
                        inter_response = "The address of {0} in {1}, {2} is {3}\n".format(stop['place'], stop['city'], stop['state'], inter_result['address'])
                        slack_client.api_call("chat.postMessage", channel=channel, text=inter_response, as_user=True)
                    else:
                        print "There is no {0} in {1}, {2}\n".format(stop['place'], stop['city'], stop['state'])
                        
            route, cost = gm.get_path(start_addr, inter_addrs, end_addr)

            addr_path_list = [start_addr]
            addr_path_list.extend(inter_addrs)
            addr_path_list.append(end_addr)

            store_route = list()
            for i in range(len(route)):
                store_route.append(addr_path_list[route[i]])

            response = "Here's a way to get to all places:\n"
            for i in range(len(cost)):
                response = response + "Go from {0} to {1}. Takes about {2} minutes\n".format(store_route[i], store_route[i+1], round(cost[i]))



    elif apiai_resp['result']['metadata']['intentName'] == 'find_place':
        if apiai_resp['result']['actionIncomplete'] == False:
            data = api_ai.parse_result(apiai_resp)
            #pprint.pprint(data)
            gplaces_result = gp.get_gplaces_results(data['place'], data['city'], data['state'])
            if gplaces_result == None:
                response = "There's no {0} in {1},{2}".forma(data['place'], data['city'], data['state'])
            else:
                pprint.pprint(gplaces_result)
                response = "Address: {0}".format(gplaces_result['address'])

    else:
        print "Intent not implemented\n"

    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
				#return text after the @mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                        output['channel']

    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print "test-bot connected and running!\n"
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            print command
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print "Connection failed. Invalid Slack token or Bot ID?\n"
