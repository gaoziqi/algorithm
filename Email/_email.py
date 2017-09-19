import time
import json
import hashlib
import requests
from bs4 import BeautifulSoup


class Email(object):

    def __init__(self, proxy={}, timeout=60, obj='bccto'):
        super(Email, self).__init__()
        timeout = 60 if timeout < 5 else int(timeout)
        if type(proxy) is not dict:
            proxy = {}
        if obj == 'bccto':
            self.obj = _Bccto(proxy=proxy, timeout=timeout)
        else:
            print("UNKNOW OBJ")
            raise
        self.m5 = hashlib.md5()

    def register(self):
        return self.obj.register(self._name())

    def getMails(self):
        return self.obj.getMails()

    def getContent(self, mail):
        return self.obj.getContent(mail)

    def _baseN(self, num, b):
        return ((num == 0) and "0") or (self._baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])

    def _name(self):
        self.m5.update(str(time.time()).encode('utf-8'))
        s = self._baseN(int(self.m5.hexdigest(), 16), 36)
        return s[0:8]


class _Bccto(object):

    def __init__(self, proxy, timeout):
        super(_Bccto, self).__init__()
        self.proxy = proxy
        self.timeout = timeout
        self.session = None
        self.back = '@bccto.me'
        self.time = ''
        self.name = ''
        self.checkTime = 0

    def register(self, name):
        if self.session is not None:
            self.destoy()
        url = "http://www.bccto.me"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWekit/537.36 (KHTML,\
            like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        self.session = requests.session()
        try:
            r = self.session.get(url, headers=headers, timeout=self.timeout, proxies=self.proxy)
        except:
            print("http://www.bccto.me 连接失败")
            return False
        url = "http://www.bccto.me/applymail"
        data = "mail=%s%s" % (name, self.back)
        headers["Cookie"] = 'mail=%s;' % self.session.cookies['mail']
        headers["Origin"] = "http://www.bccto.me"
        headers["Host"] = "www.bccto.me"
        headers["Referer"] = "http://www.bccto.me/"
        headers["X-Requested-With"] = "XMLHttpRequest"
        try:
            r = self.session.post(url, data=data, headers=headers, timeout=self.timeout, proxies=self.proxy)
            a = json.loads(r.text)
            if a['success'] == 'true':
                self.time = a['time']
                self.name = name
                self.checkTime = 0
                return "%s%s" % (name, self.back)
            else:
                print("%s" % a['message'])
                return False
        except:
            print("http://www.bccto.me/applymail 申请失败")
            return False
        return False

    def getMails(self):
        url = "http://www.bccto.me/getmail"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cache-Control': 'max-age=0',
            'Cookie': 'mail=%s;' % self.session.cookies['mail'],
            'Host': 'www.bccto.me',
            'Origin': 'http://www.bccto.me',
            'Referer': 'http://www.bccto.me/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWekit/537.36 (KHTML,\
            like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        data = "mail=%s%s&time=%s&_=%s" % (self.name, self.back, self.checkTime, int(time.time() * 1000))
        try:
            r = self.session.post(url, data=data, headers=headers, timeout=self.timeout, proxies=self.proxy)
            d = json.loads(r.text)
            return d['mail']
        except Exception as e:
            print(e)
            return []

    def getContent(self, mail):
        if len(mail) < 5:
            print('MAIL 格式不正确')
            return ""
        m = '%s%s' % (self.name, self.back)
        m = m.replace('@', '(a)').replace('.', '-_-')
        url = "http://www.bccto.me/win/%s/%s" % (m, mail[4])
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWekit/537.36 (KHTML,\
            like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        try:
            r = self.session.get(url, headers=headers, timeout=self.timeout, proxies=self.proxy)
            soup = BeautifulSoup(r.text, 'html.parser')
            s = ''
            for d in soup.select('div'):
                s += '%s\n' % d.text
            return s
        except Exception as e:
            print(e)
            return None

    def destoy(self):
        try:
            self.session.close()
        except:
            pass
        self.session = None
