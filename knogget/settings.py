import os

MONGO_DB_NAME = 'knogget'

MONGODB_URI = os.environ.get('KNOGGET_MONGO_DB_URI',
                             'mongodb://localhost:27017/')

MONGO_POOL_SIZE = os.environ.get('KNOGGET_MONGO_POOL_SIZE', 2048)
