import yaml
import logging.config
import requests
from .settings import HEADERS, API_KEY, LOG_CONFIG
from .exceptions import APIKeyMissingError

if API_KEY is None:
    raise APIKeyMissingError("Set API_KEY in settings.py")

session = requests.Session()
session.headers.update(HEADERS)

with open(LOG_CONFIG) as config_file:
    config = yaml.safe_load(config_file.read())
    logging.config.dictConfig(config)

from .anticaptcha import Anticaptcha
