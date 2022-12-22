#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`perform_patient` -- process patient mapping
=================================================

.. module:: perform_patient
    :platform: Linux/Windows
    :synopsis: module contains methods for importing, deleting patient mappings



"""

from pathlib import Path
import os
from i2b2_cdi.patient import delete_patient
from i2b2_cdi.patient import patient_mapping
from i2b2_cdi.patient import transform_file as TransformFile
from i2b2_cdi.patient import deid_patient as DeidPatient
from i2b2_cdi.common.py_bcp import PyBCP
from i2b2_cdi.common.utils import *
from i2b2_cdi.common.constants import *
from loguru import logger
from i2b2_cdi.config.config import Config
from i2b2_cdi.common.utils import total_time

def load_patient_mapping(mrn_files,factfile=None):
    """Load patient mapping from the given mrn file to the i2b2 instance.

    Args:
        mrn_files (:obj:`str`, mandatory): Path to the files which needs to be imported
    """
    logger.debug("Importing patient mappings")
    rows_skipped_for_mrn = None
    try:
        for file in mrn_files:
            extractFileName = file.split("/")[-1]  
            bcp_file_path,rows_skipped_for_mrn = patient_mapping.create_patient_mapping(file,factfile)
            bcp_upload_patient_mapping(bcp_file_path)               
        logger.success(SUCCESS)
        return rows_skipped_for_mrn
    except Exception as e:
        logger.error("Failed to load patient mapping : {}", e)
        raise e

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
        _bcp = PyBCP(
            table_name="patient_mapping",
            import_file=bcp_file_path,
            delimiter=str(config.bcp_delimiter),
            batch_size=10000,
            error_file=base_dir + "/logs/error_bcp_patient_mappings.log")
        if(str(config.crc_db_type)=='pg'):
            _bcp.upload_facts_pg(config)
        elif(str(config.crc_db_type)=='mssql'):
            _bcp.upload_facts_sql(config)
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
        _bcp = PyBCP(
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
            _bcp.execute_sql_pg(create_table_path,config)
            _bcp.upload_facts_pg(config)
            _bcp.execute_sql_pg(load_patient_path,config)
        elif(str(config.crc_db_type)=='mssql'):
            create_table_path = Path('i2b2_cdi/resources/sql') / \
            'create_patient_dimension_temp.sql'
            load_patient_path = Path('i2b2_cdi/resources/sql') / \
            'load_patient_dimension_from_temp.sql'
            _bcp.execute_sql(create_table_path,config)
            
            _bcp.upload_facts_sql(config)
            _bcp.execute_sql(load_patient_path,config)
        logger.info('exiting bcp_upload_patient_dimension')
        
    except Exception as e:
        logger.error("Failed to upload patient dimensions using BCP : {}", e)
        raise
