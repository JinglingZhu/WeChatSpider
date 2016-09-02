#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.selector import Selector

class ShareditorSpider(scrapy.Spider):
    name = "liaoliaojiagou"
    allowed_domains = ["qq.com"]
    start_urls = [
        "http://weixin.sogou.com/weixin?type=1&query=聊聊架构"
    ]

    def parse(self, response):
        href = response.selector.xpath('//div[@id="sogou_vr_11002301_box_0"]/@href').extract()[0]

        ShareditorSpider.parse_profile('stdout', stdout)
        response = HtmlResponse(url=href, body=stdout)
        ShareditorSpider.parse_profile("response", response.body)

        for selector in Selector(response=response).xpath('//*[@id="history"]/div/div/div/div'):
            hrefs= selector.xpath('h4/@hrefs').extract()[0].strip()
            title = selector.xpath('h4/text()').extract()[0].strip()
            abstract = selector.xpath('//*[contains(@class, "weui_media_desc")]/text()').extract()[0].strip()
            pubtime = selector.xpath('//*[contains(@class, "weui_media_extra_info")]/text()').extract()[0].strip()

            print(hrefs)
            print(title)
            print(abstract)
            print(pubtime)

    def parse_profile(self, title, content):
        filename = title + '.txt'
        with open(filename, 'wb') as f:
            f.write(content)
        f.close()
