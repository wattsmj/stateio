"""
Package installation tool
"""

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='NAStateIO',
    version='0.1.0',
    author='wattsmj',
    license='GPL-3.0',
    url='https://github.com/wattsmj/stateio',
    description='''
    The Network Automation StateIO package provides a programatic
    interface retrieve the state of internetworking devices''',
    long_description=README,
    packages=find_packages(),
    install_requires=['netmiko']
)
