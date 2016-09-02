#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import scrapy
import datetime
import json
import html


class WechatSpider(scrapy.Spider):
    name = "WechatSpider"
    allowed_domains = ["qq.com"]
    article_infos = {}
    '''
    The settings attribute is set in the base Spider class after the spider is initialized.
    If you want to use the settings before the initialization (e.g., in your spider’s __init__() method),
    you’ll need to override the from_crawler() method.
    Maybe we can override it to get settings from database
    '''

    def __init__(self, accountlist_settings):
        self.start_urls = map(lambda x: "http://weixin.sogou.com/weixin?type=1&query=" + x, accountlist_settings)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get('ACCOUNT_LIST'))

    def parse(self, response):
        for href in response.xpath('//div[@id="sogou_vr_11002301_box_0"]/@href'):
            account_url = response.urljoin(href.extract())
            ## self.my_print(account_url)
            ## yield scrapy.Request(account_url, callback=self.parse_print2html)
            yield scrapy.Request(account_url, callback=self.parse_account)

    def parse_account(self, response):
        nickname = response.xpath('//div/strong[contains(@class, "profile_nickname")]/text()')[0].extract().strip()
        account = response.xpath('//div/p[contains(@class, "profile_account")]/text()')[0].extract().strip()
        print(nickname)
        print(account)
        msgJson = response.xpath('/html/body/script[4]/text()')[0].re(r'var msgList = \'(.*)\'')[0]
        articles = json.loads(msgJson)['list']
        for article in articles:
            appinfo = article['app_msg_ext_info']
            cominfo = article['comm_msg_info']
            url = "http://mp.weixin.qq.com/s?" + html.unescape(html.unescape(appinfo['content_url'][4:]))
            print(url.strip())

    def my_print(self, str):
        filename = 'output/start_urls' + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.txt'
        with open(filename, 'a') as f:
            f.write(str + '\n')
        f.close()

    def parse_print2html(self, response):
        filename = 'output/account_url' + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        f.close()
