
import logging
import jsonpickle
    
#To be precise
from datetime import datetime

from db_utils import execute_sql, fetch_sql

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestDbObject():

    def __init__(self, name):
        self.name = name
        self.requests = dict()

    @classmethod
    def init_max_request(cls, name, field, sql_type):
        obj = cls(name)
        obj.add_request(f'SELECT MAX({field}) FROM {name}', sql_type)
        return obj   

    def add_request(self, sql, test_type = 'Unknow'):
        self.requests[test_type] = sql

    def add_request(self, sql, test_type = 'Unknow'):
        self.requests[test_type] = sql

    def get_request(self, test_type):
        return self.requests[test_type]

#Build a file with MAX request on base_file_date field  for DRM_INT DB
# Maybe we can find the name of the field dynamically ??   
def build_drmt_int(file_path):
    
    results = fetch_sql('DRM_INT','SELECT CONCAT(TABLE_SCHEMA,\'.\',TABLE_NAME)'\
        ' AS TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS ORDER BY TABLE_SCHEMA,TABLE_NAME')
    
    tests = [ TestDbObject.init_max_request(row.TABLE_NAME,'base_file_date','max_main_index') for row in results ]
    
    with open(file_path,'w') as f:        
        f.write(jsonpickle.encode(tests, unpicklable=False, indent=4))

def execute_test(file_path):

    save_result = 'INSERT INTO [control].[PerformanceResults] VALUES (?,?,?,?,?,?,?,?)'
    bd = 'DRM_INT'
    request_type = 'max_main_index'

    with open(file_path,'r') as f:
        tests = jsonpickle.decode(f.read())
    
    #Add an execution date
    for batch_id in range(1,6):
        for test in tests:
            
            obj_name = test['name']
            request = test['requests'][request_type]

            start = datetime.now()
            res = fetch_sql(bd,request)
            end = datetime.now()
            
            execution_time = (end - start).total_seconds()
            sql_time = start.strftime("%Y-%m-%d %H:%M:%S.%f")
            
            execute_sql('DRM_DV1_CTL', save_result, \
                        [[batch_id,bd,obj_name,request_type,request,res[0][0],execution_time,sql_time]], \
                        False)
            
            logging.info(f'Select {obj_name} in {execution_time:02f}')

def main():
    
    build_drmt_int(fr'.\sql\drmt_int.json')
   
    
    #execute_test(fr'.\sql\drmt_int_adjust.json')

if __name__ == "__main__":
    main()
