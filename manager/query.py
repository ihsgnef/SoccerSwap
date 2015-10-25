import pymongo

def get_options(line):
    line = line.strip()
    category = line.split(':')[0]
    right = line.split(':')[1]
    options = None
    if len(right) > 0:
        options = right.split(',')
    return category, options

def condition_to_query(query_file):
    # source, size, price, stud, brand, series, is_new
    and_query = []
    for line in query_file:
        or_query = []
        category, options = get_options(line)
        if options is not None:
            for option in options:
                or_query.append({category:option})
            and_query.append({"$or":or_query})
    return {"$and":and_query}

def main():
    client = pymongo.MongoClient('localhost:27018', replicaset='foo0')
    db = client.forum
    and_query = condition_to_query(open('test_query').readlines())
    print and_query
    cursor = db.threads.find(and_query)
    for document in cursor:
        print document['title']
        print document['url']
        print ''

if __name__ == '__main__':
    main()
