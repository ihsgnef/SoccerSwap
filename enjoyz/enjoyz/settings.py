# Scrapy settings for enjoyz project

BOT_NAME = 'enjoyz'

SPIDER_MODULES = ['enjoyz.spiders']
NEWSPIDER_MODULE = 'enjoyz.spiders'

ITEM_PIPELINES = ['enjoyz.pipelines.MongoDBPipeline',]

MONGODB_SERVER = "localhost"
MONGODB_REPLICASET = 'foo0'
MONGODB_PORT = 27018
MONGODB_DB = "enjoyz"
MONGODB_COLLECTION = "threads"
MONGODB_UNIQUE_KEY = 'url'
