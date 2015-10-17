import time
import pymongo

c = pymongo.MongoClient('localhost:27018', replicaset='foo0')

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
                if 'title' in doc['o'] and 'size' in doc['o']:
                    doc = doc['o']
                    if doc['size'] == 'JP280' or doc['size'] == 'JP275' or doc['size'] == 'JP285':
                        print doc['size'] + '\t', doc['title']
                        print '\t' + doc['url']
        time.sleep(1)
