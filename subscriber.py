#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A small example subscriber
"""
import paho.mqtt.client as paho
import psycopg2

conn = psycopg2.connect(host="localhost", dbname="data_monitoring", user="postgres", password="123456",
                        port="5432")
cur = conn.cursor()

#cur.execute("""CREATE TABLE IF NOT EXISTS data_collected(
#    cpu_usage FLOAT,
#    mem_usage FLOAT,
#    disk_usage FLOAT
#    );
#""")
def on_message(mosq, obj, msg):
    print ("%-20s %s" % (msg.topic, msg.payload))
    topic = msg.topic
    curr_data = msg.payload

    numbers = list(filter(lambda x: x.isdigit(), curr_data.split()))
    result = [int(s) for s in numbers]
    print (result)
    if topic == 'cpu_usg':
        curr_cpu = curr_data

        #cur.execute("""INSERT INTO data_monitoring (cpu_usage) VALUES (curr_data)""")

        #postgres_insert_query = """ INSERT INTO data_monitoring (cpu_usage) VALUES ("curr_data")"""
        #record_to_insert = (curr_data)
        #cur.execute(postgres_insert_query, record_to_insert)
    if topic == 'mem_usg':
        curr_mem = curr_data
        #cur.execute("""INSERT INTO data_monitoring (mem_usage) VALUES (curr_data)""")
    if topic == 'disk_usg':
        curr_disk = curr_data
        #cur.execute("""INSERT INTO data_monitoring (disk_usage) VALUES (curr_data)""")
    #dados = msg.payload
    #INSERT dados no tópico

    #cur.execute("""INSERT INTO data_monitoring (cpu_usage, mem_usage, disk_usage)
    #VALUES (curr_cpu, curr_mem, curr_disk)""")

    #if (curr_mem != None and curr_disk != None and curr_cpu != None):
    postgres_insert_query = """ INSERT INTO data_collected (cpu_usage, mem_usage, disk_usage) 
    VALUES (1, 2, 3)"""
    record_to_insert = (12.3, 14.8, 16.9)
    cur.execute(""" INSERT INTO data_collected (cpu_usage, mem_usage, disk_usage) 
    VALUES (1, 2, 3)""")
    #curr_mem = None
    #curr_cpu = None
    #curr_disk = None

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
    client.subscribe("swap",0)
    client.subscribe("storage", 0)

    while client.loop() == 0:
        pass

# vi: set fileencoding=utf-8 :
