#!/usr/bin/env python
from __future__ import unicode_literals, absolute_import
import os
import sys

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(here)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
