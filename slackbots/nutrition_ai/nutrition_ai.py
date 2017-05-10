import os
import time
import pprint
import random
from slackclient import SlackClient
import api_ai
import client

#from environ variable
BOT_ID = os.environ.get("NUTRITION_AI_ID")
BOT_MANAGER_CHANNEL = os.environ.get("BOT_MANAGER_CHANNEL")

#constants
AT_BOT = "<@" + BOT_ID + ">"
BOT_SESSION_ID = "nutrition_ai_bot"

#instantiate Slack client
slack_client = SlackClient(os.environ.get('NUTRITION_AI_TOKEN'))

#First offering to RNGesus
random.seed()
NUM_RECIPES_RETURNED = 3

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    response = "I'm not sure what you mean. Can you please repeat that?\n"

    apiai_query = command
    print command
    apiai_resp = api_ai.query_apiai(apiai_query, BOT_SESSION_ID)
    pprint.pprint(apiai_resp)

    response = unicode(apiai_resp['result']['fulfillment']['speech'])
    slack_client.api_call("chat.postMessage", channel=channel,
                            text=response, as_user=True)

    if apiai_resp['result']['action'] == 'get_recipe':
        if apiai_resp['result']['actionIncomplete'] == False:
            recipe_filters = api_ai.parse_result(apiai_resp)
            pprint.pprint(recipe_filters)
            protein = recipe_filters['protein']
            if 'cuisine' in recipe_filters:
                cuisine = recipe_filters['cuisine']
            else:
                cuisine = None
            recipe_suggestions = client.get_recipe_suggestions(protein=protein, cuisine=cuisine)

            pprint.pprint(recipe_suggestions)
           
            slack_client.api_call("chat.postMessage", channel=channel,
                                    text="Here's a recipe you'd like", as_user=True)

            selection = random.randint(0, NUM_RECIPES_RETURNED - 1)   # Hard Con
            
            recipe_id = recipe_suggestions['recipes'][selection]['id']
            recipe_name = recipe_suggestions['recipes'][selection]['name']

            slack_client.api_call("chat.postMessage", channel=channel,
                                    text=recipe_name, as_user=True)

            recipe_ingr = recipe_suggestions['recipes'][selection]['ingredients']
            recipe_ingr_user = "Here are the ingredients: \n"
            for ingr in recipe_ingr:
                if ingr:
                    recipe_ingr_user = recipe_ingr_user + "\t" + ingr + "\n"

            slack_client.api_call("chat.postMessage", channel=channel,
                                    text=recipe_ingr_user, as_user=True)

            recipe_instr = recipe_suggestions['recipes'][selection]['instructions']
            recipe_instr_user = "Here are the instructions: \n"
            for instr in recipe_instr:
                if instr:
                    recipe_instr_user = recipe_instr_user + "\t" + instr + "\n"

            slack_client.api_call("chat.postMessage", channel=channel,
                                    text=recipe_instr_user, as_user=True)

            #pprint.pprint(client.select_recipe(recipe_id))
            #pprint.pprint(client.get_stores_by_recipe(recipe_id))

            client.select_recipe(recipe_id)
            food_stores = client.get_stores_by_recipe(recipe_id)
            food_place_city = dict()

            for store in food_stores['stores']:
                if store['id'] != -1:
                    place = store['name']
                    print store['address'].split(',')
                    addr = store['address'].split(',')
                    city = addr[-2].strip()
                    print city
                    print addr[-1].split()
                    state = addr[-1].split()[0]
                    place_and_city = place + ' in ' + city + ', ' + state

                    food_place_city[store['food']['name']] = place_and_city

            return food_place_city

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
        print "nutrition_ai bot connected and running!\n"
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if (command and channel) and (channel != BOT_MANAGER_CHANNEL):
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
            print None
    else:
        print "Connection failed. Invalid Slack token or Bot ID?\n"
