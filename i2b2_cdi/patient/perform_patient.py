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
:mod:`perform_patient` -- process patient mapping
=================================================

.. module:: perform_patient
    :platform: Linux/Windows
    :synopsis: module contains methods for importing, deleting patient mappings


"""

from pathlib import Path
import os
from i2b2_cdi.patient import patient_mapping
from i2b2_cdi.patient import transform_file as TransformFile
from i2b2_cdi.patient import deid_patient as DeidPatient
from i2b2_cdi.common.bulk_uploader import BulkUploader
from i2b2_cdi.common.utils import *
from i2b2_cdi.common.constants import *
from loguru import logger
from i2b2_cdi.common.utils import total_time

def load_patient_mapping(mrn_files,factfile=None): 
    from Mozilla.mozilla_perform_patient import load_patient_mapping as mozilla_load_patient_mapping
    rows_skipped_for_mrn = mozilla_load_patient_mapping(mrn_files,factfile=None)
    return rows_skipped_for_mrn

# @total_time
def load_patient_mapping_from_fact_file(fact_file_list,config):
    """Load patient mapping from the given fact file to the i2b2 instance.

    Args:
        fact_file_list (:obj:`str`, mandatory): Path to the fact file which needs to be imported
    """
    logger.debug("Importing patient mappings from fact file")
    rows_skipped_for_mrn=None
    try:
        for fact_file in fact_file_list:
            logger.trace('Processing file : {}', fact_file)
            extractFileName = fact_file.split("/")[-1]
            
            # for ETLpipeline
            if not os.path.exists('tmp'):
                os.makedirs('tmp')
            mrn_file = patient_mapping.create_patient_mapping_file_from_fact_file(fact_file,config)
            bcp_file_path,rows_skipped_for_mrn = patient_mapping.create_patient_mapping(mrn_file,config)
            # Upload patient mapping using bcp
            if os.path.exists(bcp_file_path):
                
                bcp_upload_patient_mapping(bcp_file_path,config)
                #delete_file_if_exists(mrn_file)
                

        logger.success(SUCCESS)
        return rows_skipped_for_mrn
    except Exception as e:
        logger.error("Failed to load patient mapping : {}", e)
        raise

@total_time
def bcp_upload_patient_mapping(bcp_file_path,config):
    """Upload the encounters data from bcp file to the i2b2 instance

    Args:
        bcp_file_path (:obj:`str`, mandatory): Path to the bcp file having patient mapping data
    """
    logger.debug('entering bcp_upload_patient_mapping')
    logger.debug("Uploading patient mapping using BCP")
    base_dir = str(Path(bcp_file_path).parents[2])
    error_file = base_dir + "/logs/error_bcp_patient_mappings.log"
    mkParentDir(error_file)
    try:
        bulkUploader = BulkUploader(
            table_name="patient_mapping",
            import_file=bcp_file_path,
            delimiter=str(config.bcp_delimiter),
            batch_size=10000,
            error_file=base_dir + "/logs/error_bcp_patient_mappings.log")
        if(str(config.crc_db_type)=='pg'):
            bulkUploader.upload_facts_pg(config)
        # elif(str(config.crc_db_type)=='mssql'):
        #     bulkUploader.upload_facts_sql(config)
        logger.debug('exiting bcp_upload_patient_mapping')
        
    except Exception as e:
        logger.error("Failed to load patient mapping using BCP : {}", e)
        raise

def load_patient_dimension(patient_files,config):
    """Load patients from the given patient file to the i2b2 instance using pyodbc.

    Args:
        patient_files (:obj:`str`, mandatory): List of files which needs to be imported
    """
    
    try:        
        for patient_file_path in patient_files:
            extractFileName = patient_file_path.split("/")
            extractFileName = extractFileName[-1]
            filename="/usr/src/app/tmp/"+"log_"+extractFileName 

            deid_file_path, error_file_path = DeidPatient.do_deidentify(patient_file_path,config)
            logger.debug("Check error logs of patients de-identification if any : {}", error_file_path)
            
            bcp_file_path = TransformFile.do_transform(deid_file_path,config)
            
            bcp_upload_patient_dimension(bcp_file_path,config)


        logger.success(SUCCESS)
    except Exception as e:
        logger.error("Failed to load patients : {}", e)
        raise

@total_time
def bcp_upload_patient_dimension(bcp_file_path,config):
    """Upload the encounters data from bcp file to the i2b2 instance

    Args:
        bcp_file_path (:obj:`str`, mandatory): Path to the bcp file having encounters data

    """
    logger.info('entering bcp_upload_patient_dimension')
    logger.debug("Uploading patient dimensions using BCP")
    base_dir = str(Path(bcp_file_path).parents[2])
    try:
        bulkUploader = BulkUploader(
            table_name="patient_dimension_temp",
            import_file=bcp_file_path,
            delimiter=str(config.bcp_delimiter),
            batch_size=10000,
            error_file=base_dir + "/logs/error_bcp_patients.log")
        

        if(str(config.crc_db_type)=='pg'):
            create_table_path = Path('i2b2_cdi/resources/sql') / \
            'create_patient_dimension_temp_pg.sql'
            load_patient_path = Path('i2b2_cdi/resources/sql') / \
            'load_patient_dimension_from_temp_pg.sql'
            bulkUploader.execute_sql_pg(create_table_path,config)
            bulkUploader.upload_facts_pg(config)
            bulkUploader.execute_sql_pg(load_patient_path,config)
        # elif(str(config.crc_db_type)=='mssql'):
        #     create_table_path = Path('i2b2_cdi/resources/sql') / \
        #     'create_patient_dimension_temp.sql'
        #     load_patient_path = Path('i2b2_cdi/resources/sql') / \
        #     'load_patient_dimension_from_temp.sql'
        #     bulkUploader.execute_sql(create_table_path,config)
            
        #     bulkUploader.upload_facts_sql(config)
        #     bulkUploader.execute_sql(load_patient_path,config)
        logger.info('exiting bcp_upload_patient_dimension')
        
    except Exception as e:
        logger.error("Failed to upload patient dimensions using BCP : {}", e)
        raise
def load_patient_dimension_from_facts(config):
    try:
        from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
        from i2b2_cdi.database import execSql
        from i2b2_cdi.common.file_util import str_from_file

        ont_ds=I2b2crcDataSource(config)
        query = str_from_file('i2b2_cdi/resources/sql/load_patient_dimension_from_facts_pg.sql')
        execSql(ont_ds, query)
        logger.info("loading patient_dimension from facts completed...")
    except Exception as e:
        logger.error(e)