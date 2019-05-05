import logging
import os

from pymongo import MongoClient, errors

import config

logger = logging.getLogger(__name__)

class Mongo():
    def __init__(self, table):
        if os.environ.get("env"):
            env = os.environ["env"]
        else:
            env = "dev"
        
        logger.debug("Instantiating Mongo Instance with table {}".format(table))

        self.client = MongoClient(host=config.MONGO["host"], port=config.MONGO["port"])
        self.db = self.client[config.MONGO['name']]
        self.table_name = table
        self.table = None

        logger.debug("Mongo successfully started")

    def create_table(self, table_index, is_unique):
        logger.debug("Creating table {} with index {} (unique: {})".format(self.table_name, table_index, is_unique))
        self.db[self.table_name].create_index(table_index, unique=is_unique)
        logger.debug("Table created.")
        self.table = self.db[self.table_name]

    def add_data(self, data):
        """
        Adds data to a table.

        table expects type string,
        data can be either dict (singleton) or list (multiple data inserts)
        """
        
        logger.debug("Adding {} to table {}".format(data, self.table_name))

        if type(data) is dict:
            try:
                self.table.insert_one(data)
            except errors.DuplicateKeyError:
                logger.debug("Exception caught, DuplicateKeyError. Data not added.")
                raise
        elif type(data) is list:
            try:
                self.table.insert_many(data)
            except Exception as e:
                logger.debug("Exception caught, error: %s" % str(e))
                raise
    
    def delete_data(self, key, value, all=True):
        """
        Deletes data from a table.

        table expects type string,
        key, value is the pair to match,
        all determines whether all matches are deleted, or only first
        """

        logger.debug("Deleting {}: {} from {} (all: {})".format(key, value, self.table_name, all))
        
        starting_length = self.table.count()

        if all:
            self.table.delete_many({key: value})
        else:
            self.table.delete_one({key: value})
        
        logger.debug("Removed {} items from table".format(starting_length - self.table.count()))

    def find_first(self, key, value):
        for result in self.table.find({key: value}):
            return result
        return

    def count(self):
        return self.table.count()
    
    def update_data(self, key, value, data):
        for result in self.table.find({key: value}):
            old = result
            new = {"$set": data}

            self.table.update_one(old, new)
            return
    
    def push_data_to_list(self, key, value, field, values):
        for result in self.table.find({key: value}):
            old = result
            new = {"$push": {field: values}}

            self.table.update_one(old, new)
            return