import logging
import pyodbc 
import time

logger = logging.getLogger(__name__)

#pooling=False mandatory to avoid lost connexion ! I think it's helping
#Communication link failure (10060)
db_config = {'DRM_DV1_CTL':'Driver={ODBC Driver 17 for SQL Server};server=BDDVEDRM;database=DRM_DV1_CTL;trusted_connection=yes;ConnectRetryCount=5;ConnectRetryInterval=30;pooling=False',\
            'DRM_INT':'Driver={ODBC Driver 17 for SQL Server};server=AGPRDRM;database=DRM_INT;trusted_connection=yes;ConnectRetryCount=5;ConnectRetryInterval=30;pooling=False'}
db_cursor = {}
db_cnxn = {}

#If we had an sql Error,try to obtain a valid connexion before a retry
wait_valid_connexion = True

#Time to wait before a retry for a good connexion or a direct retry
waiting_time = 30

#Max number of retry  
max_attempt = 3

def get_all_config():
    return db_config

#Autocommit is set to False by default, nothing to do !
def get_connexion(db_name):
    if db_name not in db_cnxn : 
        config = db_config.get(db_name)
        if(config is None): raise Exception(f'db_utilsException: Unknow db {db_name}')
        logger.info(f'Open a connexion {db_name}')
        cnxn = pyodbc.connect(config)
        db_cnxn[db_name] = cnxn

    return db_cnxn[db_name]

#Set fast_executemany to True by default !
def get_cursor(db_name):
    if db_name not in db_cursor : 
        logger.debug(f'Open a cursor {db_name}')
        db_cursor[db_name] = get_connexion(db_name).cursor()
        #To go fast
        db_cursor[db_name].fast_executemany = True
    return db_cursor[db_name]

#If params, it will use executemany ...
#If you have params, you should have a query with params 
#There is no return info with executemany
#For a single query it's return cursor, else it's return None
def execute_sql(db_name, sql, params = None, commit = False):
    
    for attempt in range(max_attempt):
        try:
            cursor = get_cursor(db_name)
            res = cursor.execute(sql) if params == None else cursor.executemany(sql, params)   
            if(commit): cursor.commit()
            return res
        except Exception as ex:
            manage_exception(db_name,attempt,ex)
        
#Return a list of Row. 
#Row is tuple-like https://github.com/mkleehammer/pyodbc/wiki/Row
def fetch_sql(db_name, sql, params = []):

    for attempt in range(max_attempt):
        try:
            cursor = get_cursor(db_name)        
            cursor.execute(sql, params)
            return cursor.fetchall()
        except Exception as ex:
            manage_exception(db_name,attempt,ex)

def manage_exception(db_name, attempt, ex):
    #After max_attempt we raise the exception
    if( attempt == max_attempt-1):
        raise ex
    else:
        logger.info(f'SQLException --> {ex}')
        #We wait indefinitely for a valid connexion 
        #Always better ?
        if(wait_valid_connexion):
            wait_valid_connexion(db_name)
        #We just wait seconds before a retry
        else:
            logger.info(f'{db_name} wait {waiting_time} seconds after {attempt+1} attempts.')
            time.sleep(waiting_time)
            
#We retry indefinitely until success    
def wait_valid_connexion(db_name):
    
    logger.info(f'{db_name} start to wait a valid connexion.')
    attempt = 0
    while(True):
        try:
            attempt += 1
            #Just to be sure we close and reopen the connexion ?
            #close_cnxn(db_name)
            #get_connexion(db_name)
            res = fetch_sql(db_name,'SELECT 1')
            if (res[0][0] == 1): 
                logger.info(f'{db_name} end to wait a valid connexion after {attempt} attempts.')
                break

            logger.info(f'{db_name} wait {waiting_time} seconds after {attempt} attempts.')
            time.sleep(waiting_time)
            
        except Exception as e:
            logger.exception(f'Silent sql exception on close an retry ..........')
            logger.exception(f'{e}')
            logger.exception(f'Silent sql exception on close an retry ..........')
    
    
    

def close_cursor(db_name):
    logger.debug(f'Close cursor {db_name}')
    cursor = db_cursor.pop(db_name, None)
    if(cursor is not None): cursor.close()
    
def close_cnxn(db_name):
    close_cursor(db_name)

    logger.info(f'Close connexion {db_name}')
    cnxn = db_cnxn.pop(db_name,None)
    if(cnxn is not None): cnxn.close()  
    

def close_all_cnxn():   
    for db_name in list(db_cnxn.keys()):
        close_cnxn(db_name)

import atexit
atexit.register(close_all_cnxn)



