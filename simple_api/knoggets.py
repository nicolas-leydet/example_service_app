from simple_api.mongo_storage import MongoStorage


class Knoggets(object):

    storage = MongoStorage('knoggets')

    def create(self, data):
        return self.storage.create(data)

    def find(self, query=None, offset=None, limit=None):
        return self.storage.find(query, offset, limit)

    def read(self, id):
        return self.storage.read(id)

    def update(self, id, data):
        return self.storage.update(id, data)

    def delete(self, id):
        return self.storage.delete(id)
