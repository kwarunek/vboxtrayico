#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="vboxtrayico",
    packages=['vboxtrayico'],
    version="0.1.9",
    author="Krzysztof Warunek",
    author_email="kalmaceta@gmail.com",
    description="Virtualbox tray tool - list/start/stop VMs",
    license="MIT",
    keywords="virtualbox tray vm pyside",
    url="https://github.com/kAlmAcetA/vboxtrayico",
    long_description='Virtualbox icon tray. Quick access start/stop VMs',
    scripts=['scripts/vboxtrayico']
)
