#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
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
        