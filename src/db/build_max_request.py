import jsonpickle
import argparse
import logging.config

from pathlib import Path

from db_utils import fetch_sql
from DbObjectSetTest import DbObjectSetTest, DbObjectTest

logging.config.fileConfig(fname='logging.config')
logger = logging.getLogger(__name__)

#Build max request !
#sql_file must return row's result with  OBJECT_NAME and FIELD_NAME
#The request will be SELECT MAX({field_name}) FROM {object_name}
def build_max_request(db_name, test_set_name, sql_file_path):
    
    #I dont know why I have to add NOCOUNT ... but witout this it doesn't work
    sql = f'SET NOCOUNT ON\n'+Path(sql_file_path).read_text()
    results = fetch_sql(db_name,sql)

    t = DbObjectSetTest(test_set_name, db_name)
    [ t.append( DbObjectTest.init_max_request(row.OBJECT_NAME, row.FIELD_NAME)) for row in results ]
    
    json_file_path = fr'.\json\{db_name}_{test_set_name}.json'
    with open(json_file_path,'w') as f:        
        f.write(jsonpickle.encode(t, unpicklable=False, indent=4))

def main():
    
    #https://docs.python.org/fr/3/howto/argparse.html    
    parser = argparse.ArgumentParser(description='Build a json config file for performance test from a SQL request.')
    parser.add_argument('db_name', help='The db you want to test.')
    parser.add_argument('test_set_name', help='The name of the set.')
    parser.add_argument('sql_path', help=f'The sql request file to use to build the set.\
                            Must contain an OBJECT_NAME and FIELD_NAME' )
    args = parser.parse_args()
    build_max_request(args.db_name,args.test_set_name,args.sql_path)

if __name__ == "__main__":
    main()