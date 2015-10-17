import time
import pymongo

c = pymongo.MongoClient()

oplog = c.local.oplog.rs
first = oplog.find().sort('$natural', pymongo.DESCENDING).limit(-1).next()
ts = first['ts']

while True:
    cursor = oplog.find({'ts': {'$gt': ts}}, tailable=True, await_data=True)
    cursor.add_option(8)
    while cursor.alive:
        for doc in cursor:
            ts = doc['ts']
            if doc['op'] == 'i':
                if 'title' in doc['o']:
                    print doc['o']['title']
        time.sleep(1)
