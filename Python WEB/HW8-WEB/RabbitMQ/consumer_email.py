import pika

from src.models import Users
import src.connect


CREDENTIAL_LOGIN = "guest"
CREDENTIAL_PASSWORD = "guest"

credentials = pika.PlainCredentials(CREDENTIAL_LOGIN, CREDENTIAL_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
email_channel = connection.channel()

email_channel.queue_declare(queue='email_queue', durable=True)


def callback(ch, method, properties, body):
    message = body.decode()
    user = Users.objects(id = message)
    user.update(email_mailed = True)
    ch.basic_ack(delivery_tag=method.delivery_tag)


email_channel.basic_qos(prefetch_count=1)
email_channel.basic_consume(queue='email_queue', on_message_callback=callback)


if __name__ == '__main__':
    email_channel.start_consuming()
    email_channel.close()