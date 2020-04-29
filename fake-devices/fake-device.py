#!/usr/bin/env python3
import os
import json
import time
import logging
import paho.mqtt.client as mqtt

logger = logging.getLogger("IoT fake-device logger")
logging.basicConfig(
        format='%(asctime)s [%(levelname)s]: %(message)s',
        level=logging.DEBUG,
        handlers=[
            logging.StreamHandler()
    ])

HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 1883))
TOPIC = os.getenv('TOPIC', "home_device")
USER_NAME = os.getenv('USER_NAME', "Zelong")
DEVICE_NAME = os.getenv('DEVICE_NAME', "bedroom-bulb")
INTERVAL = int(os.getenv('INTERVAL', 10))

# This is a simple ON/OFF event the Publisher
client = mqtt.Client()
client.connect(HOST, PORT, 60)

actions = ["ON", "OFF"]
cur_action = 0
while True:
    message = json.dumps({"userName": USER_NAME, "actionTimestamp": time.time(), "action": actions[cur_action], "deviceName": DEVICE_NAME})
    client.publish(TOPIC, message)
    cur_action = (cur_action+1) % 2
    logger.info("User {}'s Device {} sent message {} to topic {} on {}:{}. Send next message after {} second(s)".format(USER_NAME, DEVICE_NAME, message, TOPIC, HOST, PORT, INTERVAL))
    time.sleep(INTERVAL)

client.disconnect()