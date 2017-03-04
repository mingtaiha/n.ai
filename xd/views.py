#!venv/bin/python
from flask import redirect, url_for, render_template, flash, request, send_from_directory, Response
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Message
from xd import app, lm, db, mail
from werkzeug import secure_filename
from oauth import OAuthSignIn
from models import User
from collections import defaultdict
import os, smtplib, json, datetime, requests, pprint
from datetime import timedelta


pp = pprint.PrettyPrinter(indent=4)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    return render_template('admin.html')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    # link to registration
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'GET':
        return render_template('registration.html')
    if request.method == 'POST':
        # handle user creation and link to dashboard
        # upload file handling: file = request.files['file']
        return render_template('dashboard.html')


@app.route('/dashboard', methods=['GET'])
@login_required
def dash():
    return render_template('dashboard.html', name=current_user.name)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/files/<file>', methods=['GET'])
@login_required
def files(file):
    if file == current_user.file:
        return send_from_directory(app.config["UPLOAD_FOLDER"], file)
    return render_template('404.html')


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    xd_id, name, email = oauth.callback()
    if xd_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(xd_id=xd_id).first()
    if not user: # Create, add and login new user. Redirect to /register
        user = User(xd_id=xd_id, name=name, email=email)
        db.session.add(user)
        db.session.commit()
        login_user(user, True)
        return redirect(url_for('dash')) # previously register
    else: # Login new user. Redirect to /
        login_user(user, True)
        return redirect(url_for('index'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def upload_file_handler(file):
    # Save unique file per user
    filename = str(current_user.id) + "_" + secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    current_user.file = filename
    # Delete old file
    path = os.path.abspath(app.config['UPLOAD_FOLDER'])
    list = os.listdir(path)
    for item in list:
        id = int(item.split('_')[0])
        if id == int(current_user.id) and filename != item:
            os.remove(os.path.join(path, item))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(Exception)
def unhandled_exception(e):
    return render_template('500.html'), 500
