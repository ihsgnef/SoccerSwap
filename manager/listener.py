import os
import time
import pymongo
import threading
from conditions import get_conds

time_gap = 5
lock = threading.Lock()
outfile_dir = 'log'

def write_to_file(content):
    lock.acquire()
    # print content
    outfile = open(outfile_dir, 'a+')
    outfile.write(content.encode('UTF-8') + '\n')
    outfile.close()
    lock.release()

def check_conds(doc, conds):
    # doc and conds are two dicts
    # check if all requirements in conds are met in doc
    # conds: key, [values]
    met = True
    for key in conds:
        values = conds[key]
        if key not in doc or doc[key] not in values:
            met = False
            break
    return met

def check_any_conds(doc, conds_set):
    # check if doc met and cond in conds_set
    met = None
    for name in conds_set:
        cond = conds_set[name]
        if check_conds(doc, cond):
            met = name
            break
    return met

def main():
    client = pymongo.MongoClient('localhost:27018', replicaset='foo0')
    oplog = client.local.oplog.rs
    first = oplog.find().sort('$natural', pymongo.DESCENDING).limit(-1).next()
    ts = first['ts']
    conds_set = get_conds()
    _cmd = 'terminal-notifier -message {} -title {} -open {} -sound default'

    while True:
        cursor = oplog.find({'ts': {'$gt': ts}}, tailable=True, await_data=True)
        cursor.add_option(8)
        while cursor.alive:
            for doc in cursor:
                ts = doc['ts']
                if doc['op'] == 'i':
                    doc = doc['o']
                    if 'title' in doc and 'size' in doc and 'price' in doc:
                        met = check_any_conds(doc, conds_set)
                        if met is not None:
                            time_str = doc['post_time'].strftime("%m-%d %H:%M")
                            content = str(doc['size']) + '\t' + str(doc['price']) + '\t' + doc['title'] + '\n' + time_str + '\n' + doc['url'] + '\n' 
                            write_to_file(content)

                            cmd = _cmd.format(doc['title'].encode('utf-8'), met + ' ' + str(doc['price']), doc['url'])
                            os.system(cmd)
                            print met

            time.sleep(time_gap)

if __name__ == '__main__':
    main()
