import os
import pika
import json


class RabbitMQMessager():

    def __init__(self, host, port, username, password, vhost):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.vhost = vhost


    def _get_conn(self):
        credentials = pika.PlainCredentials(self.username, 
                                            self.password
                                            )

        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host, 
                                                                        self.port, 
                                                                        self.vhost, 
                                                                        credentials))
        channel = connection.channel()

        return channel


    def send_message(self, exchange, routing_key, payload, json_format=True):
        chanel = self._get_conn()

        try:
            if json_format:
                chanel.basic_publish(exchange=exchange,
                                    routing_key=routing_key,
                                    body=json.dumps(payload))
            else:
                chanel.basic_publish(exchange=exchange,
                                    routing_key=routing_key,
                                    body=payload)
        except : Exception

        chanel.close()
        return True

