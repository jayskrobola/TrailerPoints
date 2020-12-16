"""
WSGI config for django_test project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/ubuntu/DjangoCPSC4910/django_test/django_test')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_test.settings")

application = get_wsgi_application()
