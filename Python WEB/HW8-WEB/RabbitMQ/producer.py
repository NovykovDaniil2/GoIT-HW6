from queue import Queue

import pika

from src.models import Users
import src.connect


CREDENTIAL_LOGIN = "guest"
CREDENTIAL_PASSWORD = "guest"

credentials = pika.PlainCredentials(CREDENTIAL_LOGIN, CREDENTIAL_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)


sms_channel = connection.channel()

sms_channel.exchange_declare(exchange="sms_mock", exchange_type="direct")
sms_channel.queue_declare(queue="sms_queue", durable=True)
sms_channel.queue_bind(exchange="sms_mock", queue="sms_queue")

email_channel = connection.channel()

email_channel.exchange_declare(exchange="email_mock", exchange_type="direct")
email_channel.queue_declare(queue="email_queue", durable=True)
email_channel.queue_bind(exchange="email_mock", queue="email_queue")


def create_queues() -> Queue:
    sms_queue = Queue()
    email_queue = Queue()
    for user in Users.objects:
        prefer = user.mailing_prefer
        if prefer == "sms":
            sms_queue.put(user.id)
        elif prefer == "email":
            email_queue.put(user.id)
    return sms_queue, email_queue


def spread_sms_task(sms_queue: Queue):
    sms_channel.basic_publish(
        exchange="sms_mock",
        routing_key="sms_queue",
        body=str(sms_queue.get()).encode(),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ),
    )


def spread_email_task(email_queue: Queue):
    email_channel.basic_publish(
        exchange="email_mock",
        routing_key="email_queue",
        body=str(email_queue.get()).encode(),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ),
    )


def main() -> str:
    sms_queue, email_queue = create_queues()
    sms_size, email_size = sms_queue.qsize(), email_queue.qsize()

    for _ in range(sms_size):
        spread_sms_task(sms_queue)

    for _ in range(email_size):
        spread_email_task(email_queue)

    connection.close()

    return f"\033[32mWas created {sms_size} SMS tasks and {email_size} EMAIL tasks\033[0m"


if __name__ == "__main__":
    print(main())
