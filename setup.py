# -*- coding: utf-8 -*-

from setuptools import setup
from hallgrim.custom_markdown import get_markdown

with open('README.md') as f:
    readme = get_markdown()(f.read())

long_description = """
The final data is produced in three steps:

1. A python script file with predefined structure that has to export certain variables in a specified format.
2. An intermediate representation (probably an array that contains relevant data and assumes unknown properties)
3. The XML structure for one or multiple questions, readable by Ilias.
4. An Ilias object packed as .zip file, ready for upload.
"""

setup(
    name='hallgrim',
    version='0.1.3',
    description='A script generator for the ILIAS platform',
    long_description=long_description,
    author='Jan Maximilian Michal',
    author_email='mail-github@jmx.io',
    url='https://gitlab.gwdg.de/j.michal/ilias-generator',
    download_url = 'https://gitlab.gwdg.de/j.michal/ilias-generator/repository/archive.tar.gz?ref=0.1',
    license='MIT',
    scripts=['bin/hallgrim'],
    install_requires=['mistune', 'pygments', 'requests', 'requests_toolbelt'],
    packages=['hallgrim']
)
