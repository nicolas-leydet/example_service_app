from pymongo import MongoClient, ReturnDocument
from bson import ObjectId

from simple_api.settings import MONGODB_URI, MONGO_DB_NAME


# TODO manage connection errors
class MongoStorage(object):
    def __init__(self, collection_name):
        self.collection_name = collection_name

    def setup(self):
        self.client = MongoClient(MONGODB_URI, maxPoolSize=500)
        self.db = self.client[MONGO_DB_NAME]
        self.collection = self.db[self.collection_name]

    def terminate(self):
        self.client.close()

    def create(self, data):
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def update(self, id, data):
        filter_ = {'_id': ObjectId(id)}
        data.pop('id', None)
        result = self.collection.find_one_and_replace(
            filter_, data, return_document=ReturnDocument.AFTER)
        if not result:
            raise KeyError()
        return transform_id(result)

    def delete(self, id):
        result = self.collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 0:
            raise KeyError()

    def find(self, query, offset, limit):
        result = self.collection.find({})
        return [transform_id(doc) for doc in result]

    def read(self, id):
        result = self.collection.find_one({'_id': ObjectId(id)})
        if not result:
            raise KeyError()
        return transform_id(result)

    def bulk_insert(self, data):
        obj_ids = self.collection.insert_many(data)
        return [str(obj_id) for obj_id in obj_ids.inserted_ids]

    def clear(self):
        self.collection.delete_many({})


def transform_id(doc):
    doc['_id'] = str(doc['_id'])
    return doc
