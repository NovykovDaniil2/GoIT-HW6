from queue import Queue
from random import choice
from concurrent.futures import ThreadPoolExecutor
import asyncio

from faker import Faker

from src.models import Users
import src.connect

MAIL_TYPES = ['sms', 'email']
USER_COUNT = 1000

Fake = Faker()


def create_user(queue: Queue) -> None:
    user_data = {'fullname' : Fake.name(),
                 'profession' : Fake.job(),
                 'phone' : Fake.phone_number(),
                 'email' : Fake.email(),
                 'mailing_prefer' : choice(MAIL_TYPES)}
    queue.put(user_data)
    

def add_user(queue: Queue) -> None:
    user_data = queue.get()
    user = Users(fullname = user_data['fullname'],
                 profession = user_data['profession'],
                 phone = user_data['phone'],
                 email = user_data['email'],
                 mailing_prefer = user_data['mailing_prefer'])
    user.save()

async def main() -> str:
    queue = Queue()
    for _ in range(USER_COUNT):
        create_user(queue)
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(30) as pool:
        futures = [loop.run_in_executor(pool, add_user, queue) for _ in range(queue.qsize())]
    
    return f'\033[32m{USER_COUNT} users was added to database\033[0m'

    

 
if __name__ == '__main__':
    print(asyncio.run(main()))