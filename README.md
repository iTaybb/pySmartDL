==========================================
pySmartDL (Python Smart Download Manager)
==========================================

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

@Itay Brandes.