import logging
import pyodbc 

#https://github.com/mkleehammer/pyodbc/wiki/Cursor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

db_config = {'DRM_DV1_CTL':'Driver={ODBC Driver 17 for SQL Server};server=BDDVEDRM;database=DRM_DV1_CTL;trusted_connection=yes',\
            'DRM_INT':'Driver={ODBC Driver 17 for SQL Server};server=AGPRDRM;database=DRM_INT;trusted_connection=yes'}
db_cursor = {}
db_cnxn = {}

def get_all_config():
    return db_config

#Autocommit is set to False by default, nothing to do !
def get_connexion(db_name):
    if db_name not in db_cnxn : 
        config = db_config.get(db_name)
        logging.info(f'Open a connexion {db_name}')
        cnxn = pyodbc.connect(config)
        db_cnxn[db_name] = cnxn

    return db_cnxn[db_name]

#Set fast_executemany to True by default !
def get_cursor(db_name):
    if db_name not in db_cursor : 
        logging.debug(f'Open a cursor {db_name}')
        db_cursor[db_name] = get_connexion(db_name).cursor()
        #To go fast
        db_cursor[db_name].fast_executemany = True
    return db_cursor[db_name]

#If params, it will use executemany ...
#If you have params, you should have a query with params 
#There is no retunr info with executemany
#For a single query it's return cursor, else it's return None
def execute_sql(db_name, sql, params = None, commit = False):
    cursor = get_cursor(db_name)
    try:
        res = cursor.execute(sql) if params == None else cursor.executemany(sql, params)   
        if(commit): cursor.commit()
        return res
    except Exception as e:
        logger.exception(f'Exception:{e} \nSQL:{sql}\nParams {params}')
    

#Return a list of Row. 
#Row is tuple-like https://github.com/mkleehammer/pyodbc/wiki/Row
def fetch_sql(db_name, sql, params = []):
    
    cursor = get_cursor(db_name)
    try:
        cursor.execute(sql, params)
        return cursor.fetchall()
    except Exception as e:
        logger.exception(f'Exception:{e} \nSQL:{sql}\nParams {params}')


def close_cnxn():   
    for db_name, cursor in db_cursor.items():
        logging.debug(f'Close a cursor {db_name}')
        cursor.close()
    
    for db_name, cnxn in db_cnxn.items():
        logging.info(f'Close a connexion {db_name}')
        cnxn.close()

import atexit
atexit.register(close_cnxn)



