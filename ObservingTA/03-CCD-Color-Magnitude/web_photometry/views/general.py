import os

from flask import Blueprint, render_template, jsonify

from .. import app

mod = Blueprint('general', __name__)

@mod.route('/')
def index():
    return render_template('general/index.html')
