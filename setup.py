# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='hallgrim',
    version='0.1',
    description='A script generator for the ILIAS platform',
    long_description=readme,
    author='Jan Maximilian Michal',
    author_email='mail-github@jmx.io',
    url='https://gitlab.gwdg.de/j.michal/ilias-generator',
    license=license,
    scripts=['hallgrim/bin/hallgrim'],
    install_requires=['mistune', 'pygments', 'requests', 'requests_toolbelt'],
    packages=['hallgrim']
)
