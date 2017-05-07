import os
import sys
import lxml
import pprint
from amazonproduct.contrib import cart
from amazonproduct.api import API

#### REMEMBER TO COPY amazon_cred to ~/.amazon-product-api

NUM_ENTRIES = 10


def search_item_and_price(amazon, search_str, category='All'):

    #Returns resuilt of product search with search string.
    #Searches string under the 'All' category. Only Amazon Product categories are allowed
    results = amazon.item_search(category, Keywords=search_str)

    tmp_asins = list()          #Amazon product id (I think?)
    tmp_titles = list()         #Human-readable title for product

    count = 0
    for search_item in results:
        if count == NUM_ENTRIES:
            break
        tmp_asins.append(search_item.ASIN.text)
        tmp_titles.append(search_item.ItemAttributes.Title.text)
        count += 1

    #Get information on the offers of each search result
    offers = amazon.item_lookup(*tmp_asins, ResponseGroup='Offers')

    aws_id = list()             #Product id
    #names = list()              #Names of product
    #prices = list()             #Price per unit
    #offer_listing_ids = list()  #Product Listing ID

    item_idx = 0
    for offer in offers.Items.Item:
        cur_stock = offer.Offers.getchildren()[0]   # Number of Offers for Product Listing
        if cur_stock > 0:
            aws_id.append(tmp_asins[item_idx])
            #names.append(tmp_titles[item_idx])
            #prices.append(offer.OfferSummary.LowestNewPrice.FormattedPrice.text)
            #offer_listing_ids.append(offer.Offers.Offer.OfferListing.OfferListingId.text)
        item_idx += 1

    """
    for i in range(len(aws_id)):
        print aws_id[i]
        print names[i]
        print prices[i]
        print offer_listing_ids[i]
        print
    """

    #Creating 
    if aws_id:
        item_dict = dict()
        item_dict['aws_id'] = aws_id[0]
        #item_dict['name'] = names[0]
        #item_dict['price'] = prices[0]
        #item_dict['listing_id'] = offer_listing_ids[0]

        return item_dict

    else:
        return None


def buy_items(item_list, quantity_list=None, category_list=None):

    #Instantiate Amazon API object
    amazon = API(locale='us')

    #Default buy 1 of an item, search in 'All' general category
    if quantity_list == None:
        quantity_list = [1 for item in item_list]
    if category_list == None:
        category_list = ['All' for item in item_list]

    item_and_quantity = dict()
    item_names = dict()
    item_prices = dict()

    #Search for item in Amazon, get AWS product id
    #Keep track of AWS product id the quantity to buy. Must be formatted as shown below
    for i in range(len(item_list)):
        #print item_list[i]
        result = search_item_and_price(amazon, item_list[i], category_list[i])
        if result != None:
            item_and_quantity[result['aws_id']] = quantity_list[i]
            #print type(quantity_list[i])

    #Create remote cart of items to buy
    cart = amazon.cart_create(item_and_quantity)

    #Get cart information. ID and HMAC is used to track and reference the created
    #cart. Purchase URL is what the user uses to purchase the desired items
    cart_id = cart.Cart.CartId
    cart_hmac = cart.Cart.HMAC
    purchase_url = cart.Cart.PurchaseURL.text
    #print type(purchase_url)

    #Get contents of cart
    cart_get = amazon.cart_get(cart_id, cart_hmac)
    subtotal = cart_get.Cart.SubTotal.getchildren()[2].text
    cart_contents = cart_get.Cart.CartItems.getchildren()[1:]
    #print type(subtotal)
    #pprint.pprint(item_and_quantity)

    #Get the prices and names of items in the cart. Since adding items to the cart
    #does not (seem to) let the programmer decide which offer listing to add, need
    #to check what is in the cart. Need to muck around the Amazon Product Advertising
    #API more, but man the documentation leaves much to be desired

    for cart_item in cart_contents:
        item_info = cart_item.getchildren()
        aws_id = item_info[1].text
        item_prices[aws_id] = item_info[7].getchildren()[-1].text

        if type(item_info[4].text) == unicode:
            item_names[aws_id] = item_info[4].text.encode('ascii', 'ignore')
        else: 
            # Assuming it is a string type
            item_names[aws_id] = item_info[4].text

        #print item_names[aws_id]
        #print type(item_names[aws_id])
        #print type(item_prices[aws_id])

    #pprint.pprint(item_and_quantity)
    #pprint.pprint(item_names)
    #pprint.pprint(item_prices)
    #pprint.pprint(subtotal)
    #print type(purchase_url)

    return item_and_quantity, item_names, item_prices, subtotal, purchase_url



if __name__ == "__main__":

    amazon_url = buy_items(['eggs', 'milk', 'bacon'])
    #amazon_url = buy_items(['black pepper', 'sugar', 'all-purpose flour'])

    """
    if len(sys.argv) == 2:
        amazon = API(locale='us')
        item_buy, item_add = search_item_and_price(amazon, sys.argv[1])
    elif len(sys.argv) == 3:
        item_buy, item_add = search_item_and_price(amazon, sys.argv[1], sys.argv[2])
    else:
        print "Usage: \n"
        print 'python purchase_amazon.py "<search_string>" "<amazon_recognized_category, e.g. Grocery>"'
    #item_addtocart = Item
    #item_add = cart.Item()
    #item_add.item_id = 
    print item_buy
    cart = amazon.cart_create(item_buy) ## REQUIRES A DICTIONARY OF SPECIFIC TYPE
    cart_id = cart.Cart.CartId
    cart_hmac = cart.Cart.HMAC
    cart_purchase_url = cart.Cart.PurchaseURL
    print cart_purchase_url
    #print cart.Cart.CartItems.SubTotal.Amount
    cart_get = amazon.cart_get(cart_id, cart_hmac)
    cart_items = cart_get.Cart.CartItems
    print cart_items.CartItem.Quantity, cart_items.CartItem.Price.Amount
    cart_add = amazon.cart_add(cart_id, cart_hmac, item_add)
    cart_items2 = cart_add.Cart.CartItems
    print cart_items2.CartItem.Quantity, cart_items.CartItem.Price.Amount
    
    from time import sleep
    sleep(15)
    amazon.cart_clear(cart_id, cart_hmac)
    """
