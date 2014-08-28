#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import sys

if sys.version < '3':
    execfile(os.path.join('django_iceberg', 'version.py'))
else:
    exec(open("django_iceberg/version.py").read())

install_requires = []
install_requires.append('requests >= 2.3.0')

setup(
    name='django_iceberg',
    version=VERSION,
    description='Django Iceberg',
    author='Iceberg',
    author_email='florian@iceberg-marketplace.com',
    url='https://github.com/Modizy/django-iceberg',
    packages = ["django_iceberg","django_iceberg.migrations", "django_iceberg.templates", "django_iceberg.templatetags"],
    install_requires = install_requires,
    keywords = ['iceberg', 'modizy', 'marketplace', 'saas', 'django'],
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
 )
