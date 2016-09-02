#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy

class ShareditorSpider(scrapy.Spider):
    name = "dashujuwenzhai"
    allowed_domains = ["qq.com"]
    start_urls = [
        "http://weixin.sogou.com/weixin?query=大数据文摘"
    ]

    def parse(self, response):
        href = response.selector.xpath('//div[@id="sogou_vr_11002301_box_0"]/@href').extract()[0]
        yield scrapy.Request(href, callback=self.parse_profile)

    def parse_profile(self, response):
        filename = 'dashujuwenzhai.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        f.close()
