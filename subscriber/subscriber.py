#                               _
#                            _ooOoo_
#                           o8888888o
#                           88" . "88
#                           (| -_- |)
#                           O\  =  /O
#                        ____/`---'\____
#                      .'  \\|     |//  `.
#                     /  \\|||  :  |||//  \
#                    /  _||||| -:- |||||_  \
#                    |   | \\\  -  /'| |   |
#                    | \_|  `\`---'//  |_/ |
#                    \  .-\__ `-. -'__/-.  /
#                  ___`. .'  /--.--\  `. .'___
#               ."" '<  `.___\_<|>_/___.' _> \"".
#              | | :  `- \`. ;`. _/; .'/ /  .' ; |
#              \  \ `-.   \_\_`. _.'_/_/  -' _.' /
#    ===========`-.`___`-.__\ \___  /__.-'_.'_.-'================
#  
#!/usr/bin/env python3

########################################################
##########   Home Device Message Subscriber   ##########
########################################################

import os
import logging
import paho.mqtt.client as mqtt

from models import Message

URL = 'mongodb://project2:123789@expensetracker-shard-00-00-gnxoz.mongodb.net:27017,expensetracker-shard-00-01-gnxoz.mongodb.net:27017,expensetracker-shard-00-02-gnxoz.mongodb.net:27017/test?ssl=true&replicaSet=ExpenseTracker-shard-0&authSource=admin&retryWrites=true&w=majority'
DATABASE_URI = os.getenv('DATABASE_URI', URL)
TOPIC = os.getenv('TOPIC', 'home_device')
HOST = os.getenv('HOST', 'localhost')

logger = logging.getLogger("IoT message subscriber logger") 

def subscribe(topic, host='localhost', port=1883):
    def on_connect(client, userdata, flags, rc):
        logger.info("Connected with result code {}".format(str(rc)))
        client.subscribe(topic)
        logger.info("Subscribed to topic {}".format(topic))

    def on_message(client, userdata, msg):
        logger.info("Received the following message on topic {} with QoS {}: {}".format(msg.topic, msg.qos, msg.payload))
        message = Message(msg.payload)
        message.update_device_status()

    client = mqtt.Client()
    client.connect(host, port=port, keepalive=60, bind_address="")

    client.on_connect = on_connect
    client.on_message = on_message

    logger.info("Start subscriber")
    client.loop_forever()

def connect_DB():
    logger.info('Initializing DB connection...')
    Message.init(DATABASE_URI, logger)

def init_logger():
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s]: %(message)s',
        level=logging.DEBUG,
        handlers=[
            logging.StreamHandler()
    ])


if __name__ == '__main__':
    init_logger()

    logger.info(90 * '*')
    logger.info('  I O T   M E S S A G E S   C O L L E C T O R   S E R V I C E   R U N N I N G  '.center(90, '*'))
    logger.info(90 * '*')
    
    connect_DB()
    subscribe(TOPIC, host=HOST)
