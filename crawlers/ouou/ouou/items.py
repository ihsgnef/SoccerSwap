import scrapy
from scrapy.item import Item, Field

class OuouItem(scrapy.Item):
    source      = Field()
    title       = Field()
    url         = Field()
    tid         = Field()
    uname       = Field()
    # images      = Field()
    # description = Field()
    size        = Field()
    price       = Field()
    stud        = Field()
    brand       = Field()
    series      = Field()
    is_new      = Field()
    post_time   = Field()
