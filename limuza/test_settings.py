from .settings import *

# Disable WhiteNoise for tests
MIDDLEWARE = [
    middleware for middleware in MIDDLEWARE
    if middleware != 'whitenoise.middleware.WhiteNoiseMiddleware'
]

# Use a simpler static files storage backend for testing

# Ensure the `STORAGES` setting is not conflicting
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Disable debug toolbar for tests to avoid unnecessary middleware
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: False,
}

# Override any other settings for testing if needed
DEBUG = True  # Usually, you'd want DEBUG to be True for testing
