#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
Publish some messages to queue
"""
import paho.mqtt.publish as publish


msgs = [{'topic': "cpu_usg", 'payload': "jump"},
        {'topic': "adult/news", 'payload': "extra extra"},
        {'topic': "adult/test", 'payload': "super extra"},
        {'topic': "test/topic", 'payload' : "new_message"}]

host = "localhost"


if __name__ == '__main__':
    # publish a single message
    publish.single(topic="kids/yolo", payload="just do it", hostname=host)

    # publish multiple messages
    publish.multiple(msgs, hostname=host)


# vi: set fileencoding=utf-8 :
