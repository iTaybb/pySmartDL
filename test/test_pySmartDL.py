import os
import sys
import random
import time
import string
import json
import math
import unittest
import warnings
import tempfile
from pathlib import Path
import socket

sys.path.insert(0, str(Path(__file__).parent.parent))

import pySmartDL

class TestSmartDL(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        self.dl_dir = os.path.join(tempfile.gettempdir(), "".join([random.choice(string.ascii_letters+string.digits) for i in range(8)]), '')
        while os.path.exists(self.dl_dir):
            self.dl_dir = os.path.join(tempfile.gettempdir(), "".join([random.choice(string.ascii_letters+string.digits) for i in range(8)]), '')
            
        self.res_7za920_mirrors = [
            "https://github.com/iTaybb/pySmartDL/raw/master/test/7za920.zip",
            "https://sourceforge.mirrorservice.org/s/se/sevenzip/7-Zip/9.20/7za920.zip",
            "http://www.bevc.net/dl/7za920.zip",
            "http://ftp.psu.ru/tools/7-zip/stable/7za920.zip",
            "http://www.mirrorservice.org/sites/downloads.sourceforge.net/s/se/sevenzip/7-Zip/9.20/7za920.zip"
        ]
        self.res_7za920_hash = '2a3afe19c180f8373fa02ff00254d5394fec0349f5804e0ad2f6067854ff28ac'
        self.res_testfile_1gb = 'https://speed.hetzner.de/1GB.bin'
        self.res_testfile_100mb = 'https://speed.hetzner.de/100MB.bin'
        self.enable_logging = "-vvv" in sys.argv

    def test_dependencies(self):
        self.assertTrue(sys.version_info >= (3, 4))
    
    def test_download(self):
        obj = pySmartDL.SmartDL(self.res_7za920_mirrors, dest=self.dl_dir, progress_bar=False, connect_default_logger=self.enable_logging)
        obj.start()

        data = obj.get_data(binary=True, bytes=2)
        
        self.assertEqual(data, b'PK')
    
    def test_mirrors(self):
        urls = ["http://totally_fake_website/7za.zip", "https://github.com/iTaybb/pySmartDL/raw/master/test/7za920.zip"]
        obj = pySmartDL.SmartDL(urls, dest=self.dl_dir, progress_bar=False, connect_default_logger=self.enable_logging)
        obj.start()
        
        self.assertTrue(obj.isSuccessful())
        
    def test_hash(self):
        obj = pySmartDL.SmartDL(self.res_7za920_mirrors, progress_bar=False, connect_default_logger=self.enable_logging)
        obj.add_hash_verification('sha256' , self.res_7za920_hash)  # good hash
        obj.start(blocking=False)  # no exceptions
        obj.wait()
        
        self.assertTrue(obj.isSuccessful())
        
        obj = pySmartDL.SmartDL(self.res_7za920_mirrors, progress_bar=False, connect_default_logger=self.enable_logging)
        obj.add_hash_verification('sha256' ,'a'*64)  # bad hash
        obj.start(blocking=False)  # no exceptions
        obj.wait()
        
        self.assertFalse(obj.isSuccessful())
        self.assertTrue(any([isinstance(e, pySmartDL.HashFailedException) for e in obj.get_errors()]))
        
    def test_pause_unpause(self, testfile=None):
        obj = pySmartDL.SmartDL(testfile if testfile else self.res_7za920_mirrors, dest=self.dl_dir, progress_bar=False, connect_default_logger=self.enable_logging)
        obj.start(blocking=False)
        
        while not obj.get_dl_size():
            time.sleep(0.1)
        
        # pause
        obj.pause()
        time.sleep(0.5)
        if obj.get_status() == "finished":
            # too bad, the file was too small and was downloaded complectely until we stopped it.
            # We should download a bigger file
            if self.res_testfile_100mb == testfile:
                self.fail("The download got completed before we could stop it, even though we've used a big file. Are we on a 100GB/s connection to the Internet or someting?")
            return self.test_pause_unpause(testfile=self.res_testfile_100mb)
        
        dl_size = obj.get_dl_size()

        # verify download has really stopped
        time.sleep(2.5)
        self.assertEqual(dl_size, obj.get_dl_size())
        
        # continue
        obj.unpause()
        time.sleep(2.5)
        self.assertNotEqual(dl_size, obj.get_dl_size())
        
        obj.wait()
        self.assertTrue(obj.isSuccessful())

    def test_stop(self):
        obj = pySmartDL.SmartDL(self.res_testfile_100mb, dest=self.dl_dir, progress_bar=False, connect_default_logger=self.enable_logging)
        obj.start(blocking=False)

        while not obj.get_dl_size():
            time.sleep(0.1)

        obj.stop()
        obj.wait()
        self.assertFalse(obj.isSuccessful())

    def test_speed_limiting(self):
        obj = pySmartDL.SmartDL(self.res_testfile_1gb, dest=self.dl_dir, progress_bar=False, connect_default_logger=self.enable_logging)
        obj.limit_speed(1024**2)  # 1MB per sec
        obj.start(blocking=False)

        while not obj.get_dl_size():
            time.sleep(0.1)

        time.sleep(30)

        expected_dl_size = 30 * 1024**2
        allowed_delta = 0.6 #  because we took only 30sec, the delta needs to be quite big, it we were to test 60sec the delta would probably be much smaller
        diff = math.fabs(expected_dl_size - obj.get_dl_size()) / expected_dl_size

        obj.stop()
        obj.wait()

        self.assertLessEqual(diff, allowed_delta)
    
    def test_basic_auth(self):
        basic_auth_test_url = "https://httpbin.org/basic-auth/user/passwd"
        obj = pySmartDL.SmartDL(basic_auth_test_url, progress_bar=False, connect_default_logger=self.enable_logging)
        obj.add_basic_authentication('user', 'passwd')
        obj.start()
        data = obj.get_data()
        self.assertTrue(json.loads(data)['authenticated'])
        
    def test_unicode(self):
        url = "https://he.wikipedia.org/wiki/ג'חנון"
        obj = pySmartDL.SmartDL(url, progress_bar=False, connect_default_logger=self.enable_logging)
        obj.start()

    def test_timeout(self):
        self.assertRaises(socket.timeout, pySmartDL.SmartDL, "https://httpbin.org/delay/10", progress_bar=False, timeout=3, connect_default_logger=self.enable_logging)

        obj = pySmartDL.SmartDL("https://httpbin.org/delay/3", progress_bar=False, timeout=15, connect_default_logger=self.enable_logging)
        obj.start(blocking=False)
        obj.wait()
        self.assertTrue(obj.isSuccessful())
        
def test_suite():
    suite = unittest.makeSuite(TestSmartDL)
    return suite

if __name__ == '__main__':
    unittest.main(verbosity=2)
