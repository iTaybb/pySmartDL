import os
from setuptools import setup

setup(
    name='pySmartDL',
    version='1.1.0',
    url='http://pypi.python.org/pypi/pySmartDL/',
    author='Itay Brandes',
    author_email='itay.brandes+pysmartdl@gmail.com',
    license='Public Domain',
    packages=['pySmartDL'],
    description='A Smart Download Manager for Python',
    long_description=open('README.md').read(),
    install_requires=[
        "threadpool >= 1.2.7",
    ],
    test_suite = "test.test",
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        "License :: Public Domain",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
)
