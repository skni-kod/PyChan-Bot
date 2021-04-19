from Database.database import Database as dB


class BaseDatabaseSystem:
    _collection = None
    _class_template = None

    @classmethod
    def _get_one(cls, _id: int):
        return cls._class_template(_id).load(dB.get_one(cls._collection, {'_id': _id}))

    @classmethod
    def _insert_one(cls, _id: int):
        return dB.insert_one(cls._collection, cls._class_template(_id).json())
