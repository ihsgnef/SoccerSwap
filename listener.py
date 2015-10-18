import time
import pymongo
import Queue
import threading

time_gap = 5
lock = threading.Lock()
outfile_dir = '/Users/fs/Downloads/soccerswap'

def write_to_file(content):
    lock.acquire()
    print content
    outfile = open(outfile_dir, 'a+')
    outfile.write(content.encode('UTF-8') + '\n')
    outfile.close()
    lock.release()

class listener(threading.Thread):
    def __init__(self, connection):
        super(listener, self).__init__()
        self.connection = connection

    def run(self):
        oplog = self.connection.local.oplog.rs
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
                            if doc['size'] == 'JP280' or doc['size'] == 'JP275' or doc['size'] == 'JP285':
                                content = doc['size'] + '\t' + str(doc['price']) + '\t' + doc['title'] + '\n\t\t' + doc['url'] 
                                write_to_file(content)
                time.sleep(time_gap)
    
def main():
    ouou = pymongo.MongoClient('localhost', replicaset='foo')
    ez = pymongo.MongoClient('localhost:27018', replicaset='foo0')
    t1 = listener(ouou)
    t2 = listener(ez)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
    main()
