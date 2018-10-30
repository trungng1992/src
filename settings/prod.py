from __future__ import unicode_literals, absolute_import

"""Production settings and globals."""

import os

from .base import *

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def env(setting, default=None):
    """ Get the environment setting or return exception """
    key = os.environ.get(setting, default)

    if key is None:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

    return key

# HOST CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ["*"]
# END HOST CONFIGURATION

# EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env('EMAIL_HOST', '10.13.92.251')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = env('EMAIL_HOST_USER', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = env('EMAIL_PORT', 25)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER
# END EMAIL CONFIGURATION

# DATABASE CONFIGURATION
# END DATABASE CONFIGURATION


# CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
# END CACHE CONFIGURATION




# STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = join(env('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')
# END STATIC FILE CONFIGURATION


# SECURITY CONFIGURATION
# http://django-secure.readthedocs.org/en/latest/settings.html#secure-ssl-redirect
# MIDDLEWARE_CLASSES += (
#     'djangosecure.middleware.SecurityMiddleware',
# )

SECURE_SSL_REDIRECT = True

# http://django-secure.readthedocs.org/en/latest/settings.html#secure-frame-deny
SECURE_FRAME_DENY = True

# https://docs.djangoproject.com/en/1.6/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True

# http://django-secure.readthedocs.org/en/latest/settings.html#secure-hsts-seconds
SECURE_HSTS_SECONDS = True

# http://django-secure.readthedocs.org/en/latest/settings.html#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAIN = True

# END SECURITY CONFIGURATION