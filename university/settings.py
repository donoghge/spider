# -*- coding: utf-8 -*-

# Scrapy settings for ScripMiddleware project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ScripMiddleware'

SPIDER_MODULES = ['ScripMiddleware.spiders']
NEWSPIDER_MODULE = 'ScripMiddleware.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ScripMiddleware (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

PROXIES = [
    'http://iguye.com:41801',
    'http://118.89.190.86:41801',
    'http://39.108.2.231:41801',
    'http://www.sanshi.wang:41801',
    'http://www.fand.wang:65530',
    'http://www.wuyan.ga:20950',
    'http://www.donogh.cn:41801',
    'http://39.107.98.243:41801',
    'http://47.106.138.135:41801',
    'http://lixiugang.top:44444',
    'http://www.haodong.site:9248',
    'http://39.107.93.17:41801',
    'http://47.93.233.29:36831',
    'http://www.tencenting.com:65535',
    'http://theodore.org.cn:41801',
    'http://123.56.2.87:41801',
    'http://39.106.170.255:19624',
    'http://66.98.115.200:43325',
    'http://39.105.30.223:41801',
    'http://xiaoxianmei.top:41801',
    'http://39.105.16.122:41801',
    'http://101.200.52.97:55555',
    'http://60.205.179.2:41801',
    'http://yyywww.work:41801',
    'http://60.205.221.7:41801',
    'http://47.93.27.210:65219',
    'http://39.107.86.198:41801',
    'http://101.200.36.102:41801',
    'http://39.107.232.43:41801',
    'http://39.107.113.31:7777',
    'http://60.205.179.2:41801',
    'http://39.105.15.5:41801',
    'http://47.94.194.18:41081',
    'http://www.feifan.ren:41801',

    'http://39.107.74.86:41801',
    #失败的代理
    'http://39.107.101.28:41801',
    'http://101.201.237.180:41801',
    'http://39.106.141.156:54188',
    'http://59.110.172.189:41801',
    'http://39.105.28.37:9527',
    'http://47.94.135.50:41801',
    'http://101.201.234.106:41801'

]

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ScripMiddleware.middlewares.ScripmiddlewareSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'ScripMiddleware.middlewares.ScripmiddlewareDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
   'scrapy.extensions.telnet.TelnetConsole': None,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'ScripMiddleware.pipelines.ScripmiddlewarePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
