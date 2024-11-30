#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import BIN

setup(
    name='custom_RMSD',
    version="0.1",
    packages=find_packages(),

    
    install_requires=[
        'numpy',
        'csv',
        'scipy',
        'pandas',
        'matplotlib'
    ],

    entry_points={
        'console_scripts': [
            
        ]
    }
)