import sys
sys.path.append('..')
import requests
from Proxy import Proxy
from bs4 import BeautifulSoup
p = Proxy()
url = 'http://www.baidu.com/s?wd=ip'

for i in range(10):
    proxies = p.IP()
    print(proxies)
    r = requests.get(url, timeout=60, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(soup.select("#content_left > #1 > div > div > div > table > tr > td > span")[0].text)


for i in range(10):
    proxies = p.IP(_type=1)
    print(proxies)
    r = requests.get(url, timeout=60, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(soup.select("#content_left > #1 > div > div > div > table > tr > td > span")[0].text)
