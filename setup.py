#!/usr/bin/env python
from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


def requirements():
    with open('requirements.txt') as req:
        return req.read().splitlines()


setup(
    name='anticaptcha',
    version='0.0.1',
    description='simple anti captcha library',
    long_description=readme(),
    author='Boris Ostretsov',
    license='MIT',
    author_email='ostrbor@gmail.com',
    keywords='anticaptcha anti captcha recognition',
    url='https://github.com/ostrbor/anticaptcha',
    packages=['anticaptcha'],
    install_requires=requirements())
