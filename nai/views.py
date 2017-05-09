#!venv/bin/python
from flask import redirect, url_for, render_template, request, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Message
from nai import app, lm, db, mail
from werkzeug import secure_filename
from models import *
from collections import defaultdict
from datetime import timedelta
import os, smtplib, json, datetime, requests, pprint, csv, random, itertools

from test_get_food import calculate_with_unit

pp = pprint.PrettyPrinter(indent=4)
SUGGESTION_NUM = 3
VARIETY_PERCENT = 1
# require over SUGGESTION_NUM*100/VARIETY_PERCENT recipes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/food', methods=['GET','POST'])
def food():
    if request.method == 'GET':
        foods = Food.query.all()
        return render_template('foods.html', foods=foods)
    if request.method == 'POST':
        #get input
        name = request.form.get("name")
        fats = float(request.form.get("fats"))
        carbs = float(request.form.get("carbs"))
        proteins = float(request.form.get("proteins"))
        calories = float(request.form.get("calories"))

        food = Food(name=name, fats=fats, carbs=carbs,
                proteins=proteins, calories=calories)
        db.session.add(food)
        db.session.commit()
        return redirect(url_for('food'))


def get_delta(time_str):
    """ time_str examples: '15 mins', '4 hours', '1 hour 20 mins' """
    x = time_str.split(" ")
    hours = 0
    mins = 0
    if len(x) == 4:
        hours = int(x[0])
        mins = int(x[2])
    elif len(x) == 2:
        if "hour" in x[1]: hours = int(x[0])
        else: mins = int(x[0])
    return timedelta(hours=hours, minutes=mins)


def condense_str(string):
    x = ""
    for line in string:
        x = x + line + "\n"
    return x


def get_food_from_ingredient_str(foods, ingredient_str):
    """ Return None if food not found in foods list (see Food in models.py) """
    return None, None


def get_grams(ingredient_str):
    amount = 0
    paren_split = ingredient_str.split('(')
    if len(paren_split) > 1:
        paren_str = paren_split[1].split()
        amount = calculate_with_unit(paren_str)
        if amount == 0.0:
            amount = calculate_with_unit(paren_str)
    else:
        single_str = paren_split[0].split(',')[0].split()
        amount = calculate_with_unit(single_str)
        if amount == 0.0:
            amount = 236.5 #cup
    return amount


def get_string_match_score(str1, str2):
    score = 0
    spl1 = str1.split(" ")
    spl2 = str2.split(" ")
    for x in spl1:
        for y in spl2:
            if x.strip().lower() == y.strip().lower():
                score += 1
    return score


def get_best_match_food(food_str, foods, food_names):
    food_match_scores = map(lambda name: get_string_match_score(food_str, name), food_names)
    max_index = food_match_scores.index(max(food_match_scores))
    best_match_name = food_names[max_index]
    #print type(best_match_name), "!!!!", best_match_name
    for food in foods:
        if food.name == best_match_name:
            return food
    #food = Food.query.filter_by(name=best_match_name).first()
    #print "food name is", food.name
    return None


def get_min_length_description(some_list):
    min_len = len(some_list[0].split(" "))
    min_str = some_list[0]
    for i in range(len(some_list)):
        curr_len = len(some_list[i].split(" "))
        if curr_len < min_len:
            min_len = curr_len
            min_str = some_list[i]
    return min_str
