""" This server is meant to be run within a virtual environment:
        
        % virtualenv venv
        % . venv/bin/activate
        % python serve.py
        
    Packages installed into this virtual environment:
        pip install numpy flask flask-openid pyfits PIL simplejson

"""

import os
from argparse import ArgumentParser
from web_photometry import app, init_db

if __name__ == "__main__":
    parser = ArgumentParser("Control the server!")
    parser.add_argument("-d", "--debug", dest="debug", action="store_true", 
                        default=False, help="Be chatty!")
    parser.add_argument("-p", "--port", dest="port", default=5000,
                        help="The port to run on.", type=int)
    parser.add_argument("--init-db", dest="init_db", default=False,
                        action="store_true", help="Initialize the database")
       
    args = parser.parse_args()
    
    if args.init_db:
        init_db()
    
    app.run(debug=args.debug, port=args.port) #, host="0.0.0.0")