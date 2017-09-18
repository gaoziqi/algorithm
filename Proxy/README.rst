支持多线程的代理IP池
====================
使用示例：
 | pool = Proxy() 构造代理池类
 | pool = Proxy(min_pool=50) 设置池中最少ip数量，默认值5
 | pool = Proxy(timeout=80) 设置池内请求的最大延迟，默认值60
 | pool.IP() 获取透明代理IP
 | pool.IP(_type=1) 获取高匿代理IP，默认值0（透明）
 | pool.IP(url='xici') 获取代理IP网址，目前只支持xici

完成日期 2017.09.18
