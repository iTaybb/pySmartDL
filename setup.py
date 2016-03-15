# Copyright (C) 2014-2015 Itay Brandes
import os
import sys
from setuptools import setup, find_packages

extra = {}
if sys.version_info < (3, 2):
    extra['install_requires'] = "futures >= 2.1.6" # backport of py32 concurrent.futures module
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(
    name='pySmartDL',
    version='1.2.5',
    url='http://pypi.python.org/pypi/pySmartDL/',
    author='Itay Brandes',
    author_email='itay.brandes+pysmartdl@gmail.com',
    license='Public Domain',
    packages=find_packages(),
    description='A Smart Download Manager for Python',
    long_description=open('README.md').read(),
    test_suite = "test.test_pySmartDL.test_suite",
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
        "License :: Public Domain",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
    **extra
)
