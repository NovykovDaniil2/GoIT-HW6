from prettytable import PrettyTable
from redis_lru import RedisLRU
import redis

from src.connect import client

LOCALHOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = None

db = client.test

redis_client = redis.StrictRedis(host=LOCALHOST, port=REDIS_PORT, password=REDIS_PASSWORD)
cache = RedisLRU(redis_client)


def help_() -> str:
    return '''Work example: 
            \033[32mname: Steve Martin\033[0m - find and return a list of all quotes by author Steve Martin; 
            \033[32mtag: life\033[0m -find and return a list of quotes for the life tag; 
            \033[32mexit\033[0m-complete script execution;'''

@cache
def name(fullname: str) -> str(PrettyTable):
    authors = [(_id['fullname'], _id['_id']) for _id in db.authors.find({'fullname' : {'$regex' : fullname.strip()} })]
    table = PrettyTable(['Fullname', 'Quotes'])
    for author in authors:
        quotes = db.quotes.find({'author' : author[1]})
        for quote in quotes:
            table.add_row([author[0], quote['quote']])
    return str(table)

@cache      
def tag(tags: str) -> str(PrettyTable):
    tags = tags.replace(' ', '').split(',')
    if len(tags) == 1:
        tags = tags[0]
        quotes = db.quotes.find({'tags': {'$regex' : tags} })
    elif len(tags) > 1:
        quotes = db.quotes.find({'tags': {'$all' : tags} })
    table = PrettyTable(['Tags', 'Quotes'])
    for quote in quotes:
        matched_tags = ' '.join(quote['tags'])

        table.add_row([matched_tags, quote['quote']])
    return str(table)