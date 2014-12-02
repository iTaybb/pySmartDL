==========================================
Python Smart Download Manager -- pySmartDL
==========================================

``pySmartDL`` strives to be a full-pleged smart download manager for Python. Main features:

* Built-in download acceleration (with the `multipart downloading technique <http://stackoverflow.com/questions/93642/how-do-download-accelerators-work>`_).
* Mirrors support.
* Pause/Unpause feature.
* Hash checking.
* Non-blocking, shows progress bar, download speed and eta.
* Python 3 Support

Project Links
=============

 * Downloads: http://pypi.python.org/pypi/pySmartDL/
 * Documentation: http://itaybb.github.io/pySmartDL/
 * Project page: https://github.com/iTaybb/pySmartDL/
 * Bugs and Issues: https://github.com/iTaybb/pySmartDL/issues
 
Installation
============

**Using pip**

    Make sure python-pip is installed on you system. If you are using virtualenv, then pip is alredy installed into environments created by virtualenv. Run pip to install pySmartDL:

    ``pip install pySmartDL``

**From Source**

    The pySmartDL package is installed from source using distutils in the usual way.  Download the `source distribution <http://pypi.python.org/pypi/pySmartDL>`_ first.  Unpack the source zip and run the following to install the package site-wide:

    ``python setup.py install``
 
Usage
=====

Download is as simple as creating an instance and launching it::

	import os
	from pySmartDL import SmartDL

	url = "http://mirror.ufs.ac.za/7zip/9.20/7za920.zip"
	dest = "C:\\Downloads\\" # or '~/Downloads/' on linux

	obj = SmartDL(url, dest)
	obj.start()
	# [*] 0.23 Mb / 0.37 Mb @ 88.00Kb/s [##########--------] [60%, 2s left]

	path = obj.get_dest()

==============
Requirements
==============

 * Python 2.6 or greater.
 * Python 3.0 or greater.
 * For versions before Python 3.2, the `futures backport  <https://pypi.python.org/pypi/futures>`_ package is also required.

Copyright (C) 2014-2015 Itay Brandes.