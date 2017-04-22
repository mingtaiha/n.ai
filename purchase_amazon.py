import os
import sys
import lxml
from amazonproduct.contrib import cart
from amazonproduct.api import API

#### REMEMBER TO COPY amazon_cred to ~/.amazon-product-api

NUM_ENTRIES = 5


def search_item_and_price(amazon, search_str, category='All'):
    #amazon = API(locale='us')

    results = amazon.item_search(category, Keywords=search_str)
    #print results.items

    tmp_asins = list()
    tmp_titles = list()

    first = 0
    for book in results:
        if first == NUM_ENTRIES:
            break
        #print unicode(book.ItemAttributes.Title)
        #print unicode(book.ASIN)
        tmp_asins.append(str(book.ASIN))
        tmp_titles.append(str(book.ItemAttributes.Title))

        first += 1

    #print asins[0]

    offers = amazon.item_lookup(*tmp_asins, ResponseGroup='Offers')
    #print unicode(prices.Item)

    #print type(prices)
    #print prices.getchildren()
    #children = prices.getchildren()

    aws_id = list()
    names = list()
    prices = list()
    offer_listing_ids = list()

    item_idx = 0
    for offer in offers.Items.Item:
        cur_stock = offer.OfferSummary.getchildren()[1]
        #print offer_sum
        #print offer_sum[1]
        if cur_stock > 0:
            aws_id.append(tmp_asins[item_idx])
            names.append(tmp_titles[item_idx])
            prices.append(str(offer.OfferSummary.LowestNewPrice.FormattedPrice))
            offer_listing_ids.append(str(offer.Offers.Offer.OfferListing.OfferListingId))
        #print unicode(price.OfferSummary)
        #print unicode(price.OfferAttributes)
        item_idx += 1

    for i in range(len(aws_id)):
        print aws_id[i]
        print names[i]
        print prices[i]
        print offer_listing_ids[i]
        print

    item_dict = dict()
    for i in range(len(aws_id) - 1):
        item_dict[aws_id[i]] = i+2

    last_item_dict = {aws_id[-1] : 12}

    return item_dict, last_item_dict

if __name__ == "__main__":
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
    sleep(30)
    amazon.cart_clear(cart_id, cart_hmac)
