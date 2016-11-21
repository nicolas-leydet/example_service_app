import os

MONGODB_URI = os.environ.get('knogget_MONGO_DB_URI',
                             'mongodb://localhost:27017/')

MONGO_DB_NAME = 'knogget'
