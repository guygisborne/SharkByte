import os

from settings_shared import *

DEBUG = True
LOCAL = True
TEMPLATE_DEBUG = DEBUG                               
ADMINS = (('someone', 'someone@something.com'),)
MANAGERS = ADMINS
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'static')
MEDIA_URL = 'http://localhost:8000/static/'
ADMIN_MEDIA_PREFIX = '/media/'

DATABASES = {
	'default': {
		'ENGINE': 'sqlite3',             # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': 'database.db',           # Or path to database file if using sqlite3.
		'USER': '',                      # Not used with sqlite3.
		'PASSWORD': '',                  # Not used with sqlite3.
		'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
	}
}

