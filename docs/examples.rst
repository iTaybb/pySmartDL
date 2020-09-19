Code Examples
===================================
Here are code examples for the pySmartDL module:

=============================================
Example 1: Downloading a file and running it
=============================================
::

	from pySmartDL import SmartDL

	url = "https://github.com/iTaybb/pySmartDL/raw/master/test/7za920.zip"
	dest = "C:\\Downloads\\" # or '~/Downloads/' on linux

	obj = SmartDL(url, dest)
	obj.start()
	# [*] 0.23 / 0.37 MB @ 88.00KB/s [##########--------] [60%, 2s left]

	path = obj.get_dest()

==================================================================================
Example 2: Downloading a file to a temporarily location, not showing progress bar
==================================================================================
::

	from pySmartDL import SmartDL
	 
	url = "https://github.com/iTaybb/pySmartDL/raw/master/test/7za920.zip"
	obj = SmartDL(url, progress_bar=False) # Because we didn't pass a destination path to the constructor, temporary path was chosen.
	obj.start()
	
	# Do something with obj.get_dest()

======================================
Example 3: Mirrors are also supported
======================================
::

	from pySmartDL import SmartDL
	 
	urls = ["http://totally_fake_website/7za.zip" ,"https://github.com/iTaybb/pySmartDL/raw/master/test/7za920.zip"]
	obj = SmartDL(urls, progress_bar=False)
	obj.start()
	
	print(obj.isSuccessful()) # Returns True, even though the first link is not working.

	# Do something with obj.get_dest()

=============================================================
Example 4: Passing custom options to urllib.request.Request()
=============================================================
::

	from pySmartDL import SmartDL

	request_args = {"headers": {"User-Agent": "pySmartDL/1.3.2"}}
	obj = SmartDL("http://httpbin.org/headers", request_args=request_args, progress_bar=False)
	obj.start()

	data = obj.get_json()
	print(data)


==================================================================
Example 5: Fetch data to memory instead of reading it from a file
==================================================================
::

	from pySmartDL import SmartDL
	 
	url = "http://wiki.python.org/moin/Python2orPython3" # it's also possible to pass unsafe and unicode characters in url
	obj = SmartDL(url, progress_bar=False)
	obj.start()

	data = obj.get_data()  # HTML tags!
	
	# Do something with data
	
====================================================================================
Example 6: Use the nonblocking flag and get information during the download process
====================================================================================
::

	import time
	from pySmartDL import SmartDL
	 
	url_100mb_file = ['http://www.ovh.net/files/100Mio.dat']
	obj = SmartDL(url_100mb_file, progress_bar=False)
	obj.start(blocking=False)

	while not obj.isFinished():
		print("Speed: %s" % obj.get_speed(human=True))
		print("Already downloaded: %s" % obj.get_dl_size(human=True))
		print("Eta: %s" % obj.get_eta(human=True))
		print("Progress: %d%%" % (obj.get_progress()*100))
		print("Progress bar: %s" % obj.get_progress_bar())
		print("Status: %s" % obj.get_status())
		print("\n"*2+"="*50+"\n"*2)
		time.sleep(0.2)
		
	if obj.isSuccessful():
		print("downloaded file to '%s'" % obj.get_dest())
		print("download task took %ss" % obj.get_dl_time(human=True))
		print("File hashes:")
		print(" * MD5: %s" % obj.get_data_hash('md5'))
		print(" * SHA1: %s" % obj.get_data_hash('sha1'))
		print(" * SHA256: %s" % obj.get_data_hash('sha256'))
	else:
		print("There were some errors:")
		for e in obj.get_errors():
			print(str(e))

	# Do something with obj.get_dest()
	
=========================
Example 7: Hash checking
=========================

Example with passing `blocking=True` to `obj.start()`::

	from pySmartDL import SmartDL, HashFailedException
	 
	urls = ["https://github.com/iTaybb/pySmartDL/raw/master/test/7za920.zip",
			"http://www.bevc.net/dl/7za920.zip",
			"http://ftp.jaist.ac.jp/pub/sourceforge/s/project/se/sevenzip/7-Zip/9.20/7za920.zip",
			"http://www.mirrorservice.org/sites/downloads.sourceforge.net/s/se/sevenzip/7-Zip/9.20/7za920.zip"]
	
	obj = SmartDL(urls, progress_bar=False)  # use connect_default_logger=True if you'd like to get debugging info to the console
	obj.add_hash_verification('sha256' ,'2a3afe19c180f8373fa02ff00254d5394fec0349f5804e0ad2f6067854ff28ac')
	try:
		obj.start()
		# Do something with obj.get_dest()
	except HashFailedException:
		print("Hash check failed!")
	
Example with passing `blocking=False` to `obj.start()`::

	from pySmartDL import SmartDL
	 
	urls = ["https://github.com/iTaybb/pySmartDL/raw/master/test/7za920.zip",
			"http://www.bevc.net/dl/7za920.zip",
			"http://ftp.jaist.ac.jp/pub/sourceforge/s/project/se/sevenzip/7-Zip/9.20/7za920.zip",
			"http://www.mirrorservice.org/sites/downloads.sourceforge.net/s/se/sevenzip/7-Zip/9.20/7za920.zip"]
	
	obj = SmartDL(urls, progress_bar=False) # use connect_default_logger=True if you'd like to get debugging info to the console
	obj.add_hash_verification('sha256' ,'2a3afe19c180f8373fa02ff00254d5394fec0349f5804e0ad2f6067854ff28ac')
	obj.start(blocking=False)

	while not obj.isFinished():
		do_your_stuff()
	if obj.isSuccessful():
		print("Success!")
		# Do something with obj.get_dest()
	else:
		print("Download failed with the following exceptions:")
		for e in obj.get_errors():
			print(unicode(e))

==============================
Example 8: No ssl verification
==============================
::

	from pySmartDL import SmartDL

	obj = SmartDL("https://github.com/iTaybb/pySmartDL/raw/master/test/7za920.zip", verify=False)
	obj.start()

	# Do something with obj.get_dest()
