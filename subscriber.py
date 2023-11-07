#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A small example subscriber
"""
import paho.mqtt.client as paho
#import psycopg2
from pymongo import MongoClient


try:
    conn = MongoClient('localhost', 27017)
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

db = conn.tests

collection = db.sensors


def on_message(mosq, obj, msg):
    print ("%-20s %s" % (msg.topic, msg.payload))


    read1 = {
        format(msg.payload.decode("utf-8"))
    }

    #print(msg.topic + " message payload is {}".format(msg.payload.decode("utf-8")))

    print (read1)

    insert1 = collection.insert_one(read1)

    # recuperar todos os registros ja inseridos
    cursor = collection.find()
    for record in cursor:
        print(record)

    topic = msg.topic
    curr_data = msg.payload


    mosq.publish('pong', 'ack', 0)

def on_publish(mosq, obj, mid):
    pass

if __name__ == '__main__':
    client = paho.Client()
    client.on_message = on_message
    client.on_publish = on_publish

    #client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    client.connect("127.0.0.1", 1883, 60)

    client.subscribe("cpu_usg", 0)
    client.subscribe("mem_usg", 0)
    #client.subscribe("storage", 0)

    while client.loop() == 0:
        pass



# vi: set fileencoding=utf-8 :
