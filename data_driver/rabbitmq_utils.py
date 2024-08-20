import pika
import json

def send_message(queue, message, rabbitmq_host='rabbitmq'):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(message))
    connection.close()

def receive_message(queue, callback, rabbitmq_host='rabbitmq'):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    
    def on_message(ch, method, properties, body):
        callback(json.loads(body))
    
    channel.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=True)
    channel.start_consuming()
