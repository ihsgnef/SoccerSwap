import scrapy
from scrapy.item import Item, Field

class EnjoyzItem(scrapy.Item):
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
