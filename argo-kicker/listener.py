#!/usr/bin/env python
import pika
import psycopg2
import json
import re
import os

from dotenv import load_dotenv
load_dotenv()


QUEUE = 'hello'

DBERROR=3
QERROR=4


def create_db_handle(dbstring):
    """Create a psycopg2 compatible object from the connection string.
    The string is from PHP and we reuse it here.
    """
    mystr = dbstring[6:]
    mystr = mystr.rstrip()
    d = dict(re.findall(r'(\w+)=([^;]+);?', mystr))
    # Validate dbstring:
    for key in ['user', 'password', 'host', 'dbname']:
        if key not in d.keys():
            print(f'{key} not found in DBSTRING - {dbstring} - aborting')
            exit(DBERROR)
    return d



def connect_mq(host, queue):
    """ Connect to the message queue.
    
    :param str host: connect to this host. 
    :param str queue: named queue
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    return(channel)


def setup_listener(ch, q, callback):
    ch.basic_consume(
        queue=q, on_message_callback=callback, auto_ack=False)


def my_q_callback(ch, method, properties, body):
    """on_message_callback(channel, method, properties, body)  
        channel: BlockingChannel  
        method: spec.Basic.Deliver  
        properties: spec.BasicProperties  
        body: bytes  
    """
    print(f'Received {body}')
    print(f'Method delivery tag: {method.delivery_tag}')
    msg = None # scope!
    try:
        msg = json.loads(body)
    except Exception as e:
        print(f'JSON Error: {e}')
    
    # Message processed OK. We can ACK the message so it is marked as prosessed.
    ch.basic_ack(delivery_tag=method.delivery_tag)


host = os.getenv('MQ_HOST')
queue = os.getenv('QUEUE')
ch = None

try:
    ch = connect_mq(host, queue)
    setup_listener(ch, queue, my_q_callback)
except Exception as e:
    print(f'Got an error while setting up MQ: {e}')
    exit(QERROR)


print(f'Waiting for messages on queue {QUEUE}. To exit press CTRL+C')
ch.start_consuming()
