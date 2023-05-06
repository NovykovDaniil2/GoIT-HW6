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

sms_channel.queue_declare(queue='sms_queue', durable=True)


def callback(ch, method, properties, body):
    message = body.decode()
    user = Users.objects(id = message)
    user.update(sms_mailed = True)
    ch.basic_ack(delivery_tag=method.delivery_tag)


sms_channel.basic_qos(prefetch_count=1)
sms_channel.basic_consume(queue='sms_queue', on_message_callback=callback)


if __name__ == '__main__':
    sms_channel.start_consuming()
    sms_channel.close()