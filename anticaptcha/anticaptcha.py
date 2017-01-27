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

    def getBalance(self):
        """sends JSON data in POST request -> dict"""
        url = self.base_url + 'getBalance'
        data = {'clientKey': self.clientKey}
        response = session.post(url, data=json.dumps(data)).json()
        msg = "Sent [Get Balance] to url: %s with clientKey: %s" % (
            url, self.clientKey_short)
        self.logger.info(msg)
        if response.get('errorCode'):
            msg = "Received [Get Balance] error %s: %s" % (
                response['errorCode'], response.get('errorDescription'))
            self.logger.error(msg)
        else:
            msg = "Received [Get Balance] response: balance = %s" % (
                response['balance'])
            self.logger.info(msg)
        return response

    def createTask(self, bin_str):
        """binary content of file -> id of task in dict"""
        self.logger.info('[ANTICAPTCHA] CREATE TASK')
        url = self.base_url + 'createTask'
        img_str = b64encode(bin_str).decode('ascii')
        task = {'type': 'ImageToTextTask', 'body': img_str}
        data = {'clientKey': self.clientKey, 'task': task}
        msg = "Sent [Create Task] to url: %s with clientKey: %s" % (
            url, self.clientKey_short)
        self.logger.info(msg)
        response = session.post(url, data=json.dumps(data)).json()
        if response.get('errorCode'):
            msg = "Received [Create Task] error %s: %s" % (
                response['errorCode'], response.get('errorDescription'))
            self.logger.error(msg)
        else:
            msg = "Received [Create Task] response: taskId = %s" % (
                response['taskId'])
            self.logger.info(msg)
        return response

    def getTaskResult(self, task_id):
        """ -> dict with solution and extra info about task OR None"""
        url = self.base_url + 'getTaskResult'
        time.sleep(WAIT_BEFORE_REQUESTS)
        total_sec = WAIT_BEFORE_REQUESTS
        data = {'clientKey': self.clientKey, 'taskId': task_id}
        while total_sec <= TIMEOUT:
            response = session.post(url, data=json.dumps(data)).json()
            msg = "Sent [Get Task Result] to url: %s with clientKey: %s" % (
                url, self.clientKey_short)
            self.logger.info(msg)
            if response.get('errorCode'):
                msg = "Received [Get Task Result] error %s: %s" % (
                    response['errorCode'], response.get('errorDescription'))
                self.logger.error(msg)
                break
            elif response.get('status') == 'processing':
                time.sleep(WAIT_BETWEEN_REQUESTS)
                total_sec += WAIT_BETWEEN_REQUESTS
                continue
            elif response.get('status') == 'ready':
                msg = "Received [Get Task Result] response: solution %s in %s seconds" % (
                    response['solution']['text'], total_sec)
                self.logger.info(msg)
                return response
        else:
            msg = "Not solved Task (%s) after %s seconds of waiting" % (
                task_id, total_sec)
            self.logger.error(msg)
