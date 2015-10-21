# -*- coding: utf-8 -*-

import scrapy
from scrapy import Spider
from scrapy.selector import Selector

from enjoyz.items import EnjoyzItem 

class EnjoyzSpider(Spider):
    name = 'enjoyz'
    allowed_domains = ['enjoyz.com']
    start_urls = ['http://bbs.enjoyz.com/forum.php?mod=forumdisplay&fid=15&sortid=1&typeid=149&filter=sortid&sortid=1&typeid=149&page=%s' % page for page in xrange(1, 20)]

    def parse(self, response):
        threads = Selector(response).xpath('//th[@class="new s_ltitle"]')
        for thread in threads:
            url = response.urljoin(thread.xpath('a[@class="s xst"]/@href').extract()[0])
            yield scrapy.Request(url, callback=self.parse_thread_contents)

    def parse_thread_contents(self, response):
        item = EnjoyzItem()
        
        item['title'] = Selector(response).xpath(
                '//h1[@class="ts"]/span[@id="thread_subject"]/text()').extract()[0]

        url = Selector(response).xpath('//span[@class="xg1"]/a/@href').extract()[0]
        item['url'] = response.urljoin(url)

        values = Selector(response).xpath('//table[@class="cgtl mbm"]//td/text()').extract()
        item['price'] = int(values[1].split(' ')[0])
        item['size'] = values[2][:-1]
        item['stud'] = values[3][:-1]
        item['is_new'] = True if values[4][:-1].startswith('\xe5\x85\xa8\xe6\x96\xb0'.decode('utf-8')) else False
        brand_series = values[0]
        # puma » 其他 
        item['brand'] = brand_series.split(' ')[0]
        item['series'] = brand_series.split(' ')[-2]

        yield item
