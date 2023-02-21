# Copyright 2023 Massachusetts General Hospital.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from loguru import logger
import pandas as pd


def execSql(dataSource,sql_query='select count(*) from observation_fact',autocommit=False):
    
    if sql_query=='':
        msg='sql_query was empty'
        logger.warning(msg)
        return 
    try:
        sql_query_arr=re.split(r'\n\s*GO',sql_query)
        for sql_query in sql_query_arr:
            with dataSource as cursor:
                dataSource.connection.autocommit = autocommit
                cursor.execute(sql_query)
                dataSource.connection.commit()
                if cursor.rowcount>0:
                    logger.trace('Number of rows affected:'+str(cursor.rowcount))

                dataSource.connection.autocommit = False

    except Exception as e:
        logger.error("Error executing: {}",sql_query)
        raise Exception('pyodbc exception:',e)

def getPdf(dataSource,sql_query='select count(*) from observation_fact'):
    try:
        with dataSource as cursor:
            return pd.read_sql(sql_query, cursor.connection)
    except Exception as e:  
        logger.error("Error executing: {}",sql_query)
        raise Exception('pyodbc exception:',e)

def getDataFrameInChunks(sql,dataSource,chunksize=10000):
    with dataSource as cursor:
        try:
            dfl=[]
            for chunk in pd.read_sql_query(sql , cursor.connection, chunksize=chunksize):
                dfl.append(chunk)
            df = pd.concat(dfl, ignore_index=True)
            return df
        except Exception as e:
            logger.error("error in :{}",sql)

def getPdfUsingCursor(cursor,sql_query='select count(*) from observation_fact'):
    try:
        return pd.read_sql(sql_query, cursor.connection)
    except Exception as e:  
        logger.error("Error executing: {}",sql_query)
        raise Exception('pyodbc exception:',e)

def getDataFrameInChunksUsingCursor(cursor,sql,chunksize=10000):
    try:
        dfl=[]
        for chunk in pd.read_sql_query(sql , cursor.connection, chunksize=chunksize):
            dfl.append(chunk)
        df = pd.concat(dfl, ignore_index=True)
        return df
    except Exception as e:
        logger.error("error in :{}",sql)
        raise Exception('pyodbc exception:',e)        