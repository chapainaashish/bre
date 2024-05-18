import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listygo.settings")

application = get_wsgi_application()

# wrapping up existing wsgi application
application = WhiteNoise(application, root="static")
