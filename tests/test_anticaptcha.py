from anticaptcha import Anticaptcha
from pytest import fixture
import vcr

ac = Anticaptcha()


@fixture
def balance_keys():
    return ['balance']


@fixture
def task_keys():
    return ['taskId']


@fixture
def task_result_keys():
    return ['status', 'solution']


@vcr.use_cassette(
    'tests/vcr_cassettes/getBalance.yml',
    filter_post_data_parameters=['clientKey'])
def test_getBalance(balance_keys):
    response = ac.getBalance()
    assert isinstance(response, dict)
    assert set(balance_keys).issubset(response.keys())


@vcr.use_cassette(
    'tests/vcr_cassettes/createTask.yml',
    filter_post_data_parameters=['clientKey'])
def test_createTask(task_keys):
    with open('tests/captcha.png', 'rb') as img:
        response = ac.createTask(img.read())
    assert isinstance(response, dict)
    assert set(task_keys).issubset(response.keys())


@vcr.use_cassette(
    'tests/vcr_cassettes/getTaskResult.yml',
    filter_post_data_parameters=['clientKey'])
def test_getTaskResult(task_result_keys):
    with open('tests/captcha.png', 'rb') as img:
        task_id = ac.createTask(img.read())['taskId']
    response = ac.getTaskResult(task_id)
    assert isinstance(response, dict)
    assert set(task_result_keys).issubset(response.keys())
