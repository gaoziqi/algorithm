import random
import requests
import threading
from bs4 import BeautifulSoup


class Proxy(object):

    def __init__(self, min_pool=5, timeout=60):
        super(Proxy, self).__init__()
        min_pool = int(min_pool)
        timeout = int(timeout)
        self.min_pool = 5 if min_pool < 2 else min_pool
        self.timeout = 60 if timeout < 5 else timeout
        self.mutex = threading.Lock()
        self.pool = {'xici': [[], []]}

    def IP(self, _type=0, url='xici', check=True):
        '''
        获取代理IP

        :_type: 透明0，高匿1，默认(0)
        :url: 代理获取网址，默认(xici)
        :check: 是否验证
        :returns: {}
        '''
        result = {}
        while not result:
            self._addIP(_type, url)
            if self.mutex.acquire():
                i = random.randint(0, len(self.pool[url][_type]) - 1)
                p = self.pool[url][_type][i]
                result = {'http': "http://%s:%s" % p}
                if check:
                    if not self._check(result):
                        self.pool[url][_type].pop(i)
                        result = {}
                self.mutex.release()
        return result

    def _addIP(self, _type=0, url='xici'):
        i = 0
        while len(self.pool[url][_type]) < self.min_pool:
            i += 1
            if self.mutex.acquire():
                if len(self.pool[url][_type]) < self.min_pool:
                    self._getIP(_type, url)
                self.mutex.release()
            if i > 5:
                print("min_pool is too large!")
                raise

    def _getIP(self, _type, url):
        if url == 'xici':
            if _type == 0:
                _url = 'http://www.xicidaili.com/nt'
            else:
                _url = 'http://www.xicidaili.com/nn'
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': 'www.xicidaili.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWekit/537.36 (KHTML,\
                like Gecko) Chrome/54.0.2840.71 Safari/537.36'
            }
            try:
                r = requests.get(_url, headers=headers, timeout=self.timeout)
            except:
                return
            soup = BeautifulSoup(r.text, 'html.parser')
            tr = soup.select("#ip_list > tr")
            tr.pop(0)
            for d in tr:
                td = d.select('td')
                self.pool[url][_type].append((td[1].text, td[2].text))
        else:
            print("url not define")
            raise

    def _check(self, proxies):
        url = "http://www.baidu.com"
        try:
            r = requests.get(url, timeout=self.timeout, proxies=proxies)
        except:
            return False
        return r.status_code == 200
