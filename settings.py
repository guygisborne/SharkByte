from platform import node 
import os

from settings_shared import *

# Production settings which will be overwritten if 
# the DJANGO_ENV is set to 'development'

LOCAL = False
DEBUG = False
TEMPLATE_DEBUG = DEBUG                               
ADMINS = (('someone', 'someone@something.com'),)
MANAGERS = ADMINS
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = ''
SECRET_KEY = 'k$&(n4)2hrn-4c8%l@qeu*7%@jg@i#ne0w)#*%4gboro2jgr(w'
DEVELOPMENT_HOST = 'Brenard.local'

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

if node() == DEVELOPMENT_HOST:
	from settings_development import *

