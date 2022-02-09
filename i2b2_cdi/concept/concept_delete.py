#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`concept_delete` -- Delete the concepts from i2b2 instance
===============================================================

.. module:: concept_delete
    :platform: Linux/Windows
    :synopsis: module contains methods for deleting concepts


"""
# __since__ = "2020-05-08"

import os
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource, I2b2metaDataSource
from i2b2_cdi.exception.cdi_database_error import CdiDatabaseError
from loguru import logger
from i2b2_cdi.config.config import Config
from flask import request

def delete_concepts_i2b2_metadata():
    """Delete the metadata for the concepts from i2b2 instance"""
    try:
        logger.debug('Deleting data from i2b2 metadata and table_access')
        queries = ['truncate table i2b2', 'truncate table table_access']

        with I2b2metaDataSource() as cursor:
            delete(cursor, queries)
    except Exception as e:
        raise CdiDatabaseError("Couldn't delete data: {0}".format(str(e)))


def delete_concepts_i2b2_demodata():
    """Delete the concepts from i2b2 instance"""
    try:
        logger.debug(
            'Deleting data from i2b2 concept dimension, derived_concept_definition, derived_concept_dependency and derived_concept_job_details')
        queries = [
            "delete from concept_dimension"]

        if(Config.config.crc_db_type=='mssql'):
            queries.append("IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'derived_concept_definition') BEGIN delete from derived_concept_definition END")
            queries.append("IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'derived_concept_dependency') BEGIN delete from derived_concept_dependency END")
            queries.append("IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'derived_concept_job_details') BEGIN delete from derived_concept_job_details END")
        elif(Config.config.crc_db_type=='pg'):
            queries.append(" do $$ DECLARE BEGIN if EXISTS (SELECT 1 from pg_tables where tablename='derived_concept_definition' and schemaname= '" +Config.config.crc_db_name+ "') then delete from derived_concept_definition; end if; end $$ ")
            queries.append(" do $$ DECLARE BEGIN if EXISTS (SELECT 1 from pg_tables where tablename='derived_concept_dependency' and schemaname= '" +Config.config.crc_db_name+ "') then delete from derived_concept_dependency; end if; end $$ ")            
            queries.append(" do $$ DECLARE BEGIN if EXISTS (SELECT 1 from pg_tables where tablename='derived_concept_job_details' and schemaname= '" +Config.config.crc_db_name+ "') then delete from derived_concept_job_details; end if; end $$ ")
        with I2b2crcDataSource() as cursor:
            delete(cursor, queries)
    except Exception as e:
        raise CdiDatabaseError("Couldn't delete data: {0}".format(str(e)))

def concepts_delete_by_id():
    sqlOnt=["delete from i2b2 where upload_id ="+str(Config.config.upload_id),
    "delete from table_access where upload_id ="+str(Config.config.upload_id)]
    sqlCrc=["delete from concept_dimension where upload_id ="+str(Config.config.upload_id)]

    # login_project = str(request.args.get('loginProject'))
    # logfile = os.path.join("tmp/api_reserved_dir/",login_project,"etl-runtime.log")
    logfile = os.path.join("tmp/app_dir/etl-runtime.log")
    with I2b2crcDataSource() as cursor:
        for query in sqlCrc:
            cursor.execute(query)
        with open(logfile, "a") as log_file:
            log_file.write(str(cursor.rowcount)+" Concepts Deleted\n\n")
            log_file.close()

    with I2b2metaDataSource() as cursor:
        for query in sqlOnt:
            cursor.execute(query)

def delete(cursor, queries):
    """Execute the provided query using the database cursor

    Args:
        cursor (:obj:`pyodbc.Connection.cursor`, mandatory): Cursor obtained from the Connection object connected to the database
        queries (:obj:`list of str`, mandatory): List of delete queries to be executed 
        
    """
    try:
        for query in queries:
            cursor.execute(query)
    except Exception as e:
        raise CdiDatabaseError("Couldn't delete data: {}".format(str(e)))
