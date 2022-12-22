#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`perform_encounter` -- process and inserts encounters using bcp utility
============================================================================

.. module:: perform_encounter
    :platform: Linux/Windows
    :synopsis: module contains methods for transforming and importing encounters



"""

from pathlib import Path
import argparse
import os
from i2b2_cdi.encounter import deid_encounter as DeidEncounter
from i2b2_cdi.encounter import transform_file as TransformFile
from i2b2_cdi.log import logger
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.common.py_bcp import PyBCP
from i2b2_cdi.encounter import delete_encounter as DeleteEncounter
from i2b2_cdi.encounter import encounter_mapping as EncounterMapping
from i2b2_cdi.common.utils import *
from i2b2_cdi.common.constants import *
from i2b2_cdi.config.config import Config
from i2b2_cdi.common.utils import total_time

def get_argument_parser():
    """Reads the command line arguments and passes to the ArgumentParser

    Returns:
        Namespace: arguments provided on command line while running the script 

    """
    parser = argparse.ArgumentParser(
        description='Import/Delete encounters from i2b2')
    parser.add_argument('-de', '--delete-encounters',
                        action='store_true', help="Delete encounters from i2b2")
    parser.add_argument('-dem', '--delete-encounter-mappings',
                        action='store_true', help="Delete encounter mappings from i2b2")
    parser.add_argument('-ie', '--import-encounters', dest='encounter_file',
                        type=argparse.FileType('r', encoding='UTF-8'), help="Import encounters into i2b2")
    args = parser.parse_args()
    return args


def load_encounters(config,encounter_files):
    """Load encounters from the given file to the i2b2 instance using bcp tool.
    Args:
        encounter_files (:obj:`str`, mandatory):List of files which needs to be imported
    """
    try:
        # Create encounter mapping
        create_encounter_mapping(encounter_files,config)
        for file_path in encounter_files:
            extractFileName = file_path.split("/")
            extractFileName = extractFileName[-1]
            deid_file_path, error_file_path = DeidEncounter.do_deidentify(file_path,config)
            logger.info("Check error logs of encounter de-identification if any : {}", error_file_path)
            bcp_file_path, error_file_path = TransformFile.do_transform(deid_file_path,config)
            logger.info("Check error logs of csv to bcp conversion if any : {}", error_file_path)

            bcp_upload_encounters(bcp_file_path,config)
        logger.success(SUCCESS)
    except Exception as e:
        logger.error("Failed to load encounters : {}", e)
        raise

@total_time
def create_encounter_mapping(file_list,config):
    """Load encounter mapping from the given encounetr or fact file to the i2b2 instance.

    Args:
        file_list (:obj:`str`, mandatory): Path to the files which needs to be imported
    """
    try:
        logger.debug('entering create_encounter_mapping')
        for csv_file in file_list:
            extractFileName = csv_file.split("/")
            extractFileName = extractFileName[-1]
            bcp_file_path = EncounterMapping.create_encounter_mapping(
                csv_file,config)
            if os.path.exists(bcp_file_path):
                bcp_upload_encounter_mapping(bcp_file_path,config)
        logger.debug('exiting create_encounter_mapping')
        
    except Exception as e:
        logger.error("Failed to create encounter mappings : {}", e)
        raise


@total_time
def bcp_upload_encounter_mapping(bcp_file_path,config):
    """Upload the encounters data from bcp file to the i2b2 instance

    Args:
        bcp_file_path (:obj:`str`, mandatory): Path to the bcp file having encounters data

    """
    logger.debug('entering bcp_upload_encounter_mapping')
    logger.info("Uploading encounter mappings using BCP")
    base_dir = str(Path(bcp_file_path).parents[2])
    error_file = base_dir + "/logs/error_bcp_patient_mappings.log"
    mkParentDir(error_file)
    try:
        _bcp = PyBCP(
            table_name="encounter_mapping",
            import_file=bcp_file_path,
            delimiter=str(config.bcp_delimiter),
            batch_size=10000,
            error_file=base_dir + "/logs/error_bcp_encounter_mappings.log")
        if(config.crc_db_type=='mssql'):
            _bcp.upload_facts_sql(config)
        elif(config.crc_db_type=='pg'):
            _bcp.upload_facts_pg(config)
        logger.debug('exiting bcp_upload_encounter_mapping')

    except Exception as e:
        logger.error("Failed to upload encounter mappings using BCP : {}", e)
        raise

def bcp_upload_encounters(bcp_file_path,config):
    """Upload the encounters data from bcp file to the i2b2 instance
    Args:
        bcp_file_path (:obj:`str`, mandatory): Path to the bcp file having encounters data
    """
    logger.info("Uploading encounters using BCP")
    base_dir = str(Path(bcp_file_path).parents[2])
    try:
        _bcp = PyBCP(
            table_name="visit_dimension_temp",
            import_file=bcp_file_path,
            delimiter=str(config.bcp_delimiter),
            batch_size=10000,
            error_file=base_dir + "/logs/error_bcp_encounters.log")
        # Create visit dimension temp table
        create_table_path = Path('i2b2_cdi/resources/sql') / \
            'create_visit_dimension_temp.sql'
        
        # Add new columns in visit dimension
        add_column_path = Path(
            'i2b2_cdi/resources/sql') / 'add_columns_visit_dimension.sql'
        
        # Load encounters from temp to visit dimension
        load_encounter_path = Path(
            'i2b2_cdi/resources/sql') / 'load_visit_dimension_from_temp.sql'
        

        if(str(config.crc_db_type)=='pg'):
            _bcp.execute_sql_pg(create_table_path,config)
            _bcp.upload_facts_pg(config)
            _bcp.execute_sql_pg(add_column_path,config)
            _bcp.execute_sql_pg(load_encounter_path,config)
        elif(str(config.crc_db_type)=='mssql'):
            _bcp.execute_sql(create_table_path,config)
            _bcp.upload_facts_sql(config)
            _bcp.execute_sql(add_column_path,config)
            _bcp.execute_sql(load_encounter_path,config )


    except Exception as e:
        logger.error("Failed to upload encounters using BCP : {}", e)
        raise


# if __name__ == "__main__":
#     args = get_argument_parser()

#     if args.delete_encounters:
#         delete_encounters()
#     elif args.delete_encounter_mappings:
#         delete_encounter_mappings()
#     elif args.encounter_file:
#         # Check database connection before load
#         demodata_connection = I2b2crcDataSource()
#         demodata_connection.check_database_connection()
#         load_encounters(args.encounter_file.name)
#         args.encounter_file.close()
