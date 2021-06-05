
class DbObjectSetTest():
    def __init__(self, test_name, db_name):
        self.test_set_name = test_name
        self.db_name = db_name  
        self.lst = list()

    def append(self, obj):
        self.lst.append(obj)

class DbObjectTest():

    def __init__(self, object_name):
        self.object_name = object_name
        self.requests = dict()

    @classmethod
    def init_max_request(cls, object_name, field ):
        obj = cls(object_name)
        obj.add_request(f'SELECT MAX({field}) FROM {object_name}', f'max_{field}')
        return obj   

    def add_request(self, sql, request_name = 'Unknow'):
        self.requests[request_name] = sql

    def get_request(self, test_type):
        return self.requests[test_type]

