import os

from flask import Blueprint, render_template, jsonify

from .. import app

mod = Blueprint('general', __name__)

@mod.route('/')
def index():
    return render_template('general/index.html')

@mod.route('/test')
def test():
    return render_template('general/test.html')