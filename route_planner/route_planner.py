import os
import time
import utils
from slackclient import SlackClient
import google_places as gp
import api_ai
import pprint

#from environ variable
BOT_ID = os.environ.get("ROUTE_PLANNER_ID")

#constants
AT_BOT = "<@" + BOT_ID + ">"
BOT_SESSION_ID = "route_planner_bot"


#instantiate Slack client
slack_client = SlackClient(os.environ.get('ROUTE_PLANNER_TOKEN'))

#### Commands which our bot is designed to handle
# What is the closest X nearby
         # From current location, find X with min distance       
# How do I get from X to Y
        # Find X, Find Y, get from X to Y
# Starting from X, find me the fastest route to X1, X2, ...
        # Return or not return to X?


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
    slack_client.api_call("chat.postMessage", channel=channel,
                        text=response, as_user=True)

    print apiai_resp['result']['actionIncomplete'] == "False"
    if apiai_resp['result']['actionIncomplete'] == False:
        print "I get here\n"
        data = api_ai.parse_result(apiai_resp)
        pprint.pprint(data)


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
