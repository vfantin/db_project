
import logging.config
import jsonpickle
import argparse
import os

#To be precise
from datetime import datetime

from db_utils import execute_sql, fetch_sql

#logger = logging.getLogger(__name__) ... __name__ = __main__ not very pretty
logger = logging.getLogger(os.path.basename(__file__).split('.')[0])

def execute_test(file_path):

    db_save = 'DRM_DV1_CTL'
    save_result = 'INSERT INTO [control].[PerformanceResults2] VALUES (?,?,?,?,?,?,?,?,?)'
    
    batch_guid = ''

    with open(file_path,'r') as f:
        tst_set = jsonpickle.decode(f.read())
    
    db_name = tst_set['db_name']
    test_set_name = tst_set['test_set_name']

    for test in tst_set['lst']:
        
        obj_name = test['object_name']
        for rq_name in test['requests']:
            rq = test['requests'][rq_name]   
            
            start = datetime.now()
            res = fetch_sql(db_name,rq)
            end = datetime.now()
            execution_time = (end - start).total_seconds()
            
            sql_time = start.strftime("%Y-%m-%d %H:%M:%S.%f")
            if( batch_guid == ''): batch_guid = sql_time

            execute_sql(db_save, save_result, \
                         [[batch_guid,test_set_name,db_name,obj_name,rq_name,rq,res[0][0],execution_time,sql_time]], \
                         True)
            logger.info(f'Select {obj_name}-{rq_name} in {execution_time:02f}')

def main():
    
    #https://docs.python.org/fr/3/howto/argparse.html    
    parser = argparse.ArgumentParser(description='Test db performace.')
    parser.add_argument('json_path', help='The json config file to use.')
    parser.add_argument('log_path', help='The log config file to use.')
    parser.add_argument('-n', type=int, default=1, help='Number of times you want to execute test.')
    args = parser.parse_args()

    logging.config.fileConfig(fname=args.log_path)
    
    for i in range(args.n):
        logger.info(f'Start to run {args.json_path} ({i+1}/{args.n})')
        execute_test(args.json_path)
        
if __name__ == "__main__":
    main()
