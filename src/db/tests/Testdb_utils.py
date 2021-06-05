import logging
import unittest
import pyodbc

from db_utils import get_all_config
from db_utils import execute_sql
from db_utils import fetch_sql
from db_utils import get_connexion
from db_utils import get_cursor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Testdb_utils(unittest.TestCase):

    def __init__(self,*args, **kwargs):
        super(Testdb_utils, self).__init__(*args, **kwargs)
        self.db_name = next(iter(get_all_config()))
    
    
    def test_get_all_config(self):
        self.assertGreater(len(get_all_config()),0)

    def test_get_connexion(self):
        cnxn = get_connexion(self.db_name)
        self.assertIsInstance(cnxn, pyodbc.Connection )
        logging.info(f'{self.db_name} autocommit :{cnxn.autocommit}')
        

    def test_get_cursor(self):
        cursor = get_cursor(self.db_name)
        self.assertIsInstance(cursor, pyodbc.Cursor )
        logging.info(f'{self.db_name} fast cursor :{cursor.fast_executemany}')

    def test_execute_sql(self):
        
        cnxn = get_connexion(self.db_name)
        cnxn.autocommit = False

        
        #Useless with rollback
        #res = execute_sql(self.db_name,'DROP TABLE IF EXISTS TEST1')
        #self.assertEqual(res.rowcount, -1)
        
        #We can't have a real status on CREATE/DROP ...
        res = execute_sql(self.db_name,'CREATE TABLE TEST1(COL1 INT)')
        self.assertEqual(res.rowcount, -1)

        #We can have a status on INSERT/UPDATE/DELETE with single query
        res = execute_sql(self.db_name,'INSERT INTO TEST1 VALUES (1),(2)')
        self.assertEqual(res.rowcount, 2)

        #We can't have a status on INSERT/UPDATE/DELETE with multiple queries with parameters
        res = execute_sql(self.db_name,'INSERT INTO TEST1 VALUES (?)', [[3],[4]])
        self.assertIsNone(res)

        res = fetch_sql(self.db_name,'SELECT * FROM TEST1')
        self.assertEqual(len(res),4)

        #Add an Exception to Raise ?
        #res = fetch_sql(self.db_name,'SELECT * FROM TOTO')
        #Add a test to perform with wait_until_the_end
        #self.assertRaises(Exception,execute_sql,self.db_name,'SELECT * FROM TOTO')

        res = execute_sql(self.db_name,'DROP TABLE IF EXISTS TEST1')
        
        res = fetch_sql(self.db_name,'SELECT 1')
        self.assertEqual(res[0][0],1)

        cnxn.rollback();

    def test_manage_exception(self):
        #res = fetch_sql(self.db_name,'SELECT * FROM TOTO')
        #Add a test to perform with wait_until_the_end
        self.assertRaises(Exception,fetch_sql,self.db_name,'SELECT * FROM TOTO')

        self.assertRaises(Exception,execute_sql,self.db_name,'SELECT * FROM TOTO')

    def test_fetch_sql(self):
        
        res = fetch_sql(self.db_name,'SELECT 1')
        self.assertEqual(res[0][0],1)
        
        res = fetch_sql(self.db_name,'SELECT ?',2)
        self.assertEqual(res[0][0],2)
        

if __name__ == '__main__':
    unittest.main()
