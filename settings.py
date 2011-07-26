import os.path
import socket
import sys

PROJECT_DIR = os.path.dirname(__file__)
PROJECT_NAME = 'SharkByte'
STATIC_DOC_ROOT = os.path.join(PROJECT_DIR, 'static')

DEBUG = True
TEMPLATE_DEBUG = DEBUG                               

if socket.gethostname() != 'web152.webfaction.com':
	LOCAL = True
else:
	LOCAL = False

ADMINS = (
	('Ibrahim Al-Rajhi', 'abrahamalrajhi@gmail.com'),
)

MANAGERS = ADMINS

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

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
if LOCAL:
	MEDIA_ROOT = os.path.join(PROJECT_DIR, 'static')
else:
	MEDIA_ROOT = ""
	
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
if LOCAL:
	MEDIA_URL = 'http://localhost:8000/static/'
else:
	MEDIA_URL = ''
	
# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
if LOCAL:
	ADMIN_MEDIA_PREFIX = '/media/'
else:
	ADMIN_MEDIA_PREFIX = ''
	
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'k$&(n4)2hrn-4c8%l@qeu*7%@jg@i#ne0w)#*%4gboro2jgr(w'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",               
	"django.core.context_processors.request",
	"django.contrib.messages.context_processors.messages",
)

ROOT_URLCONF = PROJECT_NAME + '.urls'

TEMPLATE_DIRS = (
	os.path.join(PROJECT_DIR, 'templates'),
	os.path.join(PROJECT_DIR, 'templates/employee'),
	os.path.join(PROJECT_DIR, 'templates/menu'),
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.admin',
	'django.contrib.admindocs',
	'django.contrib.markup',
	PROJECT_NAME + '.employee',
	PROJECT_NAME + '.menu',
)
