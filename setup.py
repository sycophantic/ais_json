#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for the Python AIS JSON Gateway.

:author: Daniel J. Grinkevich
:copyright: Copyright 2017 Daniel J. Grinkevich
:license: GNU General Public License, Version 3
:source: <https://github.com/ampledata/ais_json>
"""

import os
import sys

import setuptools

__title__ = 'ais_json'
__version__ = '1.0.0b1'
__author__ = 'Daniel J. Grinkevich'  # NOQA pylint: disable=R0801
__copyright__ = 'Copyright 2017 Daniel J. Grinkevich'  # NOQA pylint: disable=R0801
__license__ = 'GNU General Public License, Version 3'  # NOQA pylint: disable=R0801


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist')
        os.system('twine upload dist/*')
        sys.exit()


publish()


setuptools.setup(
    name=__title__,
    version=__version__,
    description='Python AIS JSON Gateway.',
    author='Daniel J. Grinkevich',
    author_email='oss@undef.net',
    packages=['ais_json'],
    package_data={'': ['LICENSE']},
    package_dir={'ais_json': 'ais_json'},
    license=open('LICENSE').read(),
    long_description=open('README.md').read(),
    url='https://github.com/ampledata/ais_json',
    zip_safe=False,
    include_package_data=True,
    install_requires=['requests >= 2.7.0', 'libais >= 0.16'],
    entry_points={'console_scripts': ['ais_json = ais_json.cmd:cli']}
)
