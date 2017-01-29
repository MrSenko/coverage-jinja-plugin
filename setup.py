#!/usr/bin/env python

from distutils.core import setup

setup(
    name='jinja_coverage',
    version='0.1',
    description='Jinja2 coverage.py plugin',
    author='Mr. Senko',
    author_email='atodorov@MrSenko.com',
    url='https://github.com/MrSenko/coverage-jinja-plugin',
    packages=['jinja_coverage'],
    install_requires=[
        'Jinja2',
        'coverage >= 4.0a7',
    ],
)
