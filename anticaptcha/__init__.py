import logging
import logging.config

import requests
import yaml

HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}

session = requests.Session()
session.headers.update(HEADERS)

try:
    with open('logging.yml') as config_file:
        config = yaml.safe_load(config_file.read())
        logging.config.dictConfig(config)
except FileNotFoundError:
    logging.basicConfig(level=logging.INFO)
    logging.warn(
        "Can't find logging.yml. Try to use basic config for logging.")
