"""
WSGI config for codeswap project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codeswap.settings')

application = get_wsgi_application() 