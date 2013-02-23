# coding: utf-8

"""  """

from __future__ import division

__author__ = "adrn <adrn@astro.columbia.edu>"

# Standard library
import os, sys
import glob
import cStringIO as StringIO

# Third-party
import Image
from flask import Blueprint, render_template, jsonify, request, abort, \
                  flash, send_file

mod = Blueprint('measurements', __name__)

@mod.route('/measurements')
def index():
    return render_template('general/measurements.html')
    