# anti captcha

Simple anticaptcha library for images with text.
Set API_KEY of anti-captcha.com in settings.py before using.

```python
from anticaptcha import Anticaptcha
ac = Anticaptcha()
with open('captcha.png', 'rb') as img:
  response = ac.createTask(img.read())
task_id = response['taskId']
result = ac.getTaskResult(task_id)
solution = result['solution']['text']
```
Test with: python -m pytest
