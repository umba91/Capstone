DEBUG = True

INSTALLED_APPS = [
# ...
'django.contrib.staticfiles',
# ...
'debug_toolbar',
]

MIDDLEWARE = [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
]