"""
i = 1
foods = Food.query.all()
food_names = map(lambda food: food.name, foods)
with open('outfiles/recipes.json', 'r') as recipes_file:
    with open('outfiles/ingredients_extract.json', 'r') as ingredients_file:
        recipes = json.load(recipes_file)
        ingredients = json.load(ingredients_file)

        for key, val in recipes.iteritems():
            # build and add recipe
            recipe = Recipe(name=key, instructions=condense_str(val["instructions"]),
                    cook_time=get_delta(val["cook_time"]), prep_time=get_delta(val["prep_time"]),
                    dairy=int(val["recipe_index"][0]), starch=int(val["recipe_index"][1]),
                    veggies=int(val["recipe_index"][2]), protein=int(val["recipe_index"][3]),
                    cuisine=int(val["recipe_index"][4]), ingredients=condense_str(val["ingredients"]))
            db.session.add(recipe)
            db.session.commit()

            # parse and add all recipe-food ingredient relationships
            #if not hasattr(ingredients, key):
            #    continue
            ingr_dict = ingredients[key]
            counter = 0
            for ingredient_str in val["ingredients"]:
                grams = get_grams(ingredient_str)
                if type(grams) is tuple:
                    #print "========================================="
                    #print "this is a tuple"
                    #print "========================================="
                    grams = grams[0]
                real_ingredient_lists = ingr_dict[ingredient_str]["ingrd_real"]
                real_ingredients = list(itertools.chain.from_iterable(real_ingredient_lists))
                min_str = get_min_length_description(real_ingredients)
                food = get_best_match_food(min_str, foods, food_names)
                #if food is None: continue
                mapping = FoodRecipeMap(grams=grams, food_id=food.id, recipe_id=recipe.id)
                db.session.add(mapping)
                #counter += 1
                #if counter % 50 == 0:
                #    db.session.commit()
            db.session.commit()
            print "added recipe", i, "and its ingredients :)"
            i += 1
"""

@app.route('/genrecipes', methods=['GET'])
def genrecipes():
    i = 1
    foods = Food.query.all()
    food_names = map(lambda food: food.name, foods)
    with open('outfiles/recipes.json', 'r') as recipes_file:
        with open('outfiles/ingredients_extract.json', 'r') as ingredients_file:
            recipes = json.load(recipes_file)
            ingredients = json.load(ingredients_file)

            for key, val in recipes.iteritems():
                # build and add recipe
                recipe = Recipe(name=key, instructions=condense_str(val["instructions"]),
                        cook_time=get_delta(val["cook_time"]), prep_time=get_delta(val["prep_time"]),
                        dairy=int(val["recipe_index"][0]), starch=int(val["recipe_index"][1]),
                        veggies=int(val["recipe_index"][2]), protein=int(val["recipe_index"][3]),
                        cuisine=int(val["recipe_index"][4]), ingredients=condense_str(val["ingredients"]))
                db.session.add(recipe)
                db.session.commit()
                # parse and add all recipe-food ingredient relationships
                #if not hasattr(ingredients, key): continue
                ingr_dict = ingredients[key]
                counter = 0
                for ingredient_str in val["ingredients"]:
                    grams = get_grams(ingredient_str)
                    if type(grams) is tuple:
                        grams = grams[0]
                    real_ingredient_lists = ingr_dict[ingredient_str]["ingrd_real"]
                    real_ingredients = list(itertools.chain.from_iterable(real_ingredient_lists))
                    min_str = get_min_length_description(real_ingredients)
                    food = get_best_match_food(min_str, foods, food_names)
                    #if food is None: continue
                    mapping = FoodRecipeMap(grams=grams, food_id=food.id, recipe_id=recipe.id)
                    db.session.add(mapping)
                db.session.commit()
                print "added recipe", i, "and its ingredients :)"
                i += 1
    return "recipes generated"

# Uncomment this to generate recipes/ingredient mappings. 1025 of them
# genrecipes()

def get_store_json(store):
    if store is None:
        return {'id': -1,
                'name': "n/a",
                'address': "n/a" }
    else:
        return {'id': store.id,
                'name': store.name,
                'address': store.address }


def get_food_json(food):
    return {'id': food.id,
            'name': food.name }
            #'calories': food.calories,
            #'fats': food.fats,
            #'carbs': food.carbs,
            #'proteins': food.proteins }


