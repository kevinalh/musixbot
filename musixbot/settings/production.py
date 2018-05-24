import dj_database_url

from .base import *

DEBUG = False

ALLOWED_HOSTS = ["musixbot.herokuapp.com"]

PAGE_TOKEN = os.environ['FACEBOOK_PAGE_ACCESS_TOKEN']

FACEBOOK_GRAPH = 'https://graph.facebook.com/v2.6/'

MESSAGES_ENTRY = FACEBOOK_GRAPH + 'me/messages'

# Database
# https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
