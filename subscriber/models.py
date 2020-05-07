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
#                            `=--=-'                    BUG FREE
"""
All models should be defined here
"""

import os
import sys
import time
import json
import logging
from requests import HTTPError, ConnectionError

from pymongo import MongoClient
from bson.objectid import ObjectId

class DatabaseConnectionError(Exception):
    """ Custom Exception when database connection fails """


class Message():
    """
    Class that represents a Message
    """
    logger = logging.getLogger("IoT message subscriber logger") 
    collection = None

    def __init__(self, message):
        """ Constructor """
        msg_dict = json.loads(message)
        try:
            self.userId = ObjectId(msg_dict['userId'])
            self.deviceName = msg_dict['deviceName']
            self.action = msg_dict['action']
            self.actionTimestamp = msg_dict['actionTimestamp']
        except KeyError as error:
            self.logger.error('Invalid message payload: missing ' + error.args[0])

    def update_device_status(self):
        """
        Update device status record in the Database
        """
        criteria = {'userId': self.userId, 'deviceName': self.deviceName}
        try:
            if self.collection.find(criteria).count() == 0:
                self.logger.error('Device(Name: {}) does not exist'.format(self.deviceName))
            else:
                device = self.collection.find_one(criteria)
                if device['status'] != self.action:
                    # Remove all record and re-insert one new record to ensure that
                    # every device will only have at most one status record in the DB
                    self.collection.delete_many(criteria)

                    # Update duration field and re-insert into DB
                    if device['status'] == 'ON' and self.action == 'OFF':
                        device['activeSeconds'] += self.actionTimestamp - device['statusUpdateTime']

                    device['status'] = self.action
                    device['statusUpdateTime'] = self.actionTimestamp
                    result = self.collection.insert_one(device)
                    self.logger.info('Inserted record "{}" with ID {}'.format(device, result.inserted_id))
        except HTTPError as error:
            self.logger.error('Create failed: {}'.format(error))

############################################################
#  D A T A B A S E   C O N N E C T I O N
############################################################
    @staticmethod
    def init(database_url, _logger):
        """
        Initialized MongoDB database connection
        """
        Message.logger = _logger
        try:
            client = MongoClient(database_url)
            Message.collection = client.test.devices
        except ConnectionError:
            raise DatabaseConnectionError(
                'MongoDB service could not be reached')
