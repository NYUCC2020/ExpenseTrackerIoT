#!/usr/bin/env python3
import os
import json
import time
import paho.mqtt.client as mqtt

HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', 1883)

# This is a simple ON/OFF event the Publisher
client = mqtt.Client()
client.connect(HOST, PORT, 60)

client.publish("home_device", json.dumps({"action_timestamp": time.time(), "action": "OFF", "device_id": "0"}))

client.disconnect()