@app.route('/getstores/<recipe_id>', methods=['GET'])
def getstores(recipe_id):
    foods = []
    stores = []
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    mappings = FoodRecipeMap.query.filter_by(recipe_id=recipe_id).all()
    for mapping in mappings:
        foods.append(Food.query.filter_by(id=mapping.food_id).first())
    for i in range(len(foods)):
        food = foods[i]
        mapping = mappings[i]
        store_map = None
        store_food_maps = list(
                filter(
                    lambda item: item.quantity > int(mapping.grams/100.0),
                    StoreFoodMap.query.filter_by(food_id=food.id).all()
                ))
        store_ids = map(lambda store: store.id, [x for x in stores if x is not None])
        pref_store_food_maps = list(
                filter(
                    lambda store_food_mapping: store_food_mapping.store_id in store_ids,
                    store_food_maps
                ))
        if not store_food_maps:
            store_map = None
        elif not pref_store_food_maps: # empty
            store_map = store_food_maps[0] # greedy
        else:
            store_map = pref_store_food_maps[0]

        if store_map is not None:
            stores.append(Store.query.filter_by(id=store_map.store_id).first())
        else:
            stores.append(None)

    stores_json = []
    for i in range(len(stores)):
        store_json = get_store_json(stores[i])
        store_json["grams"] = mappings[i].grams
        store_json["food"] = get_food_json(foods[i])
        stores_json.append(store_json)

    print "recipe for", recipe.name, ":"
    for i in range(len(stores)):
        if stores[i] is not None:
            print "go to", stores[i].name, "for", mappings[i].grams, "grams of", foods[i].name
        else:
            print "no store found that has", mappings[i].grams, "grams of", foods[i].name

    #return "success! check server output"
    return jsonify(stores=stores_json)


@app.route('/genfoods', methods=['GET'])
def genfoods():
    with open('ingredients.csv', 'rb') as ingredients_file:
        ingredients = csv.DictReader(ingredients_file)
        for row in ingredients:
            food = Food(name=row['name'], proteins=row['protein'],
                fats=row['fat'], carbs=row['carb'], calories=row['cal'])
            db.session.add(food)
        db.session.commit()
    return "foods generated"


@app.route('/genstores', methods=['GET'])
def genstores():

    foods = Food.query.all()
    all_stores = []
    all_foods = []

    target = Store(name="Target", address="5000 Hadley Center Drive, South Plainfield, NJ 07080")   #4
    quickchek = Store(name="QuickChek", address="130 Woodbridge Avenue, Highland Park, NJ 08904")   #6
    stopnshop = Store(name="Stop & Shop", address="424 Raritan Avenue, Highland Park, NJ 08904")    #1
    hmart = Store(name="H-Mart", address="Festival Plaza, 1761 NJ-27, Edison, NJ 08817")            #2
    shoprite = Store(name="ShopRite", address="Rt 1 & Old Post Road, Edison, NJ 08817")             #5
    walmart = Store(name="Walmart", address="2220 NJ-27, Edison, NJ 08817")                         #3

    all_stores.append(target)
    all_stores.append(quickchek)
    all_stores.append(stopnshop)
    all_stores.append(hmart)
    all_stores.append(shoprite)
    all_stores.append(walmart)

    for store in all_stores:
        db.session.add(store)

    db.session.commit()

    target_foods = set([random.choice(foods) for x in range(1, 100)])
    quickchek_foods = set([random.choice(foods) for x in range(1, 100)])
    stopnshop_foods = set([random.choice(foods) for x in range(1, 100)])
    hmart_foods = set([random.choice(foods) for x in range(1, 100)])
    shoprite_foods = set([random.choice(foods) for x in range(1, 100)])
    walmart_foods = set([random.choice(foods) for x in range(1, 100)])

    all_foods.append(target_foods)
    all_foods.append(quickchek_foods)
    all_foods.append(stopnshop_foods)
    all_foods.append(hmart_foods)
    all_foods.append(shoprite_foods)
    all_foods.append(walmart_foods)

    for inventory in all_foods:
        for food in inventory:
            store_name = all_stores[all_foods.index(inventory)].name
            mapping = StoreFoodMap(
                    price = float(random.randint(100,1000))/100,
                    quantity = random.randint(1, 100),
                    food_id = food.id,
                    store_id = Store.query.filter_by(name=store_name).first().id)
            db.session.add(mapping)
    db.session.commit()

    return "stores generated"

