# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from datetime import datetime

from enjoyz.items import EnjoyzItem 

model_dict = {
        "legend":"tiempo",
        }

class EnjoyzSpider(Spider):
    name = 'enjoyz'
    allowed_domains = ['enjoyz.com']
    start_urls = ['http://bbs.enjoyz.com/forum.php?mod=forumdisplay&fid=15&sortid=1&typeid=149&filter=sortid&sortid=1&typeid=149&page=%s' % page for page in xrange(1, 4)]

    def parse(self, response):
        threads = Selector(response).xpath('//th[@class="new s_ltitle"]')
        for thread in threads:
            url = response.urljoin(thread.xpath('a[@class="s xst"]/@href').extract()[0])
            yield scrapy.Request(url, callback=self.parse_thread_contents)

    def parse_thread_contents(self, response):
        item = EnjoyzItem()
        item['source'] = 'enjoyz'
        
        item['title'] = Selector(response).xpath(
                '//h1[@class="ts"]/span[@id="thread_subject"]/text()').extract()[0]

        url = Selector(response).xpath('//span[@class="xg1"]/a/@href').extract()[0]
        item['url'] = response.urljoin(url)

        values = Selector(response).xpath('//table[@class="cgtl mbm"]//td/text()').extract()
        item['price'] = int(values[1].split(' ')[0])
        item['size'] = int(values[2][2:-1])
        item['stud'] = values[3][:2]
        item['is_new'] = True if values[4][:-1].startswith('\xe5\x85\xa8\xe6\x96\xb0'.decode('utf-8')) else False
        brand_series = values[0]
        # puma » 其他 
        item['brand'] = brand_series.split(' ')[0].lower()
        series = brand_series.split(' ')[-2].lower()
        if series in model_dict:
            series = model_dict[series]
        item['series'] = series

        item['uname'] = Selector(response).xpath('//td[@class="pls"]//div[@class="pi"]//div[@class="authi"]/a/text()').extract()[0]
        time_str = Selector(response).xpath('//td[@class="plc"]//div[@class="pti"]//div[@class="authi"]/em/span/@title').extract()
        time_str = time_str[0]
        item['post_time'] = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

        yield item
