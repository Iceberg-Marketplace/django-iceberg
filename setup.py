#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


install_requires = []
install_requires.append('requests >= 2.3.0')
version = __import__('django_iceberg').__version__


setup(
    name='django_iceberg',
    version=version,
    description='Django Iceberg',
    author='Iceberg',
    author_email='florian@izberg-marketplace.com',
    url='https://github.com/Modizy/django-iceberg',
    packages=["django_iceberg", "django_iceberg.templatetags", "django_iceberg.models"],
    install_requires=install_requires,
    keywords=['iceberg', 'marketplace', 'saas', 'django'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_data={'django_iceberg': ['templates/django_iceberg/*']}
)
