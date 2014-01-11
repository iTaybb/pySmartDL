import time
from pySmartDL import SmartDL

url_100mb_file = ['http://ipv4.download.thinkbroadband.com/100MB.zip']
obj = SmartDL(url_100mb_file, progress_bar=False)
obj.start(blocking=False)

while not obj.isFinished():
        print "Speed: %s" % obj.get_speed(human=True)
        print "Already downloaded: %s" % obj.get_dl_size(human=True)
        print "Eta: %s" % obj.get_eta(human=True)
        print "Progress: %d%%" % (obj.get_progress()*100)
        print "Progress bar: %s" % obj.get_progress_bar()
        print "Status: %s" % obj.get_status()
        print "\n"*2+"="*50+"\n"*2
        time.sleep(0.2)

if obj.isSuccessful():
        print "downloaded file to '%s'" % obj.get_dest()
        print "download task took %ss" % obj.get_dl_time(human=True)
        print "File hashes:"
        print " * MD5: %s" % obj.get_data_hash('md5')
        print " * SHA1: %s" % obj.get_data_hash('sha1')
        print " * SHA256: %s" % obj.get_data_hash('sha256')
else:
        print "There were some errors:"
        for e in obj.get_errors():
                print str(e)

# Do something with obj.get_dest()