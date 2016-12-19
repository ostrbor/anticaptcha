import requests
from .settings import HEADERS, API_KEY
from .exceptions import APIKeyMissingError

if API_KEY is None:
    raise APIKeyMissingError("Set API_KEY in settings.py")

session = requests.Session()
session.headers.update(HEADERS)

from .anticaptcha import Anticaptcha
