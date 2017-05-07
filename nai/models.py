#!venv/bin/python
from nai import db


class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)


class Food(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    calories = db.Column(db.Float, nullable=True)
    """ # grams of _ per 100g of food """
    fats = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    proteins = db.Column(db.Float, nullable=False)


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    weight_curr = db.Column(db.Integer, nullable=True)  #lbs
    weight_goal = db.Column(db.Integer, nullable=True)  #lbs
    activity = db.Column(db.String(64), nullable=True)  #constants
    height = db.Column(db.Integer, nullable=True)       #inches


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    ingredients = db.Column(db.String(16000), nullable=True)
    instructions = db.Column(db.String(16000), nullable=True)
    cook_time = db.Column(db.Interval(), nullable=True)
    prep_time = db.Column(db.Interval(), nullable=True)
    dairy = db.Column(db.Integer, nullable=True)  #dairy
    starch = db.Column(db.Integer, nullable=True)  #starch
    veggies = db.Column(db.Integer, nullable=True)  #veggies
    protein = db.Column(db.Integer, nullable=True)  #proteins
    cuisine = db.Column(db.Integer, nullable=True)  #cuisines


class StoreFoodMap(db.Model):
    __tablename__ = 'store_food'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False) #per 100g unit
    quantity = db.Column(db.Integer, nullable=False) #100g units
    food_id = db.Column(db.Integer, db.ForeignKey("foods.id"), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)


class PersonFoodMap(db.Model):
    __tablename__ = 'person_food'
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey("foods.id"), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"), nullable=False)
    pref_score = db.Column(db.Float, default=0, nullable=False) #allergies, [0, 10]


class PersonRecipeMap(db.Model):
    __tablename__ = 'person_recipe'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"), nullable=False)
    time = db.Column(db.DateTime, nullable=False)


class FoodRecipeMap(db.Model):
    __tablename__ = 'food_recipe'
    id = db.Column(db.Integer, primary_key=True)
    grams = db.Column(db.Integer, nullable=False)   #grams
    food_id = db.Column(db.Integer, db.ForeignKey("foods.id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
