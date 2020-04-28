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


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """


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
            self.device_id = msg_dict['device_id']
            self.action = msg_dict['action']
            self.action_timestamp = msg_dict['action_timestamp']
        except KeyError as error:
            self.logger.error('Invalid message payload: missing ' + error.args[0])

    def update_device_status(self):
        """
        Update device status record in the Database
        """
        data_dict = self.serialize()
        try:
            if self.collection.find({'device_id': self.device_id}).count() == 0:
                data_dict['duration_use_in_seconds'] = 0
                result = self.collection.insert_one(data_dict)
                self.logger.info('Inserted message "{}" with ID {}'.format(data_dict, result.inserted_id))
            else:
                device_status = self.collection.find_one({'device_id': self.device_id})
                if device_status['action'] != self.action:
                    # Remove all record and re-insert one new record to ensure that
                    # every device will only have at most one status record in the DB
                    self.collection.delete_many({'device_id': self.device_id})

                    # Update duration of use
                    duration = device_status['duration_use_in_seconds']
                    if device_status['action'] == 'ON' and self.action == 'OFF':
                        duration += self.action_timestamp - device_status['action_timestamp']
                    
                    # Add duration field and insert data into DB
                    data_dict['duration_use_in_seconds'] = duration
                    result = self.collection.insert_one(data_dict)
                    self.logger.info('Updated message "{}" with ID {}'.format(data_dict, result.inserted_id))
        except HTTPError as error:
            self.logger.error('Create failed: {}'.format(error))
        # except Exception as error:
        #     raise

    def serialize(self):
        """ Serializes a device message into a dictionary """
        return {
            "device_id": self.device_id,
            "action": self.action,
            "action_timestamp": self.action_timestamp,
        }

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
            Message.collection = client.test.messages
        except ConnectionError:
            raise DatabaseConnectionError(
                'MongoDB service could not be reached')
