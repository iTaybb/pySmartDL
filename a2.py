import time
from pySmartDL import SmartDL

url_100mb_file = ['http://www.debian.co.il/debian-cd/7.5.0/i386/iso-cd/debian-7.5.0-i386-netinst.iso']
# url_100mb_file = "http://httpbin.org/basic-auth/user/passwd"
# url_100mb_file = "http://cachefly.cachefly.net/100mb.test"
url_100mb_file = 'https://r1---sn-ivuoxu-ua8l.googlevideo.com/videoplayback?requiressl=yes&sver=3&signature=B08C02FDEDC76633D28EA9F72121F341BD471250.CD791E123F116CE2E480BCDEED4268DE35934249&itag=84&id=o-ALsVuxK7RU-9cWXebyXGLBf3xiFZN7N6aMkvkpevG9Jm&sparams=id%2Cip%2Cipbits%2Citag%2Cpcm2%2Cratebypass%2Crequiressl%2Csource%2Cupn%2Cexpire&ms=au&upn=k-0bari8bTI&mt=1399282666&expire=1399304082&mv=m&pcm2=yes&source=youtube&fexp=933905%2C935501%2C939936%2C945033%2C929305%2C932936%2C937417%2C913434%2C923341%2C936923%2C902408%2C945044&ipbits=0&ratebypass=yes&ip=37.142.247.11&key=yt5&mws=yes'
obj = SmartDL(url_100mb_file, progress_bar=False, connect_default_logger=True)
# obj.add_basic_authentication('user', 'passwd')
# obj.fetch_hash_sums()
# import pdb; pdb.set_trace()
obj.start(blocking=False)
import pdb; pdb.set_trace()

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