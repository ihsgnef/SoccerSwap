# Define your item pipelines here

import pymongo
from pymongo import errors

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

from ouou.items import OuouItem

class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], 
                                         settings['MONGODB_PORT'],
                                         replicaset=settings['MONGODB_REPLICASET'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.collection.ensure_index(settings['MONGODB_UNIQUE_KEY'], unique=True)
        self.stop_on_duplicate = 0

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}".format(data))

        if valid:
            try:
                self.collection.insert(dict(item))
                log.msg("Thread added to MongoDB", 
                        level=log.DEBUG, spider=spider)
            except errors.DuplicateKeyError:
                log.msg(u'Duplicate key found', 
                        level=log.DEBUG, spider=spider)
                pass

        return item

if __name__ == '__main__':
    pipeline = MongoDBPipeline()
