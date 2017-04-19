#!venv/bin/python
from flask import redirect, url_for, render_template, flash, request, send_from_directory, Response, get_flashed_messages
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Message
from nai import app, lm, db, mail
from werkzeug import secure_filename
from models import *
from collections import defaultdict
from datetime import timedelta
import os, smtplib, json, datetime, requests, pprint, csv, random

pp = pprint.PrettyPrinter(indent=4)



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


@app.route('/genrecipes', methods=['GET'])
def genrecipes():
    foods = Food.query.all()
    with open('recipes.json', 'r') as recipes_file:
        recipes = json.load(recipes_file)
        for key, val in recipes.iteritems():
            recipe = Recipe(name=key, instructions=condense_str(val["instructions"]),
                        cook_time=get_delta(val["cook_time"]), prep_time=get_delta(val["prep_time"]),
                        dairy=int(val["recipe_index"][0]), starch=int(val["recipe_index"][1]),
                        veggies=int(val["recipe_index"][2]), protein=int(val["recipe_index"][3]),
                        cuisine=int(val["recipe_index"][4], ingredients=condense_str(val["ingredients"])))
            db.session.add(recipe)
            db.session.commit()
            # add foodrecipemappings from val["ingredients"]
            for ingredient_str in val["ingredients"]:
                food, grams = get_food_from_ingredient_str(foods, ingredient_str)
                if food is not None:
                    mapping = FoodRecipeMap(grams=grams, food_id=food.id, recipe_id=recipe.id)
                    db.session.add(mapping)
                    db.session.commit()
    return "recipes generated"


@app.route('/genfoods', methods=['GET'])
def genfoods():
    """with open('ingredients.csv', 'rb') as ingredients_file:
        ingredients = csv.DictReader(ingredients_file)
        for row in ingredients:
            food = Food(name=row['name'], proteins=row['protein'],
                fats=row['fat'], carbs=row['carb'], calories=row['cal'])
            db.session.add(food)
        db.session.commit()
    """
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


@app.route('/delstores', methods=['GET'])
def delstores():
    for mapping in StoreFoodMap.query.all():
        db.session.delete(mapping)
    for store in Store.query.all():
        db.session.delete(store)
    db.session.commit()
    return "stores deleted"


#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404


#@app.errorhandler(Exception)
#def unhandled_exception(e):
#    return render_template('500.html'), 500
