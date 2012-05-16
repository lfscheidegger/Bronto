# Bronto - jasmine-like tests for Python
# Copyright (C) 2012 Luiz Scheidegger

"""
setup.py
Setup script to install bronto.
"""

from setuptools import setup

setup(
    name = "bronto",
    version = "0.1",
    packages = ['bronto'],
    entry_points = {
        'console_scripts': [
            'bronto = bronto.main:main'
        ]
    }
)
