#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


INSTALL_REQUIRES = [
    'croniter>=0.3.20',
    'pandas>=0.21.0',
    'pandas-bigquery>=0.9.0'
]

setup(
    name='dataleash',
    version='0.1.0',
    description="Framework to manage and run data validity tests",
    long_description=readme(),
    license='Apache License',
    author='Paolo Burelli',
    author_email='paolo@tactile.dk',
    url='https://github.com/tactileentertainment/dataleash',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
    ],
    keywords='data',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    test_suite='tests',
    dependency_links=[
        'git+https://github.com/tactileentertainment/pandas-bigquery.git@prerelease#egg=pandas-bigquery-0.9.0']
)
