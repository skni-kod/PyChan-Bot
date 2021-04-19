from Database.DatabaseClasses.base_classes.base_database_class import BaseDatabaseClass
from Database.DatabaseClasses.base_classes.base_database_system import BaseDatabaseSystem
from Database.database import Database as dB


class KarolServerClass(BaseDatabaseClass):
    def __init__(self, _id: int):

        class ServerSettings(BaseDatabaseClass):
            def __init__(self):
                self.prefix = '^'

        self._id = _id
        self.settings = ServerSettings()


class ServerClass(BaseDatabaseClass):
    def __init__(self, _id: int):
        self._id = _id
        self.prefix = '^'


class ServerSystem(BaseDatabaseSystem):
    _collection = dB.db_servers
    _class_template = ServerClass

    @classmethod
    def get_server(cls, server_id: int) -> ServerClass:
        """Returns [ServerClass] class instance from database"""
        return cls._get_one(server_id)

    @classmethod
    def add_new(cls, server_id: int):
        """Adds new template [ServerClass] to database"""
        return cls._insert_one(server_id)

    @classmethod
    def set_prefix(cls, server_id: int, new_prefix: str):
        return dB.update_one(cls._collection, {'_id': server_id}, {'prefix': new_prefix})

    @classmethod
    def get_prefix(cls, server_id: int) -> str:
        return dB.get_one(cls._collection, {'_id': server_id}, selection={'_id': 0, 'prefix': 1})['prefix']
