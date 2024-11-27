from django.conf import settings
import pika



class RabbitMQ:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RabbitMQ, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RMQ_HOST,
                port=settings.RMQ_PORT,
                credentials=pika.PlainCredentials(
                    username=settings.RMQ_USER,
                    password=settings.RMQ_PASSWORD,
                ),
                heartbeat=600,
                blocked_connection_timeout=300
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(settings.TASK_QUEUE)

    def publish(self, body):
        self.channel.basic_publish(
            exchange=settings.EXCHANGE,
            routing_key=settings.ROUTING_KEY,
            body=body,
        )


publisher = RabbitMQ()