#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`DatabaseInitialization` -- I2B2 Database Initialization 
=============================================

.. module:: DatabaseInitialization
    :platform: Linux/Windows
    :synopsis: module contains method for upgrading i2b2 project database.

"""
from loguru import logger
from i2b2_cdi.config.config import Config
import sys
from i2b2_cdi.database import execSql, DataSource
from i2b2_cdi.common.py_bcp import PyBCP
import glob
from i2b2_cdi.common.file_util import str_from_file
from i2b2_cdi.database.cdi_db_executor import execSql
def initDatabase(args):
    try:
        logger.trace(args)
        #creation of datasource object
        proj_ds=DataSource( ip=args.host,
            port=args.port,
            database=args.database_name,
            username=args.user_name,
            password=args.password,
            dbType='mssql')

        sourcePath="i2b2_cdi/project/resources/sql/initDatabase/"

        for file in glob.glob(sourcePath+'/*.sql'):
            logger.trace(file)
            if(file.__contains__("i2b2hive")):
                #updating the hive sql for db_lookup table records.
                hiveSql=str_from_file(file)
                updatedHiveSql=hiveSql.replace("{DATABASE_NAME}",proj_ds.database)
                execSql(proj_ds,updatedHiveSql)
            else:
                #bcp object 
                _bcp = PyBCP(
                    table_name="table_name",
                    import_file='',
                    delimiter='~@~',
                    batch_size=10000,
                    error_file="/error_execute_sql.log")
                _bcp.execute_sql(file,proj_ds)

        #generation of .env file
        env=str_from_file(sourcePath+"/.env")
        UpdatedEnv=env.replace("{I2B2_DB_HOST}",proj_ds.ip).replace("{I2B2_DB_USER}",proj_ds.username).replace("{I2B2_DB_PASSWORD}",proj_ds.password).replace("{I2B2_DB_NAME}",proj_ds.database).replace("{I2B2_DB_PORT}",proj_ds.port).replace("{I2B2_DB_TYPE}","mssql")

        newEnvFile=open("/usr/src/app/tmp/etl-mssql.env","w")
        newEnvFile.write(UpdatedEnv)
        newEnvFile.close()
    except Exception as e:
        logger.error(e)



if __name__ == "__main__":
    Config().new_config(argv=sys.argv[1:])
    options=Config.config
    initDatabase(options)
