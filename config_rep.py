from pymongo import MongoClient

port = 27018
name = 'foo0'

c = MongoClient('localhost', port)
config = {'_id': name, 'members': [
    {'_id': 0, 'host': 'localhost:' + str(port)}]}
c.admin.command("replSetInitiate", config)
