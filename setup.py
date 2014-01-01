import os
from setuptools import setup

setup(
    name='pySmartDL',
    version='1.0.0',
    url='http://pypi.python.org/pypi/pySmartDL/',
    author='Itay Brandes',
    author_email='itay.brandes+pysmartdl@gmail.com',
    license='Public Domain',
    packages=['pySmartDL'],
    description='A Smart Download Manager for Python',
    long_description=open('README.txt').read(),
    install_requires=[
        "threadpool >= 1.2.7",
    ],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        "License :: Public Domain",
        "Operating System :: Microsoft",
        "Topic :: Internet :: WWW/HTTP",
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
    ),
)
