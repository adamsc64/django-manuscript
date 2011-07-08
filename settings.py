# Django settings for wyclif project.

# I have split django settings into two files.
#  1. [settings.py] This file. Includes settings common to the server and localhost.
#  2. [local_settings.py] Settings local to your system. For example, you can use
#       your own development database, staticfiles directory, DEBUG = value, etc.

ADMINS = (
	('Christopher R. Adams', 'christopher.r.adams@gmail.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


# Make this unique, and don't share it with anybody.
SECRET_KEY = '8w889y24thu23tn23jt32oit32o8ue8dsudsf8u32058905238huwehhfhjdfjsk8dfsudsfiou'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
	'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'wyclif.urls'


#URL to use when referring to static files located in STATIC_ROOT.
#Example: "/site_media/static/" or "http://static.example.com/"
#If not None, this will be used as the base path for media definitions and the staticfiles app.
#It must end in a slash if set to a non-empty value.
STATIC_URL = '/static/'

# The URL prefix for admin media -- CSS, JavaScript and images used by the
# Django administrative interface. Make sure to use a trailing slash, and
# to have this be different from the MEDIA_URL setting (since the same URL
#cannot be mapped onto two different sets of files). For integration with
#staticfiles, this should be the same as STATIC_URL followed by 'admin/'.
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.static',
)


INSTALLED_APPS = (

	#django apps.
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
	#'django.contrib.admindocs',
	'django.contrib.staticfiles',

	#sentry error reporting system.
	'indexer', 'paging', 'sentry', 'sentry.client',
	
	#wyclif apps.
	'wyclif',

	#django-manuscript
	'manuscript',

	#Other apps.
	'tastypie',
	'south',
	
	#debugging
	'debug_toolbar',
)

#AUTH_PROFILE_MODULE = 'wyclif.Profile'

LOGIN_URL = "/accounts/login/"

# These two settings should be left as True in order for sentry to catch as much information as possible.
TEMPLATE_DEBUG = True
SENTRY_TESTING = True

# Import local settings.
from local_settings import *

