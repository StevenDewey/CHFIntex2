"""
WSGI config for test_dmp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
os.environ["DJANGO_SETTINGS_MODULE"] = "test_dmp.settings"
sys.path.append('C:/Apache24/htdocs/CHFIntex2-master')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
