#!/usr/bin/env python

import os
from distutils.core import setup

name = 'dropboxfs'
version = '0.3.3'
release = '0'
versrel = version + '-' + release
readme = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = file(readme).read()

setup(
    name=name,
    version=versrel,
    description='A PyFilesystem backend for the Dropbox API.',
    long_description=long_description,
    install_requires=[
        'fs',
        'dropbox',
    ],
    author='Ben Timby',
    author_email='btimby@gmail.com',
    maintainer='Ben Timby',
    maintainer_email='btimby@gmail.com',
    url='http://github.com/btimby/fs-dropbox/',
    license='GPLv3',
    py_modules=['dropboxfs'],
    package_data={'': ['README.rst']},
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
