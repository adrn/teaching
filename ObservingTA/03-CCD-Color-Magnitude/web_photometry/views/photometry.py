# coding: utf-8

""" Rawtran: http://integral.physics.muni.cz/rawtran/ """

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
import numpy as np
import astropy.io.fits as fits

# Project
from .. import app

mod = Blueprint('photometry', __name__)

@mod.route('/photometry')
def index():

    with open("data/TA-List") as f:
        lab_tas = [line.strip() for line in f]
    
    for ta in lab_tas:
        ta_data_path = os.path.join("data","classes",ta)
        if not os.path.exists(ta_data_path):
            os.mkdir(ta_data_path)
        
    files = sorted([x for x in os.listdir("data/classes") if x != ".DS_Store" ])
    
    return render_template('general/photometry.html', ta_list=files)

@mod.route('/ajax/image_list', methods=['GET', 'POST'])
def image_list():
    if request.method == "POST":
        ta_name = request.form.get('name', '')
    elif request.method == "GET":
        ta_name = request.args.get('name', '')
    
    # Read in list of lab TAs from data file
    with open("data/TA-List") as f:
        lab_tas = [line.strip() for line in f]
    
    if ta_name == '' or ta_name == '--' or ta_name not in lab_tas:
        abort(404)
    
    #os.listdir()
    ims = [os.path.basename(x) for x in 
            glob.glob(os.path.join("data", "classes", ta_name, "*.fits"))]
    return jsonify(dict(image_names=ims))

def linear_scale(data):
    return 255.*(data - data.min()) / (data.max() - data.min())

@mod.route('/_image/<ta>/<image>/<channel>')
def image_serve(ta, image, channel):
    channel_map = dict(r=0, g=1, b=2)
    image_path = os.path.join("data", "classes", ta, image)
    
    hdulist = fits.open(image_path)
    raw_data = hdulist[0].data
    
    if len(raw_data.shape) in [3,4]:        
        if raw_data.shape[0] in [3,4]:
            image_data = raw_data[channel_map[channel]]
        elif raw_data.shape[2] in [3,4]:
            image_data = raw_data[:,:,channel_map[channel]]
        else:
            # TODO should be a better error...
            print raw_data.shape
            abort(404)
    else:
        image_data = raw_data
    
    im = Image.fromarray(linear_scale(image_data).astype(np.uint8))
    output = StringIO.StringIO()
    im.save(output, "png")
    output.seek(0)
    return send_file(output, mimetype='image/png')

@mod.route('/fitsimage/<ta>/<image>')
def image_viewer(ta, image):
    image_url = os.path.join("/_image", ta, image, "g")
    return render_template('general/tool.html', ta=ta, 
                            image_name=image, 
                            image_url=image_url)
    
    