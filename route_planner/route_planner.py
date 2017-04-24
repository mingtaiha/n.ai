import os
import time
import utils
from slackclient import SlackClient
import google_places as gp

#from environ variable
BOT_ID = os.environ.get("ROUTE_PLANNER_ID")

#constants
AT_BOT = "<@" + BOT_ID + ">"

PROXIMITY_CMD_UNIQ = ['nearest', 'closest']
PROXIMITY_CMD = ['nearby', 'close by', 'near me', 'in the area', 'around me']
CLOSEST_ROUTE = "fastpath"

#instantiate Slack client
slack_client = SlackClient(os.environ.get('ROUTE_PLANNER_TOKEN'))

#### Commands which our bot is designed to handle
# What is the closest X nearby
         # From current location, find X with min distance       
# How do I get from X to Y
        # Find X, Find Y, get from X to Y
# Starting from X, I'd like to go to following places: X1, X2, ... , Xk
        # Return or not return to X?
# Starting from X, find me the fastest route to X1, X2, ...
        # Return or not return to X?

def closest_route(command):
    start_loc = ""
    end_loc = ""
    while (start_loc == '') and (end_loc == ''):
        locs = str(command).split('fastpath ')[1].split(',')
        if 'from' == locs[0][:4]:
            start_loc = locs[0][5:]
            if 'to' in locs[1][:2]:
                end_loc = locs[3:]
            else:
                response = "You are missing an ending location\n"
                return response
        elif 'to' in locs[0][:2]:
            end_loc = locs[0][3:]
            if 'from' in loc[1][:4]:
                start_loc = locs[1][5:]
            else:
                response = "You are missing a starting location\n"
                return response
        else:
            response = "try `fastpath from <start> to <end>`" 
            return response
            
    gp.get_gplaces_results(start_loc)
    print
    print
    gp.get_gplaces_results(end_loc)
    response = "correct syntax\n"
    return response



def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "I'm not sure what you mean. Can you please repeat that?\n"
    if command.startswith(CLOSEST_ROUTE):   
        print command
        closest_route(command)

        

    #cmd = utils.strip_punc(str(command))
    #print cmd
    #cmd_list = utils.filter_stopwords(cmd.split())

    

    #if command.startswith(EXAMPLE_COMMAND):
        response = unicode("seems to be working alright\n")
        print len(response)
        slack_client.api_call("chat.postMessage", channel=channel,
							text=response, as_user=True)


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
