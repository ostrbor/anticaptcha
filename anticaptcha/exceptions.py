class APIKeyMissingError(Exception):
    """No api key in settings.py"""
    pass

class TimeoutError(Exception):
    """ timeout of wait for result """
    pass
