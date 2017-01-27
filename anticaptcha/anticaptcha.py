import json
import logging
import time
from base64 import b64encode

from . import session

TIMEOUT = 60  # max seconds to wait for result
WAIT_BEFORE_REQUESTS = 5  # wait seconds before starting to request for result
WAIT_BETWEEN_REQUESTS = 1


class Anticaptcha:
    def __init__(self, API_KEY):
        self.clientKey = API_KEY
        # for logging to hide full key from saving in log file
        self.clientKey_short = self.clientKey[-8:]
        self.base_url = 'http://api.anti-captcha.com/'
        self.logger = logging.getLogger(__name__)

    def _send_post_request(self, url, data, api_method):
        "Send request and log request"
        response = session.post(url, data=json.dumps(data)).json()
        msg = "Sent [%s] to url: %s with clientKey: %s" % (
            api_method, url, self.clientKey_short)
        self.logger.info(msg)
        return response

    def _log_response(self, response, attr_to_log, api_method):
        if response.get('errorCode'):
            msg = "Received [%s] error %s: %s" % (
                api_method, response['errorCode'],
                response.get('errorDescription'))
            self.logger.error(msg)
        else:
            msg = "Received [%s] response: %s = %s" % (api_method, attr_to_log,
                                                       response[attr_to_log])
            self.logger.info(msg)

    def getBalance(self):
        """sends JSON data in POST request -> dict"""
        api_method = 'getBalance'
        url = self.base_url + api_method
        data = {'clientKey': self.clientKey}
        response = self._send_post_request(url, data, api_method)
        self._log_response(response, 'balance', api_method)

    def createTask(self, bin_str):
        """binary content of file -> id of task in dict"""
        api_method = 'createTask'
        url = self.base_url + api_method
        img_str = b64encode(bin_str).decode('ascii')
        task = {'type': 'ImageToTextTask', 'body': img_str}
        data = {'clientKey': self.clientKey, 'task': task}
        response = self._send_post_request(url, data, api_method)
        self._log_response(response, 'taskId', api_method)

    def getTaskResult(self, task_id):
        """ -> dict with solution and extra info about task OR None"""
        api_method = 'getTaskResult'
        url = self.base_url + api_method
        time.sleep(WAIT_BEFORE_REQUESTS)
        total_sec = WAIT_BEFORE_REQUESTS
        data = {'clientKey': self.clientKey, 'taskId': task_id}
        while total_sec <= TIMEOUT:
            response = self._send_post_request(url, data, api_method)
            if response.get('errorCode'):
                msg = "Received [%s] error %s: %s" % (
                    api_method, response['errorCode'],
                    response.get('errorDescription'))
                self.logger.error(msg)
                return
            elif response.get('status') == 'processing':
                time.sleep(WAIT_BETWEEN_REQUESTS)
                total_sec += WAIT_BETWEEN_REQUESTS
                continue
            elif response.get('status') == 'ready':
                msg = "Received [%s] response: solution %s in %s seconds" % (
                    api_method, response['solution']['text'], total_sec)
                self.logger.info(msg)
                return response
        else:
            msg = "TIMEOUT. Task (%s) was not solved for %s seconds" % (
                task_id, total_sec)
            self.logger.error(msg)
