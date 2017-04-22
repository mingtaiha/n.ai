import os
import sys
import lxml
from amazonproduct.api import API

#### REMEMBER TO COPY amazon_cred to ~/.amazon-product-api

NUM_ENTRIES = 10

def search_item_and_price(search_str, category='All'):
    amazon = API(locale='us')

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

    item_idx = 0
    for offer in offers.Items.Item:
        cur_stock = offer.OfferSummary.getchildren()[1]
        #print offer_sum
        #print offer_sum[1]
        if cur_stock > 0:
            aws_id.append(tmp_asins[item_idx])
            names.append(tmp_titles[item_idx])
            prices.append(str(offer.OfferSummary.LowestNewPrice.FormattedPrice))
        #print unicode(price.OfferSummary)
        #print unicode(price.OfferAttributes)
        item_idx += 1

    for i in range(len(aws_id)):
        print aws_id[i]
        print names[i]
        print prices[i]
        print


if __name__ == "__main__":
    if len(sys.argv) == 2:
        search_item_and_price(sys.argv[1])
    elif len(sys.argv) == 3:
        search_item_and_price(sys.argv[1], sys.argv[2])
    else:
        print "Usage: \n"
        print 'python purchase_amazon.py "<search_string>" "<amazon_recognized_category, e.g. Grocery>"'
