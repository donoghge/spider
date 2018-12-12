# -*- coding: utf-8 -*-
import json
import random
import re
import string

import scrapy
from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from xpc.items import PostItem, CopyrightItem, CommentItem, ComposerItem

cookies = dict(
    Authorization='A37AB29030DC8844A30DC843CB30DC8B2D630DC861E78138BA33'
)


def convert_int(s):
    if isinstance(s, str):
        return int(s.replace(',',''))
    return 0


def strip(s):
    if s:
        return s.strip()
    return ''


def gen_sessionid():
    return ''.join(random.choice(string.ascii_lowercase + string.digits,k=26))


class DiscoverySpider(scrapy.Spider):

    name = 'discovery'
    allowed_domains = ['xinpianchang.com','openapi-vtom.vmovier.com']
    start_urls = ['https://www.xinpianchang.com/channel/index/sort-like?from=tabArticle']
    page_count = 0

    #
    #
    def parse(self, response):
        # 设置PHPSESSID， 当页面超过100行时，改变cookie值
        self.page_count += 1
        if self.page_count >=100:
            cookies.update(PHPSESSID=gen_sessionid())
            page_count = 0


        # 跳转某一电影的url
        url = "https://www.xinpianchang.com/a%s?from=ArticleList"
        # 先找到所有的pid
        post_list = response.xpath(
            '//ul[@class="video-list"]/li')

        for post in post_list:
            # 找到pid 进入某一个电影页面
            # .get()和.extract_first()一样
            pid = post.xpath('./@data-articleid').get()
            request = response.follow(url % pid, self.parse_post)

            request.meta['pid'] = pid
            request.meta['thumbnail'] = post.xpath('./a/img/@_src').get()
            yield request

        # 处理下一页数据， 超过20page需要携带cookies
        pages = response.xpath('//div[@class="page"]//a/@href').extract()
        for page in pages:
            yield response.follow(page, self.parse, cookies=cookies)

    #
    # 获取电影信息，但是电影视频等需要parse_video处理
    def parse_post(self, response):

        pid = response.meta['pid']
        post = PostItem(pid=pid)

        post['thumbnail'] = response.meta['thumbnail']
        post['title'] = response.xpath('//div[@class="title-wrap"]/h3/text()').get()

        # 获取电影视频vid， Json url，
        vid, = re.findall('vid: \"(\w+)\"\,', response.text)
        video_url = 'https://openapi-vtom.vmovier.com/v3/video/%s?expand=resource,resource_origin?'

        # 类型
        cates = response.xpath('//div//span[contains(@class, "cate")]//text()').extract()
        post['category'] = ''.join([cate.strip() for cate in cates])
        # 发表时间
        post['created_at'] = response.xpath('//div//span[contains(@class, "update-time")]/i/text()').get()
        post['play_counts'] = convert_int(response.xpath('//div//i[contains(@class, "play-counts")]/text()').get())
        post['like_counts'] = convert_int(response.xpath('//div//span[contains(@class, "like-counts")]/@data-counts').get())
        post['description'] = response.xpath('//div//p[contains(@class, "desc")]//text()').get()

        #
        request = Request(video_url % vid, callback=self.parse_video)
        request.meta['post'] = post
        yield request

        # 评论也是动态加载，处理评论部分
        comment_url = 'http://www.xinpianchang.com/article/filmplay/ts-getCommentApi?id=%s&page=1'
        request = Request(comment_url % pid, callback=self.parse_comment)
        request.meta['pid'] = pid
        yield request

        # 获取本片创作者
        creator_list = response.xpath('//div[@class="user-team"]//ul[@class="creator-list"]/li')
        composer_url = 'https://www.xinpianchang.com/u%s?from=articleList'
        # 迭代每个作者
        for creator in creator_list:
            cid = creator.xpath('./a/@data-userid').get()

            request = Request(composer_url % cid, self.parse_composer)
            request.meta['cid'] = cid
            request.meta['dont_merge_cookies'] = True
            yield request

            # 把每个作者与该作品的关系存储表
            cr = CopyrightItem()
            cr['pcid'] = "%s_%s" % (pid,cid)
            cr['pid'] = pid
            cr['cid'] = cid
            cr['roles'] = creator.xpath('./div[@class="creator-info"]/span/text()').get()
            yield cr

    #
    # 处理电影视频信息
    def parse_video(self, response):

        post = response.meta['post']

        result = json.loads(response.text)

        data = result['data']
        if 'resource' in data:
            post['video'] = data['resource']['default']['url']
        else:
            d = data['third']['data']
            post['video'] = d.get('iframe_url', d.get('swf', ''))

        post['preview'] = data['video']['cover']

        post['duration'] = data['video']['duration']
        yield post

    #
    # 处理评论信息
    def parse_comment(self, response):
        result = json.loads(response.text)

        for c in result['data']['list']:
            comment = CommentItem()
            comment['uname'] = c['userInfo']['username']
            comment['avatar'] = c['userInfo']['face']
            comment['cid'] = c['userInfo']['userid']
            comment['commentid'] = c['commentid']
            comment['pid'] = c['articleid']
            comment['created_at'] = c['addtime_int']
            comment['like_counts'] = c['count_approve']
            comment['content'] = c['content']
            if c['reply']:
                comment['reply'] = c['reply']['commentid'] or 0
            yield comment
        # 分页
        next_page = result['data']['next_page_url']
        if next_page:
            yield response.follow(next_page, self.parse_comment)

    #
    # 搜索每个创作者的具体信息
    def parse_composer(self, response):

        composer = ComposerItem()
        composer['cid'] = response.meta['cid']

        banner = response.xpath('//div[@class="banner-wrap"]/@style').get()
        composer['banner'] = re.findall('background-image:url\((.+?)\)',banner)

        composer['avatar'] = response.xpath('//span[@class="avator-wrap-s"]/'
                                            'img/@src').get()
        composer['name'] = response.xpath('//p[contains(@class, "creator-name")]/'
                                          'text()').get()
        composer['intro'] = response.xpath('//p[contains(@class, "creator-desc")]/'
                                           'text()').get()
        composer['like_counts'] = convert_int(response.xpath('//span[contains(@class,"like-counts")]/'
                                                 'text()').get())
        composer['fans_counts'] = convert_int(response.xpath('//span[contains(@class,"fans-counts")]/'
                                                 'text()').get())
        composer['follow_counts'] = convert_int(response.xpath('//span[contains(@class, "follow-wrap")]/'
                                                   'span[last()]/text()').get())
        composer['location'] = response.xpath('//span[contains(@class, "icon-location")]/'
                                              'following-sibling::span[1]/text()').get() or ""
        composer['career'] = response.xpath('//span[contains(@class, "icon-career")]/'
                                            'following-sibling::span[1]/text()').get() or ""
        yield composer