#todo: insert into personfoodmap. also, personrecipemap will be history. enable 'choosing'
#basically, build algorithm

@app.route('/genperson', methods=['GET'])
def genperson():
    person = Person(name="Sakib", email="sakib.jalal@gmail.com",
                    address="3 Pace Drive, Edison, NJ 08820",
                    weight_curr=180, weight_goal=200, activity=1.4, height=68)
    db.session.add(person)
    db.session.commit()
    foods = Food.query.all()

    person_food_mappings = \
        map(lambda food: PersonFoodMap(person_id=person.id, food_id=food.id, pref_score=0), foods)

    for x in person_food_mappings:
        db.session.add(x)
        db.session.commit()

    return "person generated"


def get_foods_in_recipe(recipe, foods_dict):
    food_recipe_maps = set(FoodRecipeMap.query.filter_by(recipe_id=recipe.id).all())
    component_foods = map(lambda mapping: foods_dict[mapping.food_id], food_recipe_maps)
    return set(component_foods)


def sum_food_scores(food_list, personal_foods_maps):
    recipe_score = 0
    food_list_ids = map(lambda food: food.id, food_list)
    relevant_foods_maps = filter(lambda food_map: food_map.food_id in food_list_ids, personal_foods_maps)
    for food_map in relevant_foods_maps:
        recipe_score += food_map.pref_score
    return recipe_score


def get_recipe_json(recipe, foods_dict):
    instructions = recipe.instructions.split("\n")
    ingredients = recipe.ingredients.split("\n")
    foods_json = map(get_food_json, get_foods_in_recipe(recipe, foods_dict))

    return {'id': recipe.id,
            'name': recipe.name,
            'cook_time': str(recipe.cook_time),
            'prep_time': str(recipe.prep_time),
            'dairy': recipe.dairy,
            'starch': recipe.starch,
            'veggies': recipe.veggies,
            'protein': recipe.protein,
            'cuisine': recipe.cuisine,
            'ingredients': ingredients,
            'instructions': instructions,
            'food_list': foods_json }


# Generate top suggestion_num recipes for a particular person
@app.route('/suggestions/<person_id>', methods=['GET'])
def suggestions(person_id):
    # take proteins, cuisines, number of suggestions from args
    protein = request.args.get("protein")
    cuisine = request.args.get("cuisine")
    suggestion_num = request.args.get("suggestion_num")
    if not suggestion_num: suggestion_num = SUGGESTION_NUM
    master_list = []
    person = Person.query.filter_by(id=person_id).first()
    if not person: return "bad person, fool"
    foods_dict = dict((food.id, food) for food in Food.query.all())
    recipes = Recipe.query.all()
    print "pre filter", len(recipes)
    if protein == "chicken": recipes = filter(lambda r: (r.protein-2**4)>=0 and (r.protein-2**4)%2==0, recipes)
    if protein == "beef": recipes = filter(lambda r: (r.protein-2**3)>=0 and (r.protein-2**3)%2==0, recipes)
    if protein == "pork": recipes = filter(lambda r: (r.protein-2**2)>=0 and (r.protein-2**2)%2==0, recipes)
    if protein == "lamb": recipes = filter(lambda r: (r.protein-2**1)>=0 and (r.protein-2**1)%2==0, recipes)
    if protein == "eggs": recipes = filter(lambda r: (r.protein-2**0)>=0 and (r.protein-2**0)%2==0, recipes)
    if protein == "vegetarian": recipes = filter(lambda r: (r.protein)==0, recipes)
    if cuisine == "french": recipes = filter(lambda r: (r.cuisine-2**5)>=0 and (r.cuisine-2**5)%2==0, recipes)
    if cuisine == "chinese": recipes = filter(lambda r: (r.cuisine-2**4)>=0 and (r.cuisine-2**4)%2==0, recipes)
    if cuisine == "indian": recipes = filter(lambda r: (r.cuisine-2**3)>=0 and (r.cuisine-2**3)%2==0, recipes)
    if cuisine == "italian": recipes = filter(lambda r: (r.cuisine-2**2)>=0 and (r.cuisine-2**2)%2==0, recipes)
    if cuisine == "american": recipes = filter(lambda r: (r.cuisine-2**1)>=0 and (r.cuisine-2**1)%2==0, recipes)
    if cuisine == "mediterranean": recipes = filter(lambda r: (r.cuisine-2**0)>=0 and (r.cuisine-2**0)%2==0, recipes)
    if cuisine == "south_american": recipes = filter(lambda r: (r.cuisine)==0, recipes)
    print "post filter", len(recipes)
    personal_foods_maps = PersonFoodMap.query.filter_by(person_id=person.id).all()
    # for variety, pick random subset from top 5% of recipe_score range
    for recipe in recipes:
        ingredients = get_foods_in_recipe(recipe, foods_dict)
        recipe_score = sum_food_scores(ingredients, personal_foods_maps)
        master_list.append([recipe_score, recipe])

    limit = len(recipes)/(100/VARIETY_PERCENT)
    if limit < suggestion_num: limit = suggestion_num
    top = sorted(master_list, reverse=True)[:limit] # top 1% if VP=1
    random.shuffle(top)
    suggestions = [x for x in top[:suggestion_num]]
    recipes_json = []
    for score, recipe in suggestions:
        print score, recipe.id, recipe.name
        recipe_json = get_recipe_json(recipe, foods_dict)
        recipe_json["score"] = score
        recipes_json.append(recipe_json)

    return jsonify(recipes=recipes_json)


