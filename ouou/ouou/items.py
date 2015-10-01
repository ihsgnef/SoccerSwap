# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class OuouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title       = Field()
    url         = Field()
    tid         = Field()
    uname       = Field()
    description = Field()
    images      = Field()
    size        = Field()
    price       = Field()
    stud        = Field()
    brand       = Field()
    series      = Field()
    is_new      = Field()
    post_time   = Field()
