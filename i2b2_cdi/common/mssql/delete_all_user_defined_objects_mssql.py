#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#

from db_helper import DBHelper
import os
from dotenv import load_dotenv
import argparse



sql_del_tables='''use ..
        DECLARE @sql NVARCHAR(max)=''

        SELECT @sql += ' Drop table ' + QUOTENAME(TABLE_SCHEMA) + '.'+ QUOTENAME(TABLE_NAME) + '; '
        FROM   INFORMATION_SCHEMA.TABLES
        WHERE  TABLE_TYPE = 'BASE TABLE'

        --PRINT @sql

        Exec Sp_executesql @sql

        '''

sql_del_functions='''
        use ..
        Declare @sql NVARCHAR(MAX) = N'';

        SELECT @sql = @sql + N' DROP FUNCTION ' 
                        + QUOTENAME(SCHEMA_NAME(schema_id)) 
                        + N'.' + QUOTENAME(name)
        FROM sys.objects
        WHERE type_desc LIKE '%FUNCTION%';

        --PRINT @sql

        Exec Sp_executesql @sql
        '''                     

def getArgs():
    my_parser = argparse.ArgumentParser()
    my_parser.version = '0.1'
    my_parser.add_argument('-e','--env-path', type=str,action='store',\
         default='-',\
         help='reads file for environment')
    my_parser.add_argument('--version', action='version') 
    return my_parser.parse_args()
if __name__ == "__main__":
    args = getArgs()
    args.env_path=".."
    
    print('in main:',args) 
    try:
        
        load_dotenv(args.env_path)
        print("connecting to : ",os.getenv('I2B2_DS_CRC_DB'))
        d=DBHelper(ip=os.getenv('I2B2_DS_CRC_IP'),port=os.getenv('I2B2_DS_CRC_PORT'),db=os.getenv('I2B2_DS_CRC_DB'),\
            user=os.getenv('I2B2_DS_CRC_USER'),
            password=os.getenv('I2B2_DS_CRC_PASS'))       
       
        #d.execSql("quit;")
        print("deleting user-defined tables")
        d.execSql(sql_del_tables)
        print("deleting user-defined functions")
        d.execSql(sql_del_functions)
    except Exception as e:
        raise Exception("error",e)