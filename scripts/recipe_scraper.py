import urllib2
import csv
import json

from BeautifulSoup import BeautifulSoup


'''
recipe_site = 'http://www.afamilyfeast.com/alphabetical-list/'

req = urllib2.Request(recipe_site, headers={'User-Agent' : 'Magic-Browser'})
con = urllib2.urlopen(req)
html = con.read()
print html
'''

all_recipes = dict()

with open("recipe_list.csv", "rb") as c_recipe:
    c = csv.reader(c_recipe)
    for row in c:
        recipe = dict()

        recipe_name = row[1]
        print recipe_name

        recipe_site = row[0]

        req = urllib2.Request(recipe_site, headers={'User-Agent' : 'Magic-Browser'})

        try:
            con = urllib2.urlopen(req)
            html = BeautifulSoup(con.read())

            ingredients = html.findAll('li', attrs={'class' : 'ingredient', 'itemprop' : 'ingredients'})
            instructions = html.findAll('li', attrs={'class' : 'instruction', 'itemprop' : 'recipeInstructions'})
            servings = html.find('span', attrs={'itemprop' : 'recipeYield'})
            prep_time = html.find('time', attrs={'itemprop' : 'prepTime'})
            cook_time = html.find('time', attrs={'itemprop' : 'cookTime'})
            total_time = html.find('time', attrs={'itemprop' : 'totalTime'})

            try:
                recipe['prep_time'] = prep_time.contents[0]
            except:
                recipe['prep_time'] = ""

            try:
                recipe['cook_time'] = cook_time.contents[0]
            except:
                recipe['cook_time'] = ""

            try:
                recipe['total_time'] = total_time.contents[0]
            except:
                recipe['total_time'] = ""


            ingre_list = list()
            instr_list = list()
        
            for ingre in ingredients:
                ingre_list.append(ingre.contents[0])

            for instr in instructions:
                instr_list.append(instr.contents[0])

            recipe['ingredients'] = ingre_list
            recipe['instructions'] = instr_list

            all_recipes[recipe_name] = recipe

        except:
            print "can't connect"

try:
    with open('recipes.json', 'w') as jfile:
        json.dump(all_recipes, jfile, sort_keys=True, indent=4)
except:
    import pprint
    pprint.pprint(all_recipes)
