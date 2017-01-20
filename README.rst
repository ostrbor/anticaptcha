anticaptcha
=========

Simple anticaptcha library for images with text.

>>> pip install anticaptcha

.. code:: python
   from anticaptcha import Anticaptcha
   ac = Anticaptcha('API_TOKEN')
   with open('captcha.png', 'rb') as img:
          response = ac.createTask(img.read())
   task_id = response['taskId']
   result = ac.getTaskResult(task_id)
   solution = result['solution']['text']


Test with: python -m pytest
