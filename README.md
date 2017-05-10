# Nutritional AI

This is Sakib and Ming's Nutritional AI App that uses Flask/SQLAlchemy. 

Graduate Course Report avaiable for viewing [here](https://goo.gl/K7K3ye).

## Overview

This app incorporates a custom-built machine learning algorithm to suggest what recipes a user should eat. The user may specify the number of suggested recipes, the protein and the specific cuisine. Many scripts (stored in /scripts) were used to scrape food/recipe data from online, clean it in various stages (see /outfiles), and structure it to mold to our database models. Routes were built to expose user services on API endpoints:

* Get suggestions for recipes, based on user history and preferences for foods
* Select a recipe for consumption, which are learned into your preferences
* Get a minimal set of stores to buy the ingredients for a particular recipe from

These services are designed to feed into each other, and are integrated into the Slackbots which communicate with each other to provide a seamless natural language interface for this service flow.

The design of the bots is loosely coupled, so that it is as easy as possible for anyone to add their own bots which do specific tasks and integrate them into the service flow. The goal is for a master bot to enable bot-service discovery for automatic bot-to-bot communication.

## Setup

After going into the directory, these are the steps to get the app up and running locally:

#### Step 1. Create a Virtual Environment and Install Dependencies

Create a new Virtual Environment for the project and source it.  If you don't have Virtual Environment yet, you can find installation [instructions here](https://virtualenv.readthedocs.org/en/latest/).

```
$ virtualenv venv
$ source venv/bin/activate
```

Next we need to install the project dependencies, which are listed in `pip.req`. If you have issues, try install MySQL python dev libs.

```
(venv) $ pip install -r pip.req
```

#### Step 2. Set up the Database

Enter the MySQL shell and create a flask app user and database running locally. If you don't have MySQL yet, you can find installation [instructions here](http://dev.mysql.com/doc/refman/5.7/en/installing.html).

```
mysql> create database nai;
mysql> create user 'nai'@'localhost' identified by 'nai';
mysql> grant all privileges on nai.* to 'nai'@'localhost';
```

Now apply the models defined in the flask app as such:

```
(venv) $ ./migrate.py db init
(venv) $ ./migrate.py db migrate
(venv) $ ./migrate.py db upgrade
```

For most table changes, edit nai/models.py, and run the above migrate and upgrade commands again.

If you happen to change a foreign key, or delete the migrations folder, run the above init, migrate and upgrade commands again.

#### Step 3. Run the Server

Now we're ready to start our server which is as simple as:

```
(venv) $ ./run.py
```

Optional: If we want to expose this to a public facing URL, we can use [ngrok](https://ngrok.com/):

```
(venv) $ ./ngrok http 5000
```

## Credit

Built by Sakib Jalal & Ming Tai Ha at Rutgers University, kept under the MIT License.

ALL STORES SELL ITEMS IN 100g PACKAGES, NO EXCEPTIONS
