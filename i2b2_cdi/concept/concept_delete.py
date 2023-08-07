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
from Mozilla.exception.mozilla_cdi_database_error import CdiDatabaseError
from loguru import logger
from pathlib import Path

def delete_concepts_i2b2_metadata(config):
    from Mozilla.mozilla_concept_delete import delete_concepts_i2b2_metadata as mozilla_delete_concepts_i2b2_metadata
    mozilla_delete_concepts_i2b2_metadata(config)


def delete_concepts_i2b2_demodata(config):
    """Delete the concepts from i2b2 instance"""
    try:
        logger.debug(
            'Deleting data from i2b2 concept_dimension and derived_concept_job')
        queries = [
            "delete from concept_dimension","delete from provider_dimension"]

        if(config.crc_db_type=='mssql'):
            # queries.append("IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'derived_concept_definition') BEGIN delete from derived_concept_definition END")
            # queries.append("IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'derived_concept_dependency') BEGIN delete from derived_concept_dependency END")
            # queries.append("IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'derived_concept_job_details') BEGIN delete from derived_concept_job_details END")
            queries.append("IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'derived_concept_job') BEGIN delete from derived_concept_job END")
        elif(config.crc_db_type=='pg'):
            # queries.append(" do $$ DECLARE BEGIN if EXISTS (SELECT 1 from pg_tables where tablename='derived_concept_definition' and schemaname= '" +config.crc_db_name+ "') then delete from derived_concept_definition; end if; end $$ ")
            # queries.append(" do $$ DECLARE BEGIN if EXISTS (SELECT 1 from pg_tables where tablename='derived_concept_dependency' and schemaname= '" +config.crc_db_name+ "') then delete from derived_concept_dependency; end if; end $$ ")            
            # queries.append(" do $$ DECLARE BEGIN if EXISTS (SELECT 1 from pg_tables where tablename='derived_concept_job_details' and schemaname= '" +config.crc_db_name+ "') then delete from derived_concept_job_details; end if; end $$ ")
            queries.append(" do $$ DECLARE BEGIN if EXISTS (SELECT 1 from pg_tables where tablename='derived_concept_job' and schemaname= '" +config.crc_db_name+ "') then delete from derived_concept_job; end if; end $$ ")
        with I2b2crcDataSource(config) as cursor:
            delete(cursor, queries)
    except Exception as e:
        raise CdiDatabaseError("Couldn't delete data: {0}".format(str(e)))

def concepts_delete_by_id(config):
    sqlOnt=["delete from i2b2 where upload_id ="+str(config.upload_id),
    "delete from table_access where upload_id ="+str(config.upload_id)]
    sqlCrc=["delete from concept_dimension where upload_id ="+str(config.upload_id)]
    # login_project = str(request.args.get('loginProject'))
    Path("tmp/app_dir").mkdir(parents=True, exist_ok=True)
    logfile = os.path.join("tmp/app_dir/etl-runtime.log")
    
    
    with I2b2crcDataSource(config) as cursor:
        for query in sqlCrc:
            cursor.execute(query)
        with open(logfile, "a") as log_file:
            log_file.write(str(cursor.rowcount)+" Concepts Deleted\n\n")
            log_file.close()

    with I2b2metaDataSource(config) as cursor:
        for query in sqlOnt:
            cursor.execute(query)

def delete(cursor, queries):
    from Mozilla.mozilla_concept_delete import delete as mozilla_delete
    mozilla_delete(cursor, queries)