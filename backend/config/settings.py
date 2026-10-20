"""
Settings for the Assignment Cost Estimate back end.

This is a calculation-only JSON API: no users, sessions, admin or database
models, so the apps and middleware for those are left out.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Read from the environment in production; the default exists only so the
# local dev server and tests run with zero setup. It is NOT a real secret.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-insecure-key")

# Local development only. Turned off before any real deployment.
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    "estimator.apps.EstimatorConfig",
]

# No sessions, authentication or CSRF-protected forms: this API keeps no
# per-user state, so no middleware is needed.
MIDDLEWARE = []

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

# No models exist, but the test runner still wants a database to create,
# so keep the simplest possible one.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_TZ = True