# Based on selection of recipe, modify food.pref_scores for person
@app.route('/selection/<person_id>/<recipe_id>', methods=['GET'])
def selection(person_id, recipe_id):
    person = Person.query.filter_by(id=person_id).first()
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if not person or not recipe: return "bad args, fool"
    foods_dict = dict((food.id, food) for food in Food.query.all())
    # mod all pref scores accordingly, +1 but cap at 10, upon 10 renormalize
    relevant_foods = get_foods_in_recipe(recipe, foods_dict)
    person_food_maps = map(lambda food: \
        PersonFoodMap.query.filter_by(person_id=person.id, food_id=food.id).first(), relevant_foods)
    for mapping in person_food_maps:
        mapping.pref_score += 1
        if mapping.pref_score > 10:
            normalize(person_id)
    meal_record = PersonRecipeMap(recipe_id=recipe_id,
            person_id=person_id, time=datetime.datetime.now())
    db.session.add(meal_record)
    db.session.commit()
    return "preferences modified"


# Normalize food preference scores if they get too large!
@app.route('/normalize/<person_id>', methods=['GET'])
def normalize(person_id):
    foods = Food.query.all()
    sigma = 0.0
    # renormalize to sum all pref_scores to 10
    person_food_maps = PersonFoodMap.query.filter_by(person_id=person_id).all()
    for mapping in person_food_maps: sigma += mapping.pref_score
    print "sigma", sigma
    if sigma != 0:
        for mapping in person_food_maps: mapping.pref_score /= (sigma/2)
    db.session.commit()
    return "normalized"


@app.route('/clearscores/<person_id>', methods=['GET'])
def clearscores(person_id):
    person_food_maps = PersonFoodMap.query.filter_by(person_id=person_id).all()
    for mapping in person_food_maps:
        mapping.pref_score = 0
    db.session.commit()
    return "scores for person cleared"


@app.route('/loadhistoricalprefs/<person_id>', methods=['GET'])
def loadhistoricalprefs(person_id):
    n = request.args.get("n")
    if not n: n = 10
    clearscores(person_id)
    person_recipe_maps = sorted(PersonRecipeMap.query.all(), key=lambda mapping: mapping.time, reverse=True)[:n]
    recipes = map(lambda mapping: Recipe.query.filter_by(id=mapping.recipe_id).first(), person_recipe_maps)
    finale = map(lambda recipe: selection(person_id, recipe.id), recipes)
    return "pref scores reloaded for {0} most recent meals".format(len(recipes))
