# Copyright (C) 2012-2013 Itay Brandes
'''
The Utils class contains many functions for project-wide use.
'''

import os
import urlparse
import urllib
import urllib2
import random
import logging

def combine_files(parts, dest):
    '''
    Combines files.
    
    :param parts: Source files.
    :type parts: list of strings
    :param dest: Destination file.
    :type dest: string
    
    '''
    with open(dest, 'wb') as output:
        for part in parts:
            with open(part, 'rb') as f:
                output.writelines(f.readlines())
            os.remove(part)
            
def url_fix(s, charset='utf-8'):
    '''
    Sometimes you get an URL by a user that just isn't a real
    URL because it contains unsafe characters like ' ' and so on.  This
    function can fix some of the problems in a similar way browsers
    handle data entered by the user:

    >>> url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffskl?rung)')
    'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

    :param s: Url address.
    :type s: string
    :param charset: The target charset for the URL if the url was
                    given as unicode string. Default is 'utf-8'.
    :type charset: string
    :rtype: string
                    
    (taken from `werkzeug.utils <http://werkzeug.pocoo.org/docs/utils/>`_)
    '''
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))
    
def progress_bar(progress, length=20):
    '''
    Returns a textual progress bar.
    
    >>> progress_bar(0.6)
    '[##########--------]'
    
    :param progress: Number between 0 and 1 describes the progress.
    :type progress: float
    :param length: The length of the progress bar in chars. Default is 20.
    :type length: int
    :rtype: string
    '''
    length -= 2 # The brackets are 2 chars long.
    if progress < 0:
        progress = 0
    if progress > 1:
        progress = 1
    return "[" + "#"*int(progress*length) + "-"*(length-int(progress*length)) + "]"
    
def is_HTTPRange_supported(url, timeout=15):
    '''
    Checks if a server allows `Byte serving <https://en.wikipedia.org/wiki/Byte_serving>`_,
    using the Range HTTP request header and the Accept-Ranges and Content-Range HTTP response headers.
    
    :param url: Url address.
    :type url: string
    :param timeout: Timeout in seconds. Default is 15.
    :type timeout: int
    :rtype: bool
    '''
    url = url.replace(' ', '%20')
    
    fullsize = get_filesize(url)
    if not fullsize:
        return False
    
    headers = {'Range': 'bytes=0-3'}
    req = urllib2.Request(url, headers=headers)
    urlObj = urllib2.urlopen(req, timeout=timeout)
        
    meta = urlObj.info()
    filesize = int(meta.getheaders("Content-Length")[0])
    
    urlObj.close()
    return (filesize != fullsize)

def get_filesize(url, timeout=15):
    '''
    Fetches file's size of a file over HTTP.
    
    :param url: Url address.
    :type url: string
    :param timeout: Timeout in seconds. Default is 15.
    :type timeout: int
    :returns: Size in bytes.
    :rtype: int
    '''
    url = url_fix(url)
    try:
        u = urllib2.urlopen(url, timeout=timeout)
    except (urllib2.HTTPError, urllib2.URLError) as e:
        return 0
    meta = u.info()
    try:
        file_size = int(meta.getheaders("Content-Length")[0])
    except IndexError:
        return 0
        
    return file_size
    
def get_random_useragent():
    '''
    Returns a random popular user-agent.
    Taken from <http://techblog.willshouse.com/2012/01/03/most-common-user-agents/>_, last updated on 01/01/2014.
    
    :returns: user-agent
    :rtype: str
    '''
    l = [   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9) AppleWebKit/537.71 (KHTML, like Gecko) Version/7.0 Safari/537.71',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/7.0.1 Safari/537.73.11',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0',
                ]
    return random.choice(l)
    
def create_debugging_logger():
    '''
    Creates a debugging logger that prints to console.
    
    :rtype: `logging.Logger` instance
    '''
    t_log = logging.getLogger('testingLog')
    t_log.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # console.setFormatter(logging.Formatter('[%(levelname)s@%(thread)d] %(message)s'))
    console.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    t_log.addHandler(console)
    return t_log
    
class DummyLogger(object):
    '''
    A dummy logger. You can call `debug()`, `warning()`, etc on this object, and nothing will happen.
    '''
    def __init__(self):
        pass

    def dummy_func(self, *args, **kargs):
        pass

    def __getattr__(self, name):
        if name.startswith('__'):
            return object.__getattr__(name)
        return self.dummy_func