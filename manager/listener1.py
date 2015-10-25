import time
import pymongo
import threading

time_gap = 5
lock = threading.Lock()
outfile_dir = 'log_new'

def write_to_file(content):
    lock.acquire()
    print content
    outfile = open(outfile_dir, 'a+')
    outfile.write(content.encode('UTF-8') + '\n')
    outfile.close()
    lock.release()

def main():
    client = pymongo.MongoClient('localhost:27018', replicaset='foo0')
    oplog = client.local.oplog.rs
    first = oplog.find().sort('$natural', pymongo.DESCENDING).limit(-1).next()
    ts = first['ts']
    while True:
        cursor = oplog.find({'ts': {'$gt': ts}}, tailable=True, await_data=True)
        cursor.add_option(8)
        while cursor.alive:
            for doc in cursor:
                ts = doc['ts']
                if doc['op'] == 'i':
                    if 'title' in doc['o'] and 'size' in doc['o'] and 'price' in doc['o']:
                        doc = doc['o']
                        ss = doc['size']
                        if doc['is_new'] == True:
                            if ss == '265' or ss == '270': 
                                time_str = doc['post_time'].strftime("%m-%d %H:%M")
                                content = str(doc['size']) + '\t' + str(doc['price']) + '\t' + doc['title'] + '\n' + time_str + '\t' + doc['url'] + '\n' 
                                write_to_file(content)
            time.sleep(time_gap)

if __name__ == '__main__':
    main()
