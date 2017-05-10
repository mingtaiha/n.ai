#!/usr/bin/python
import requests, json

BASE_URL = "http://kool.ngrok.io/"
USER_ID = 1 # default user, sakib

# recipe_id: which recipe id is the user looking for ingredients for?
def get_stores_by_recipe(recipe_id):
    r = requests.get(BASE_URL + "getstores/{0}".format(recipe_id))
    return json.loads(r._content)


# recipe_id: which recipe id did the user just choose?
def select_recipe(recipe_id):
    r = requests.get(BASE_URL + "selection/{0}/{1}".format(USER_ID, recipe_id))
    return r._content


# suggestion_num: number of recipes you want back
# protein: chicken, beef, pork, lamb, eggs, vegetarian
# cuisine: french, chinese, indian, italian, american, mediterranean, south_american
def get_recipe_suggestions(suggestion_num=None, protein=None, cuisine=None):
    url = BASE_URL + "suggestions/{0}".format(USER_ID) + "?"
    and_val = False
    if suggestion_num is not None:
        url += "suggestion_num={0}".format(suggestion_num)
        and_val = True
    if protein is not None:
        if and_val: url += "&"
        url += "protein={0}".format(protein)
        and_val = True
    if cuisine is not None:
        if and_val: url += "&"
        url += "cuisine={0}".format(cuisine)
    r = requests.get(url)
    return json.loads(r._content)


#get_stores_by_recipe(13001)
#select_recipe(13001)
#print get_recipe_suggestions()
