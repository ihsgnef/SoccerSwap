# Scrapy settings for ouou project

BOT_NAME = 'ouou'

SPIDER_MODULES = ['ouou.spiders']
NEWSPIDER_MODULE = 'ouou.spiders'

ITEM_PIPELINES = ['ouou.pipelines.MongoDBPipeline']

MONGODB_SERVER = "localhost"
MONGODB_REPLICASET = 'foo'
MONGODB_PORT = 27017
MONGODB_DB = "ouou"
MONGODB_COLLECTION = "threads"
MONGODB_UNIQUE_KEY = 'tid'
