#!venv/bin/python
from flask import redirect, url_for, render_template, flash, request, send_from_directory, Response, get_flashed_messages
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Message
from nai import app, lm, db, mail
from werkzeug import secure_filename
from models import *
from collections import defaultdict
import os, smtplib, json, datetime, requests, pprint
from datetime import timedelta

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
        fats = request.form.get("fats")
        carbs = request.form.get("carbs")
        proteins = request.form.get("proteins")
        gram_unit_ratio = request.form.get("gram_unit_ratio")
        #validate input
        f_fats = float(fats)
        f_carbs = float(carbs)
        f_proteins = float(proteins)
        f_g_u_ratio = float(gram_unit_ratio)
        if name == "" or f_fats <= 0 or f_carbs <= 0 or f_proteins <= 0 or f_g_u_ratio <= 0:
            flash("yo fuck u")
            return redirect(url_for('food'))

        total_grams = f_fats + f_carbs + f_proteins
        fats_ratio = f_fats / total_grams
        carbs_ratio = f_carbs / total_grams
        proteins_ratio = f_proteins / total_grams

        food = Food(name=name, fats=fats_ratio, carbs=carbs_ratio,
                proteins=proteins_ratio, gram_unit_ratio=f_g_u_ratio)
        db.session.add(food)
        db.session.commit()
        return redirect(url_for('food'))


@app.route('/gay', methods=['GET'])
def memes():
    return "hi"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(Exception)
def unhandled_exception(e):
    return render_template('500.html'), 500
