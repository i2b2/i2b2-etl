#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`projectUpgrade` -- I2B2 project upgrade 
=============================================

.. module:: projectUpgrade
    :platform: Linux/Windows
    :synopsis: module contains method for upgrading i2b2 project database.


"""
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource, I2b2metaDataSource, I2b2pmDataSource
from i2b2_cdi.common.file_util import str_from_file
from i2b2_cdi.database import execSql
from loguru import logger
from os.path import dirname, realpath, sep, pardir
from i2b2_cdi.config.config import Config

def upgradeProject(args):
    logger.debug("Upgrade project")
    targetDb=args.project_name
    crc_ds=I2b2crcDataSource()
    ont_ds=I2b2metaDataSource()
    pm_ds=I2b2pmDataSource()
    if targetDb != 'demo':
        crc_ds.database=args.project_name
        ont_ds.database=args.project_name
    try:
        sql_resource_dir=dirname(realpath(__file__)) + sep + pardir + sep + pardir +sep+'i2b2_cdi/project/resources/'
        if(str(Config.config.crc_db_type)=='pg'):
            sql=str_from_file(sql_resource_dir+'sql/upgrade/projectUpgrade_pg.sql')
        elif(str(Config.config.crc_db_type)=='mssql'):
            sql=str_from_file(sql_resource_dir+'sql/upgrade/projectUpgrade_sql.sql')
        ontSql,crcPmSql=sql.split('RUN ON CRC')
        crcsql,pmsql=crcPmSql.split('RUN ON PM')
        execSql(crc_ds,crcsql)
        execSql(ont_ds,ontSql)
        if targetDb == 'demo':
            pmsql,derivedsql = pmsql.split('RUN FOR MAIN DB')    
            execSql(pm_ds,pmsql)
            execSql(crc_ds,derivedsql)
        logger.success("Upgrade project..completed")
    
    except Exception as e:
        logger.error(e)
        raise(e)


if __name__ == "__main__":
    upgradeProject(args)
    logger.info("Success")
