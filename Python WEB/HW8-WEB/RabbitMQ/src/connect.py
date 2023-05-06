import configparser

from mongoengine import connect


config = configparser.ConfigParser()
config.read('RabbitMQ\config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')


host = f'mongodb+srv://{mongo_user}:{mongodb_pass}@{db_name}.{domain}.mongodb.net/?retryWrites=true&w=majority'
connect(host = host, ssl = True)