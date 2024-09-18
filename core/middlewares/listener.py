import pika
import time
from core.env import config
import json
from .reducers import *
 
# Connect to RabbitMQ
credentials = pika.PlainCredentials(config.RABBIT_MQ_USER, config.RABBITMQ_DEFAULT_PASS)
parameters = pika.ConnectionParameters(config.RABBITMQ_HOSTNAME,
                                    config.RABBITMQ_PORT,
                                    'ashvdjpb',
                                    credentials,
                                    heartbeat=600)
connection = pika.BlockingConnection(parameters=parameters) # add container name in docker



class ListeningClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(parameters=parameters)
            self.channel = self.connection.channel()

            # Declare the queues
            self.channel.queue_declare(queue='B_to_A')
            
        except Exception as e:
            print(f"Connection error: {e}")
            time.sleep(5)  # Wait before retrying
            self.connect()  # Retry connection

    def start_consuming(self):
        def callback(ch, method, properties, body):
            print(body)
            print(json.loads(body))
            
            # body = json.loads(body)
            # match body['service']:
            #     case "users":
            #         act_on_users(body['action'], body['payload'], body['id'])
                
            #     case "transactions":
            #         act_on_transactions(body['action'], body['payload'], body['id'])
                
            #     case "books":
            #         act_on_books(body['action'], body['payload'], body['id'])
                    
            
            print(f"Received message from B: {body.decode()}")

        try:
            self.channel.basic_consume(
                queue='B_to_A',
                on_message_callback=callback,
                auto_ack=True
            )
            print(" [*] Waiting for messages from B. To exit press CTRL+C")
            self.channel.start_consuming()
            
        except pika.exceptions.AMQPConnectionError:
            print("Connection lost, reconnecting...")
            self.connect()  # Reconnect
            self.start_consuming()  # Restart consuming
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.connect()  # Reconnect
            self.start_consuming()  # Restart consuming


    def close(self):
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()

client = ListeningClient()