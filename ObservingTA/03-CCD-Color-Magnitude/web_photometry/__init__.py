# coding: utf-8

""" Website for third observing lab! """

__author__ = "adrn <adrn@astro.columbia.edu>"

# Standard library
import os, sys
import sqlite3 
from contextlib import closing

# Third-party
from flask import Flask, session, g, render_template

# Define application and configuration script
app = Flask(__name__)
app.config.from_object("wwwconfig")

# Custom 404 page -- should be at: templates/404.html
#@app.errorhandler(404)
#def not_found(error):
#    return render_template('404.html'), 404

from web_photometry.views import general, photometry, measurements, test
app.register_blueprint(general.mod)
app.register_blueprint(photometry.mod)
app.register_blueprint(measurements.mod)
app.register_blueprint(test.mod)

# The code below is for connecting to the database containing measurements from
#   the students.
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('../data/schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()