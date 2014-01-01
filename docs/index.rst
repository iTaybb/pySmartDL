.. SmartDL documentation master file, created by
   sphinx-quickstart on Sat Jun 29 13:36:18 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PySmartDL's documentation!
=====================================

``pySmartDL`` strives to be a full-pleged smart download manager for Python.
Typical usage often looks like this::

	import os
	from pySmartDL import SmartDL

	url = "http://mirror.ufs.ac.za/7zip/9.20/7za920.zip"
	dest = "C:\\Downloads\\"

	obj = SmartDL(url, dest)
	obj.start()

	# [*] 0.23 / 0.37 MB @ 88.00KB/s [##########--------] [60%, 2s left]

	os.startfile(obj.get_dest()) # get_dest() returns the destination of the downloaded file.

==============
Main Features
==============

* Built-in download acceleration (with the `multipart downloading technique <http://stackoverflow.com/questions/93642/how-do-download-accelerators-work>`_).
* Mirrors support.
* Pause/Unpause feature.
* Hash checking.
* Non-blocking, shows progress bar, download speed and eta.

==============
Prerequisites
==============

PySmartDL works with Python 2.7. The `threadpool  <https://pypi.python.org/pypi/threadpool>`_ module needs to be installed before first running pySmartDL.

===
FAQ
===
Q: How do I make a feature request?
A: Mail me your ideas and also don't forget to tell me the benefits.  

Q: I found a bug. How should I report it?  
A: Mail me the details.  
   Try to give as many details as possible, especially describe the necessary  
   steps to reproduce the bug.  
   
Q: How can I access the source code?  
A: You're more than welcome to visit our github repository: https://github.com/iTaybb/pySmartDL

Documentation
=====================================

.. toctree::
   :maxdepth: 2
   
   examples
   code
   notes
   todo

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

