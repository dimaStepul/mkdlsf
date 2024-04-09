#!/usr/bin/python
import requests
import ssl
from requests.adapters import HTTPAdapter

try:
    from requests.packages.urllib3.poolmanager import PoolManager
except:
    from urllib3.poolmanager import PoolManager


class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        ssl_version = ssl.PROTOCOL_TLSv1
        # ssl_version=ssl.PROTOCOL_SSLv23
        # ssl_version=ssl.PROTOCOL_SSLv3
        assert_hostname = 'netflix.com'
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block, ssl_version=ssl_version,
                                       assert_hostname=assert_hostname)


def newSession():
    s = requests.Session()
    s.mount('https://', SSLAdapter())
    s.headers.update({
                         'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.6 Safari/537.36'})
    return s


urlMain = "https://vk.com"
session = None
session = newSession()
session.get(urlMain, verify=False).text()
