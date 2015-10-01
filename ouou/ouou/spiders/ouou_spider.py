import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from datetime import datetime

from ouou.items import OuouItem

class OuouSpider(Spider):
    name = 'ouou'
    allowed_domains = ['ouou.cn']
    start_urls = ['http://bbs.ouou.cn/thread-htm-fid-6-type-233-modelid-9.html']
    # start_urls = ['http://bbs.ouou.cn/thread-htm-fid-6-type-233-modelid-9-page-%s.html' % page for page in xrange(1, 512)]

    def parse(self, response):
        threads = Selector(response).xpath('//td[@class="subject f14"]')
        for thread in threads:
            url = response.urljoin(thread.xpath('a[@class="f14"]/@href').extract()[0])
            yield scrapy.Request(url, callback=self.parse_thread_contents)

    def parse_thread_contents(self, response):
        item = OuouItem()
        item['title'] = Selector(response).xpath(
                '//h1[@id="subject_tpc"][@class="read_h1"]/text()').extract()[0]
        item['url'] = Selector(response).xpath(
                '//h1[@id="subject_tpc"][@class="read_h1"]/a[@href="javascript:;"]/@title').extract()[0]

        content_hdr = '//div[@class="tpc_content"]/div[@class="f14 mb10"][@id="read_tpc"]'

        description = Selector(response).xpath(content_hdr + '/text()').extract()
        description = '\n'.join(description)
        item['description'] = description
        
        content = Selector(response).xpath(content_hdr)
        _images = content.xpath('//img/@src').extract()
        images = []
        for image in _images:
            if image.startswith('http://bbsimg.ouou.cn/Mon_'):
                images.append(image.split('?')[0])
        item['images'] = images


        str_brand = u'\u54c1\u724c\u7cfb\u5217\uff1a'
        str_size = u'\u5c3a\u7801\uff1a'
        str_stud = u'\u978b\u9489\u7c7b\u578b\uff1a'
        str_isnew = u'\u6210\u8272\uff1a'
        str_price = u'\u4ef7\u683c\uff1a'

        # brand > series, size, stud, isnew, price
        cate_keys = Selector(response).xpath('//div[@class="cates"]').xpath(
                '//em/text()').extract()[4:]
        cate_values = Selector(response).xpath('//div[@class="cates"]').xpath(
                '//cite/text()').extract()
        cates = zip(cate_keys, cate_values)
        
        for key, value in cates:
            if key == str_brand:
                if '>' in value:
                    item['brand'] = value.split(' > ')[0]
                    item['series'] = value.split(' > ')[1]
                else:
                    item['brand'] = value
            if key == str_size:
                item['size'] = value
            if key == str_stud:
                item['stud'] = value
            if key == str_isnew:
                item['is_new'] = True if value == '\xe5\x85\xa8\xe6\x96\xb0'.decode('utf-8') else False
            if key == str_price:
                item['price'] = int(value)

        item['uname'] = Selector(response).xpath(
                '//div[@class="readName b"]/a/text()').extract()[0]

        
        time_str = Selector(response).xpath(
                '//div[@class="tipTop s6"]/span/@title').extract()[-1]
        item['post_time'] = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

        yield item
