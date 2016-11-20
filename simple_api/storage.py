class Storage(object):
    def __init__(self):
        self.table = {}
        self.index = 0


db = Storage()


def set_db_fixture(fixture):
    db.table = fixture
    db.index = max(fixture.keys()) + 1
