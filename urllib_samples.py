import urllib.request
import json
"""
# 接受path为参数
r = urllib.request.urlopen('http://httpbin.org/get')
text = r.read()


# 返回的内容是json格式，直接用load函数加载
print(json.loads(text))
# 返回状态码和msg
print(text)
print(r.status, r.reason)
r.close()


# r.headers是一个HTTPMessage对象
# print(r.headers)
for k, v in r.headers._headers:
    print("%s: %s" % (k, v))


ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) ' \
     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77' \
     ' Safari/537.36'
# 添加自定义的头信息
req = urllib.request.Request('http://httpbin.org/user-agent')
req.add_header('User-Agent', ua)

# 接收一个urllib.request.Request对象作为参数
r = urllib.request.urlopen(req)
resp = json.load(r)
# 打印出httpbin网站返回信息里的user-agent
print('user-agent:', resp["user-agent"])
"""


# uri去除域名的部分
# 发起带basic auth的请求
auth_handler = urllib.request.HTTPBasicAuthHandler()
auth_handler.add_password(realm='httpbin auth',
                          uri='/basic-auth/guye/123456',
                          user='guye',
                          passwd='123456')
opener = urllib.request.build_opener(auth_handler)
urllib.request.install_opener(opener)
r = urllib.request.urlopen('http://httpbin.org')
print(r.read.decode('utf-8'))


# 使用GET参数
# params = urllib.parse.urlencode({'spam': 1, 'egsg':2})
# url = 'http://httpbin.org/get?%s' %params
# with urllib.request.urlopen(url) as f:
#     print(json.load(f))

# 使用POST参数
# data = urllib.parse.urlencode({'name': 'xiaoming', 'age':2})
# data = data.encode()
# with urllib.request.urlopen('http://httpbin.org/post',data) as f:
#     print(json.load(f))


# ip代理
# proxy_handler = urllib.request.ProxyHandler({'http':'http://iguye.com:41801'})

# 带用户名密码
# proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()

# opener = urllib.request.build_opener(proxy_handler)
# r = opener.open('http://httpbin.org/ip')
# print(r.read)


# urlparse模块
# o = urllib.parse.urlparse('http://httpbin.org/get')


# from urllib.request import urlopen
#
# urlopen('http://httpbin.org/get')
