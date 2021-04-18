import pymongo
from database import Database as dB

testDB = dB.cluster['testDB']
test_coll1 = testDB['test_coll1']
static_data = testDB['static_data']


def get_all_database_names_in_cluster():
    return dB.cluster.list_database_names()


def get_all_collections_in_db(db_name: str) -> list:
    list_of_collections = []
    for collection in dB.cluster[db_name].list_collections():
        list_of_collections.append(collection['name'])
    return list_of_collections


def get_all_items_in_collection(db_name: str, collection_name: str):
    list_of_items = []
    for item in dB.get_all(dB.cluster[db_name][collection_name]):
        list_of_items.append(item)
    return list_of_items


print(dB.increment_one(static_data, {}, {'test_number': 7}))

result = get_all_items_in_collection('testDB', 'static_data')

print(result)



