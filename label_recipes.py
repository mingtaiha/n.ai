import sys
import json
import random
import math
from pprint import pprint

def list_to_num(input_list):

    num = 0

    for i in range(len(input_list)):
        num += math.pow(2, i) * input_list[i]

    return num


random.seed()

filename = sys.argv[1]
print filename

with open(filename, 'r') as jfile:
    j = json.load(jfile)


for key, value in j.iteritems():
    print key
    ingr_list = j[key]["ingredients"]

    dairy = [0, 0, 0, 0]
    starch = [0, 0, 0, 0]
    veggies = [0, 0, 0, 0]
    protein = [0, 0, 0, 0, 0]
    cuisine = [0, 0, 0, 0, 0, 0, 0]

    recipe_list = [0, 0, 0, 0, 0]

    for ingr in ingr_list:
        ingr_lower = ingr.lower()

        if "milk" in ingr_lower:
            dairy[3] = 1

        if "cheese" in ingr_lower:
            dairy[2] = 1

        if "cream" in ingr_lower:
            dairy[1] = 1

        if "yogurt" in ingr_lower:
            dairy[0] = 1


        if "potato" in ingr_lower:
            starch[3] = 1

        if ("rice" in ingr_lower) or ("oats" in ingr_lower):
            starch[2] = 1

        if ("bread" in ingr_lower) or ("toast" in ingr_lower) or ("taco" in ingr_lower) or ("tortilla" in ingr_lower) or ("flour" in ingr_lower):
            starch[1] = 1

        if ("pasta" in ingr_lower) or ("noodle" in ingr_lower) or ("vermicelli" in ingr_lower) or ("orzo" in ingr_lower):
            starch[0] = 1


        if ("onion" in ingr_lower) or ("carrot" in ingr_lower) or ("turnip" in ingr_lower) or ("parsnip" in ingr_lower) or ("radish" in ingr_lower) or ("celery" in ingr_lower) or ("beet" in ingr_lower):
            veggies[3] = 1

        if ("bean" in ingr_lower) or ("nut" in ingr_lower) or ("pea" in ingr_lower) or ("lentil" in ingr_lower) or ("almond" in ingr_lower) or ("cashew" in ingr_lower):
            veggies[2] = 1

        if ("kale" in ingr_lower) or ("broccoli" in ingr_lower) or ("cabbage" in ingr_lower) or ("lettuce" in ingr_lower) or ("chard" in ingr_lower) or ("tomato" in ingr_lower) or ("okra" in ingr_lower) or ("pepper" in ingr_lower) or ("asparagus" in ingr_lower) or ("spinach" in ingr_lower) or ("greens" in ingr_lower) or ("shallot" in ingr_lower):
            veggies[1] = 1

        if ("apple" in ingr_lower) or ("banana" in ingr_lower) or ("orange" in ingr_lower) or ("berry" in ingr_lower) or ("grape" in ingr_lower) or ("lemon" in ingr_lower) or ("cherry" in ingr_lower) or ("pear" in ingr_lower) or ("mango" in ingr_lower) or ("avocado" in ingr_lower) or ("peach" in ingr_lower) or ("melon" in ingr_lower) or ("apricot" in ingr_lower) or ("plum" in ingr_lower) or ("kiwi" in ingr_lower) or ("nectarine" in ingr_lower) or ("fig" in ingr_lower) or ("pomegranate" in ingr_lower):
            veggies[0] = 1


        if "chicken" in ingr_lower:
            protein[4] = 1

        if "beef" in ingr_lower:
            protein[3] = 1
        
        if "pork" in ingr_lower:
            protein[2] = 1

        if "lamb" in ingr_lower:
            protein[1] = 1

        if "egg" in ingr_lower:
            protein[0] = 1

        
    for i in range(len(cuisine)):
        cuisine[i] = random.randint(0, 1)



    recipe_list[0] = list_to_num(dairy)
    recipe_list[1] = list_to_num(starch)
    recipe_list[2] = list_to_num(veggies)
    recipe_list[3] = list_to_num(protein)
    recipe_list[4] = list_to_num(cuisine)
        
    j[key]["recipe_index"] = recipe_list

with open("recipes_indexed.json", "wb") as j_out:
    json.dump(j, j_out, indent=4)
