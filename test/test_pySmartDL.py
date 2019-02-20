# -*- coding: utf-8 -*-

import os
import sys
import random
import time
import string
import json
import math
import unittest
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pySmartDL

#
# Test code
#

class TestSmartDL(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        self.dl_dir = os.path.join(os.getenv('tmp'), "".join([random.choice(string.ascii_letters+string.digits) for i in range(8)]), '')
        while os.path.exists(self.dl_dir):
            self.dl_dir = os.path.join(os.getenv('tmp'), "".join([random.choice(string.ascii_letters+string.digits) for i in range(8)]), '')
            
        self.res_7za920_mirrors = [
            "https://github.com/iTaybb/pySmartDL/raw/master/test/7za920.zip",
            "https://sourceforge.mirrorservice.org/s/se/sevenzip/7-Zip/9.20/7za920.zip",
            "http://www.bevc.net/dl/7za920.zip",
            "http://ftp.psu.ru/tools/7-zip/stable/7za920.zip",
            "http://www.mirrorservice.org/sites/downloads.sourceforge.net/s/se/sevenzip/7-Zip/9.20/7za920.zip",
            "http://helpdesk.cki.tl/7za920.zip"
        ]
        self.res_7za920_hash = '2a3afe19c180f8373fa02ff00254d5394fec0349f5804e0ad2f6067854ff28ac'
        self.res_testfile_1gb = 'https://speed.hetzner.de/1GB.bin'

    def test_dependencies(self):
        self.assertTrue(sys.version_info >= (3, 4))
    
    def test_download(self):
        obj = pySmartDL.SmartDL(self.res_7za920_mirrors, dest=self.dl_dir, progress_bar=False)
        obj.start()

        data = obj.get_data(binary=True, bytes=2)
        
        self.assertEqual(data, b'PK')
    
    def test_mirrors(self):
        urls = ["http://totally_fake_website/7za.zip", "https://github.com/iTaybb/pySmartDL/raw/master/test/7za920.zip"]
        obj = pySmartDL.SmartDL(urls, dest=self.dl_dir, progress_bar=False)
        obj.start()
        
        self.assertTrue(obj.isSuccessful())
        
    def test_hash(self):
        obj = pySmartDL.SmartDL(self.res_7za920_mirrors, progress_bar=False)
        obj.add_hash_verification('sha256' , self.res_7za920_hash) # good hash
        obj.start(blocking=False)  # no exceptions
        obj.wait()
        
        self.assertTrue(obj.isSuccessful())
        
        obj = pySmartDL.SmartDL(self.res_7za920_mirrors, progress_bar=False)
        obj.add_hash_verification('sha256' ,'a'*64)  # bad hash
        obj.start(blocking=False)  # no exceptions
        obj.wait()
        
        self.assertFalse(obj.isSuccessful())
        self.assertTrue(isinstance(obj.get_errors()[-1], pySmartDL.HashFailedException))
        
    def test_pause_unpause(self):
        obj = pySmartDL.SmartDL(self.res_7za920_mirrors, dest=self.dl_dir, progress_bar=False)
        obj.start(blocking=False)
        
        while not obj.get_dl_size():
            time.sleep(0.1)
        
        # pause
        obj.pause()
        time.sleep(0.5)
        dl_size = obj.get_dl_size()

        # verify download has really stopped
        time.sleep(2.5)
        self.assertEqual(dl_size, obj.get_dl_size())
        
        # continue
        obj.unpause()
        time.sleep(1)
        self.assertNotEqual(dl_size, obj.get_dl_size())
        
        obj.wait()
        self.assertTrue(obj.isSuccessful())

    def test_stop(self):
        obj = pySmartDL.SmartDL(self.res_7za920_mirrors, dest=self.dl_dir, progress_bar=False)
        obj.start(blocking=False)

        while not obj.get_dl_size():
            time.sleep(0.1)

        obj.stop()
        obj.wait()
        self.assertFalse(obj.isSuccessful())

    def test_speed_limiting(self):
        obj = pySmartDL.SmartDL(self.res_testfile_1gb, dest=self.dl_dir, progress_bar=False)
        obj.limit_speed(1 * 1024**2)  # 1MB per sec
        obj.start(blocking=False)

        while not obj.get_dl_size():
            time.sleep(0.1)

        time.sleep(10)

        expected_dl_size = 10 * 1024**2  # after 10 seconds, we should of downloaded max of 5MB
        allowed_delta = 0.25 #  because we took only 10sec, the delta needs to be quite big, it we were to test 30sec the delta would probably be much smaller
        diff = math.fabs(expected_dl_size - obj.get_dl_size()) / expected_dl_size

        obj.stop()
        obj.wait()

        self.assertLessEqual(diff, allowed_delta)
    
    def test_basic_auth(self):
        basic_auth_test_url = "https://httpbin.org/basic-auth/user/passwd"
        obj = pySmartDL.SmartDL(basic_auth_test_url, progress_bar=False)
        obj.add_basic_authentication('user', 'passwd')
        obj.start()
        data = obj.get_data()
        self.assertTrue(json.loads(data)['authenticated'])
        
    def test_unicode(self):
        url = "https://he.wikipedia.org/wiki/ג'חנון"
        obj = pySmartDL.SmartDL(url, progress_bar=False)
        obj.start()
        
def test_suite():
    suite = unittest.makeSuite(TestSmartDL)
    return suite

if __name__ == '__main__':
    unittest.main(verbosity=2)
