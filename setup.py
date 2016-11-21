#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from setuptools import setup, find_packages


SERVICE_NAME = 'knogget'


requirements_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')


setup(
    name=SERVICE_NAME,
    description='Record your nuggets of knowledge and do interesting '\
                'things with them (hopefully) '
    version='0.1',
    author='Nicolas Leydet',
    packages=find_packages(),
    install_requires=open(requirements_path).readlines(),
    package_data={'': ['requirements.txt']},
    include_package_data=True,
    entry_points=dict(
        console_scripts=[
            '{0}=knogget.server:run'.format(SERVICE_NAME),
        ],
    ),
)
