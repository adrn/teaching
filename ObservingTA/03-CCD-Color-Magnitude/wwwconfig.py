import os

DEBUG = False
#SERVER_NAME = "deimos.astro.columbia.edu:5000"
SESSION_COOKIE_NAME = "ccd03"

SECRET_KEY = '/3yXR~oo240;)@941../;;'
#DATABASE = "sqlite://" + os.path.join(os.getcwd(), "data", "measurements.db")
DATABASE = os.path.join(os.getcwd(), "data", "measurements.db")
USERNAME = "admin"
PASSWORD = "colAstro13+"

ADMINS = []