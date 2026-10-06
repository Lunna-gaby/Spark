import os

from django.core.wsgi import get_wsgi_application
from workers import wsgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

app = wsgi.entrypoint(application)