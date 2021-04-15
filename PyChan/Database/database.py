import pymongo
from pymongo import MongoClient
from pymongo import collection

from PyChan.mongodb_token import mongodb_token


class Database():
    cluster = MongoClient(mongodb_token)
    db = cluster['PyChan']
    db_servers = db['servers']
    db_images = db['images']

    @staticmethod
    def get_one(collection, query, selection = {}):
        if not selection:
            return collection.find_one(query)
        return collection.find_one(query, selection)


    @staticmethod
    def insert_one(collection, data):
        collection.insert_one(data)

    @staticmethod
    def update_one(collection, query, query_to_update):
        return collection.update_one(query, {'$set': query_to_update}).modified_count == 1

    @staticmethod
    def check_connect_with_db():
        try:
            Database.cluster.server_info()
            print('[MongoDB] Baza połączona')
        except Exception as err:
            return err
        return True
