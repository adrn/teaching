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
    
    if ta_name not in lab_tas:
        abort(404)
    
    ims = [os.path.splitext(os.path.basename(x))[0] for x in 
            glob.glob(os.path.join("data", "classes", ta_name, "*.CR2"))]
    return jsonify(dict(image_names=ims))

@mod.route('/fitsimage/<ta>/<image_name>')
def image_viewer(ta, image_name):
    return render_template('general/tool.html', 
                            ta=ta, 
                            image_name=image_name)

@mod.route('/wcs/<ta>/<image_name>')
def wcs(ta, image_name):
    
    url = "http://deimos.astro.columbia.edu/photometry/images/png/"
    print os.path.join(url, ta, image_name)
    return
    
    client = AstrometryClient("ebupzewhusazsmqe")
    
    wcs_url = "http://nova.astrometry.net/wcs_file/"
    #response = client.url_upload(url)
    image_id = client.submission_images(32430)[0]
    wcs = os.path.join(wcs_url, image_id)
    
    return 
    
# ----------------------------------------------------------------------------
#   Image utilities
# 
def resample(array, factor):
    """ Downsample an image by some factor """
    
    nx, ny = np.shape(array)

    nx_new = int(nx / factor)
    ny_new = int(ny / factor)

    array2 = np.zeros((nx_new, ny))
    for i in range(nx_new):
        array2[i, :] = np.mean(array[i * factor:(i + 1) * factor, :], axis=0)

    array3 = np.zeros((nx_new, ny_new))
    for j in range(ny_new):
        array3[:, j] = np.mean(array2[:, j * factor:(j + 1) * factor], axis=1)

    return array3

def linear_scale(data):
    return (data - data.min()) / (data.max() - data.min())

def arcsinh_scale(data, midpoint=None):
    if midpoint is None:
        # Use a default value -- stolen from APLPy
        midpoint = -1/30.
    return np.arcsinh(data / midpoint) / np.arcsinh(1. / midpoint)

@mod.route('/images/png/<ta>/<image_name>', methods=['GET'])
def image_serve(ta, image_name):
    """ Return a PNG of the given FITS image with a specified scale.
        
        Parameters
        ----------
        filter : str
            The filter
        scale_function : str, [linear, arcsinh, log, sqrt]
        min : numeric
            minimum pixel value
        max : numeric
            maximum pixel value
        midpoint : numeric
        clip : bool
            clip the normalized image data to the range 0-1
        downsample : numeric
            the factor to downsample the image
    """
    
    filter = request.args.get("filter", "Ri")
    scale_function = request.args.get("scale_function", "linear")
    midpoint = request.args.get("midpoint", 1./30)
    clip = request.args.get("clip", 0)
    downsample = request.args.get("downsample", None)
    
    image_base = image_name
    ext = ".fits"
    
    full_image_name = "{0}_{1}{2}".format(image_base, filter, ext)
    fits_image_path = os.path.join("data", "classes", ta, full_image_name)
    hdulist = fits.open(fits_image_path)
    raw_image_data = hdulist[0].data.astype(float)
    
    min = float(request.args.get("min", raw_image_data.min()))
    max = float(request.args.get("max", raw_image_data.max()))
    
    if downsample is not None:
        raw_image_data = resample(raw_image_data, float(downsample))
    
    if int(clip):
        image_data = np.clip(raw_image_data, min, max)
    else:
        image_data = raw_image_data.copy()
    
    image_data = (image_data - min) / (max - min)
    
    if scale_function == "linear":
        pass
    elif scale_function == "arcsinh":
        image_data = arcsinh_scale(image_data, midpoint=float(midpoint))
    else:
        flash("BROKEN")
        return None
    
    im = Image.fromarray((255*image_data).astype(np.uint8))
    output = StringIO.StringIO()
    im.save(output, "png")
    output.seek(0)
    return send_file(output, mimetype='image/png')

@mod.route('/images/raw/<ta>/<image_name>')
def raw_image_data(ta, image_name):
    """ Return a JSON object with the raw data from a FITS image. 
        
        Parameters
        ----------
        downsample : numeric
            the factor to downsample the image
    """
    downsample = request.args.get("downsample", None)
    filter = request.args.get("filter", "Ri")
    image_base = image_name
    ext = ".fits"
    full_image_name = "{0}_{1}{2}".format(image_base, filter, ext)
    
    fits_image_path = os.path.join("data", "classes", ta, full_image_name)
    hdulist = fits.open(fits_image_path)
    raw_image_data = hdulist[0].data
    
    if downsample is not None:
        raw_image_data = resample(raw_image_data, float(downsample))
        
    return jsonify(dict(image_data=raw_image_data.tolist()))

