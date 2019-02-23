Documentation
===================================

===========
Basic usage
===========

Basic usage::

	from pySmartDL import SmartDL

	url = "https://github.com/iTaybb/pySmartDL/raw/master/test/7za920.zip"
	dest = "C:\\Downloads\\" # or '~/Downloads/' on linux

	obj = SmartDL(url, dest)
	obj.start()
	# [*] 0.23 Mb / 0.37 Mb @ 88.00Kb/s [##########--------] [60%, 2s left]

	path = obj.get_dest()

For more examples please refer to the :doc:`examples` page.

===============================
pySmartDL.SmartDL (main class)
===============================
	
.. automodule:: pySmartDL

	.. autoclass:: pySmartDL.SmartDL
		:members:
		
===========
Exceptions
===========
The following exceptions may be raised:

 .. exception:: HashFailedException
 
	May be raised when hash check fails.
	
 .. exception:: CanceledException
 
	Raised when user cancels the task with `SmartDL.stop()`.
	
 .. exception:: urllib2.HTTPError
 
	May be raised due to problems with the servers. Read more on the `official documentation <http://docs.python.org/2/library/urllib2.html#urllib2.HTTPError>`_.
	
 .. exception:: urllib2.URLError
 
	May be raised due to problems while reaching the servers. Read more on the `official documentation <http://docs.python.org/2/library/urllib2.html#urllib2.URLError>`_.
	
 .. exception:: exceptions.IOError
 
	May be raised due to any local I/O problems (such as `no disk space available`). Read more on the `official documentation <http://docs.python.org/2/library/exceptions.html#exceptions.IOError>`_.
	
.. warning::
	If you're using the non-blocking mode, Exceptions won't be raised. In that case, call
	`isSuccessful()` after the task is finished, to make sure the download succeeded. Call
	`get_errors()` to get the the exceptions.

==============================
pySmartDL.utils (helper class)
==============================

.. automodule:: pySmartDL.utils
	:members: