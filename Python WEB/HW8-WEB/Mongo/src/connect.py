import configparser

from mongoengine import connect
from pymongo import MongoClient
from pymongo.server_api import ServerApi


config = configparser.ConfigParser()
config.read('mongo/config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')


host = f'mongodb+srv://{mongo_user}:{mongodb_pass}@{db_name}.tiky1rr.mongodb.net/?retryWrites=true&w=majority'
connect(host = host, ssl = True)
client = MongoClient(host, server_api=ServerApi('1'))