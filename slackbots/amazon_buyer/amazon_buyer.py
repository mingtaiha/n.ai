import os
import time
import pprint
from slackclient import SlackClient
import api_ai
import purchase_amazon as pa

#from environ variable
BOT_ID = os.environ.get("AMAZON_BUYER_ID")
BOT_MANAGER_CHANNEL = os.environ.get("BOT_MANAGER_CHANNEL")

#constants
AT_BOT = "<@" + BOT_ID + ">"
BOT_SESSION_ID = "amazon_buyer_bot"

#instantiate Slack client
slack_client = SlackClient(os.environ.get('AMAZON_BUYER_TOKEN'))

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

    if apiai_resp['result']['action'] == 'buy_items':
        if apiai_resp['result']['actionIncomplete'] == False:
            items = api_ai.parse_buy_items(apiai_resp)
            item_and_quantity, item_names, item_prices, subtotal, purchase_url = pa.buy_items(items) 
            
            response = ""
            for item_id in item_names.keys():
                response = response + "Buying {0} unit of {1}. Costs {2}\n".format(item_and_quantity[item_id], item_names[item_id], item_prices[item_id])
            response = response + "The total cost comes out to {0}\n".format(subtotal)
            response = response + "Here's the link to checkout: {0}\n".format(purchase_url)


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
        print "amazon_buyer bot connected and running!\n"
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel and (channel != BOT_MANAGER_CHANNEL):
                handle_command(command, channel)
            elif channel and (channel == BOT_MANAGER_CHANNEL):
                print "got a message from the computer_networks channel"
            time.sleep(READ_WEBSOCKET_DELAY)
            print None
    else:
        print "Connection failed. Invalid Slack token or Bot ID?\n"
