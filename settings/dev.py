from __future__ import unicode_literals, absolute_import

'''
Production settings and global
'''
from os.path import join, normpath

from .base import *


DEBUG = True

TEMPLATE_DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'guacamole_db',
        'USER': 'guacamole_user',
        'PASSWORD': 'passguacamole',
        'HOST': '10.12.166.191',
        'POST': '3306'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

#INSTALLED_APPS += (
#)


DEBUG_TOOLBAR_PATCH_SETTINGS = False

# http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
INTERNAL_IPS = ('127.0.0.1',)
# END TOOLBAR CONFIGURATION

# TEMPLATE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#template-string-if-invalid
TEMPLATE_STRING_IF_INVALID = 'INVALID VARIABLE: (%s)'

# http://django-crispy-forms.readthedocs.org/en/latest/crispy_tag_forms.html#make-crispy-forms-fail-loud
CRISPY_FAIL_SILENTLY = False
# END TEMPLATE CONFIGURATION

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': join(SITE_ROOT, 'whoosh_index'),
    }
}
