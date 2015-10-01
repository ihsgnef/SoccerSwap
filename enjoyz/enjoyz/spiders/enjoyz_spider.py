import scrapy
from scrapy import Spider
from scrapy.selector import Selector

from enjoyz.items import EnjoyzItem 

class EnjoyzSpider(Spider):
    name = 'enjoyz'
    allowed_domains = ['enjoyz.com']
    start_urls = ['http://bbs.enjoyz.com/forum.php?mod=forumdisplay&fid=15&filter=sortid&sortid=1&typeid=149']

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

        description = ''
        descriptions = Selector(response).xpath('//td[@class="t_f"]').extract()
        for des in descriptions:
            if des.startswith('<'):
                print '*****************', des, '==============='
                if des.startswith('<font') and not des.startswith(
                        '<font class="jammer"'):
                    print ''
            else:
                description += '\n' + des
        item['description'] = description

        yield item
