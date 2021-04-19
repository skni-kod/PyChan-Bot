import pymongo
from pymongo import MongoClient


from mongodb_token import mongodb_token


class Database:
    cluster = MongoClient(mongodb_token)
    db = cluster['PyChan']
    db_servers = db['servers']
    db_images = db['images']

    @classmethod
    def get_one(cls, collection: pymongo.collection, query: dict, selection=None) -> dict:
        """Returns data in as dict, and if found nothing,
         or failed by other means returns empty dict {}, so keep that in mind

        Arguments:
            collection {pymongo.collection} -- database collection class
            query {dict} -- query, something like {'_id': 1}

        Keyword Arguments:
            selection {dict} -- dict containing query, like {'_id': 1}

        Raises:
            TypeError -- description

        Returns:
            dict -- data as dict, could be empty if failed
        """
        if selection is not None:
            return collection.find_one(query, selection)
        return collection.find_one(query)

    @classmethod
    def get_many(cls, collection: pymongo.collection, query: dict, selection=None) -> list:
        """

        Arguments:
            collection {pymongo.collection} -- database collection class
            query {dict} -- dict, something like {'_id': 1}

        Keyword Arguments:
            selection {dict} -- Dict containing query, like {'_id': 1}

        Raises:
            TypeError -- description

        Returns:
           list -- List of returned objects, could be empty
        """
        if selection is not None:
            total_data = collection.find(query, selection)
        else:
            total_data = collection.find(query)

        list_of_data = [data for data in total_data]

        return list_of_data

    @classmethod
    def get_all(cls, collection: pymongo.collection, selection=None) -> list:
        """Returns list of found dictionaries, reduced to

        Arguments:
            collection {pymongo.collection} -- database collection class

        Keyword Arguments:
            selection {dict} -- Dict containing query, like {'_id': 1}

        Raises:
            TypeError -- description

        Returns:
            list -- List of returned objects, could be empty
        """

        if selection is not None:
            return cls.get_many(collection, {}, selection=selection)
        else:
            return cls.get_many(collection, {})

    @classmethod
    def insert_one(cls, collection: pymongo.collection, data: dict) -> bool:
        """ Make sure to not try to insert _id that is already in collection

        Arguments:
            collection {pymongo.collection} -- database collection class
            data {dict} -- data to insert, something like {'_id': 1, 'text': "something"}

        Keyword Arguments:
            kwarg {[type]} -- [description]

        Raises:
            pymongo.errors.DuplicateKeyError -- if {_id} is already in database

        Returns:
            bool -- Returns True if successfully inserted, False otherwise
        """
        return collection.insert_one(data).acknowledged

    @classmethod
    def insert_many(cls, collection: pymongo.collection, list_of_data: list) -> int:
        """ Make sure to not try to insert _ids that are already in collection

        Arguments:
            collection {pymongo.collection} -- database collection class instance
            list_of_data {list} -- list of dicts with data to insert,
            something like [{'_id': 1, 'text': "something"}, {'_id': 2}]

        Keyword Arguments:
            kwarg {[type]} -- [description]

        Raises:
            pymongo.errors.DuplicateKeyError -- if {_id} is already in database

        Returns:
            bool -- Count of items that were successfully inserted
        """
        return collection.insert_many(list_of_data).inserted_ids.__len__()

    @classmethod
    def update_one(cls, collection: pymongo.collection, query: dict, data_to_update: dict) -> bool:
        """Updates one item in collection

        Arguments:
            collection {pymongo.collection} -- database collection class instance
            query {dict} -- dict, something like {'_id': 1}
            data_to_update {dict} -- dict, something like {'value1': 1}

        Keyword Arguments:
            kwarg {[type]} -- [description]

        Raises:
            TypeError -- [description]

        Returns:
            bool -- Returns True if operation was successful, False otherwise
        """
        return collection.update_one(query, {'$set': data_to_update}).acknowledged

    @classmethod
    def update_many(cls, collection: pymongo.collection, query: dict, data_to_update: dict) -> int:
        """Updates multiple items in collection

        Arguments:
            collection {pymongo.collection} -- database collection class instance
            query {dict} -- dict, something like {'_id': 1}
            data_to_update {dict} -- dict, something like {'value1': 1}

        Keyword Arguments:
            kwarg {[type]} -- [description]

        Raises:
            TypeError -- [description]

        Returns:
            int -- Returns count of items that matched the query
        """
        return collection.update_many(query, {'$set': data_to_update}).matched_count

    @classmethod
    def update_all(cls, collection: pymongo.collection, data_to_update: dict) -> int:
        """Updates multiple items in collection

        Arguments:
            collection {pymongo.collection} -- database collection class instance
            data_to_update {dict} -- dict, something like {'value1': 1}

        Keyword Arguments:
            kwarg {[type]} -- [description]

        Raises:
            TypeError -- [description]

        Returns:
            int -- Returns count of items that matched the query
        """
        return cls.update_many(collection, {}, data_to_update)

    @classmethod
    def delete_one(cls, collection: pymongo.collection, query: dict) -> bool:
        """Deletes one item from collection

        Arguments:
            collection {pymongo.collection} -- database collection class instance
            query {dict} -- dict, something like {'_id': 1}

        Keyword Arguments:
            kwarg {[type]} -- [description]

        Raises:
            TypeError -- [description]

        Returns:
            bool -- Returns True if successfully deleted one item
        """
        return collection.delete_one(query).deleted_count == 1

    @classmethod
    def delete_many(cls, collection: pymongo.collection, query: dict) -> int:
        """Deletes multiple items from collection

        Arguments:
            collection {pymongo.collection} -- database collection class instance
            query {dict} -- dict, something like {'_id': 1}

        Keyword Arguments:
            kwarg {[type]} -- [description]

        Raises:
            TypeError -- [description]

        Returns:
            int -- Returns count of deleted items
        """
        return collection.delete_many(query).deleted_count

    @classmethod
    def delete_all(cls, collection: pymongo.collection) -> int:
        """Deletes all items in the collection

        Arguments:
            collection {pymongo.collection} -- database collection class instance

        Keyword Arguments:
            kwarg {[type]} -- [description]

        Raises:
            TypeError -- [description]

        Returns:
            int -- Returns count of deleted items
        """
        return cls.delete_many(collection, {})

    @classmethod
    def increment_one(cls, collection: pymongo.collection, query: dict, data_to_increment: dict) -> bool:
        """Increments one item, for example {'value1': 12, 'value2': -4},
         it would increase value1 by 12 and decrease value2 by 4

        Arguments:
            collection {pymongo.collection} -- database collection class instance
            query {dict} -- dict, something like {'_id': 1}
            data_to_increment -- dict, something like {'value1': -11}

        Keyword Arguments:
            kwarg {[type]} -- [description]

        Raises:
            TypeError -- [description]

        Returns:
            bool -- Returns True if operation was successful, False otherwise
        """
        return collection.update_one(query, {'$inc': data_to_increment}).acknowledged

    @classmethod
    def increment_many(cls, collection: pymongo.collection, query: dict, data_to_increment: dict) -> int:
        """Increments many items by values specified in dict,
         for example {'value1': 12, 'value2': -4},
         it would increase value1 by 12 and decrease value2 by 4,
         of all the items that matched query

        Arguments:
            collection {pymongo.collection} -- database collection class instance
            query {dict} -- dict, something like {'_id': 1}
            data_to_increment -- dict, something like {'value1': -11}

        Keyword Arguments:
            kwarg {[type]} -- [description]

        Raises:
            TypeError -- [description]

        Returns:
            int -- Returns count of items found by query
        """
        return collection.update_many(query, {'$inc': data_to_increment}).matched_count

    @classmethod
    def increment_all(cls, collection: pymongo.collection, data_to_increment: dict) -> int:
        """Increments all items in collection items by values specified in dict,
         for example {'value1': 12, 'value2': -4},
         it would increase value1 by 12 and decrease value2 by 4

        Arguments:
            collection {pymongo.collection} -- database collection class instance
            data_to_increment -- dict, something like {'value1': -11}

        Keyword Arguments:
            kwarg {[type]} -- [description]

        Raises:
            TypeError -- [description]

        Returns:
            int -- Returns count of items found by query
        """
        return cls.increment_many(collection, {}, data_to_increment)

    @classmethod
    def check_connect_with_db(cls):
        try:
            Database.cluster.server_info()
            print('[MongoDB] Baza połączona')
        except Exception as err:
            return err
        return True

