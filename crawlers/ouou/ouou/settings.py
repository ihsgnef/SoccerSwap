# Scrapy settings for ouou project

BOT_NAME = 'ouou'

SPIDER_MODULES = ['ouou.spiders']
NEWSPIDER_MODULE = 'ouou.spiders'

ITEM_PIPELINES = ['ouou.pipelines.MongoDBPipeline']

MONGODB_SERVER = "localhost"
MONGODB_REPLICASET = 'foo0'
MONGODB_PORT = 27018
MONGODB_DB = "forum"
MONGODB_COLLECTION = "threads"
MONGODB_UNIQUE_KEY = 'url'
