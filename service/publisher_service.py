
import logging
import os
import pika

from pika.exchange_type import ExchangeType
from pika.exceptions import AMQPError


class PublishService:
    """
    Service for publishing messages to a RabbitMQ server.
    """
    def __init__(self, host=None, exchange_name='iot_exchange', exchange_type=ExchangeType.fanout):
        self.host = host or os.getenv('RABBITMQ_HOST', 'rabbit-server')
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.connection_parameters = pika.ConnectionParameters(self.host)

    def publish_to_queue(self, message):
        """
        Publishes a message to the specified RabbitMQ exchange.
        """
        try:
            logging.info(f"Establishing connection to RabbitMQ server at {self.host}")
            with pika.BlockingConnection(self.connection_parameters) as connection:
                channel = connection.channel()
                logging.info(f"Declaring exchange '{self.exchange_name}' of type '{self.exchange_type}'")
                channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type)

                logging.info(f"Publishing message: {message}")
                channel.basic_publish(exchange=self.exchange_name, routing_key='', body=message.encode())
                logging.info("Message published successfully")
        except AMQPError as e:
            logging.error(f"Error in RabbitMQ operation: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise
