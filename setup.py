#!/usr/bin/env python

from distutils.core import setup

setup(
    name='mako_coverage',
    version='0.1',
    description='Mako coverage.py plugin',
    author='Ned Batchelder',
    author_email='ned@nedbatchelder.com',
    url='',
    packages=['mako_coverage'],
    install_requires=[
        'Mako >= 1.0',
        'coverage >= 4.0a7',
    ],
)
