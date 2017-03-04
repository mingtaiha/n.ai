#!venv/bin/python
from flask import redirect, url_for, render_template, flash, request, send_from_directory, Response
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
    # link to registration
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(Exception)
def unhandled_exception(e):
    return render_template('500.html'), 500
