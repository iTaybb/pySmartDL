# Copyright (C) 2014 Itay Brandes
import os
import sys
import random
import time
import string
import unittest

sys.path.append(r'..')
from pySmartDL import SmartDL, HashFailedException, CanceledException
import pySmartDL

#
# Test code
#

class TestSmartDL(unittest.TestCase):
    def setUp(self):
        self.dl_dir = os.path.join(os.getenv('tmp'), "".join([random.choice(string.ascii_letters+string.digits) for i in range(8)]), '')
        while os.path.exists(self.dl_dir):
            self.dl_dir = os.path.join(os.getenv('tmp'), "".join([random.choice(string.ascii_letters+string.digits) for i in range(8)]), '')
            
        self.default_7za920_mirrors = [ "http://mirror.ufs.ac.za/7zip/9.20/7za920.zip",
                                        "http://www.bevc.net/dl/7za920.zip",
                                        "http://ftp.jaist.ac.jp/pub/sourceforge/s/project/se/sevenzip/7-Zip/9.20/7za920.zip",
                                        "http://www.mirrorservice.org/sites/downloads.sourceforge.net/s/se/sevenzip/7-Zip/9.20/7za920.zip"]
                                        
    def test_dependencies(self):
        self.assertTrue(sys.version_info >= (2,6))
        
        if sys.version_info < (3,2):
            from concurrent import futures
    
    def test_download(self):
        obj = SmartDL(self.default_7za920_mirrors, dest=self.dl_dir, progress_bar=False)
        obj.start()

        data = obj.get_data(binary=True, bytes=2)
        
        if sys.version_info >= (3,):
            self.assertEqual(data, b'PK')
        else:
            self.assertEqual(data, 'PK')
    
    def test_mirrors(self):
        urls = ["http://totally_fake_website/7za.zip" ,"http://mirror.ufs.ac.za/7zip/9.20/7za920.zip"]
        obj = SmartDL(urls, dest=self.dl_dir, progress_bar=False)
        obj.start()
        
        self.assertTrue(obj.isSuccessful())
        
    def test_hash(self):
        obj = SmartDL(self.default_7za920_mirrors, progress_bar=False)
        obj.add_hash_verification('sha256' ,'2a3afe19c180f8373fa02ff00254d5394fec0349f5804e0ad2f6067854ff28ac') # good hash
        obj.start(blocking=False) # no exceptions
        obj.wait()
        
        self.assertTrue(obj.isSuccessful())
        
        obj = SmartDL(self.default_7za920_mirrors, progress_bar=False)
        obj.add_hash_verification('sha256' ,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') # bad hash
        obj.start(blocking=False) # no exceptions
        obj.wait()
        
        self.assertFalse(obj.isSuccessful())
        self.assertTrue(isinstance(obj.get_errors()[-1], HashFailedException))
        
    def test_pause_unpause_stop(self):
        obj = SmartDL(self.default_7za920_mirrors, dest=self.dl_dir, progress_bar=False)
        obj.start(blocking=False)
        
        while not obj.get_dl_size():
            time.sleep(0.2)
            
        time.sleep(1)
        obj.pause()
        time.sleep(0.5)
        dl_size = obj.get_dl_size()
        time.sleep(2.5)
        self.assertEqual(dl_size, obj.get_dl_size())
        
        obj.unpause()
        time.sleep(0.5)
        self.assertNotEqual(dl_size, obj.get_dl_size())
        
        obj.stop()
        obj.wait()
        self.assertFalse(obj.isSuccessful())
        # self.assertTrue(isinstance(obj.get_errors()[-1], pySmartDL.CanceledException), msg=str(obj.get_errors()[-1]))

if __name__ == '__main__':
    if sys.version_info < (2,7):
        unittest.main()
    else:
        unittest.main(verbosity=2)