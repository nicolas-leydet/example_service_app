import os

MONGODB_URI = os.environ.get('SIMPLE_API_MONGO_DB_URI',
                             'mongodb://localhost:27017/')

MONGO_DB_NAME = 'simple_api'
