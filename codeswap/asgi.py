"""
ASGI config for codeswap project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codeswap.settings')

application = get_asgi_application() 