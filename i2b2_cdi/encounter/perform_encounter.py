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
import time

def delete_encounters():
    """Delete the encounters from i2b2 instance"""
    logger.info("Deleting encounters")
    try:
        DeleteEncounter.delete_encounters()
        logger.success(SUCCESS)
    except Exception as e:
        logger.error("Failed to delete encounters : {}", e)
        raise

def delete_encounter_mappings():
    """Delete the encounter mapping from i2b2 instance"""
    logger.info("Deleting encounter mappings")
    try:
        DeleteEncounter.delete_encounter_mapping()
        logger.success(SUCCESS)
    except Exception as e:
        logger.error("Failed to delete encounter mappings : {}", e)
        raise


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


def load_encounters(encounter_files):
    """Load encounters from the given file to the i2b2 instance using bcp tool.
    Args:
        encounter_files (:obj:`str`, mandatory):List of files which needs to be imported
    """
    try:
        # Create encounter mapping
        start = time.time()
        create_encounter_mapping(encounter_files)
        end = time.time()
        f=open("/usr/src/app/tmp/common.csv", "a")
        f.write("Create encounter mapping  || encounter_mapping"+","+str(end-start)[:4]+"\n")
        f.close()
        for file_path in encounter_files:
            extractFileName = file_path.split("/")
            extractFileName = extractFileName[-1]
            filename="/usr/src/app/tmp/"+"log_"+extractFileName
            f=open(filename, "a")
            start = time.time()
            deid_file_path = de_identify_encounters(file_path)
            end = time.time()
            f.write("de_identify_encounters  || encounter_mapping"+","+str(end-start)[:4]+"\n")

            start = time.time()
            bcp_file_path = convert_csv_to_bcp(deid_file_path)
            end = time.time()
            f.write("convert_csv_to_bcp  || encounter_mapping"+","+str(end-start)[:4]+"\n")

            start = time.time()
            bcp_upload_encounters(bcp_file_path)
            end = time.time()
            f.write("bcp_upload_encounters  || encounter_mapping"+","+str(end-start)[:4]+"\n")
            f.close()
        logger.success(SUCCESS)
    except Exception as e:
        logger.error("Failed to load encounters : {}", e)
        raise


def de_identify_encounters(file_path):
    """DeIdentify the encounters data
    Args:
        file_path (:obj:`str`, mandatory): Path to the file which needs to be deidentified
    Returns:
        str: path to the deidentified file
    """
    logger.info("De-identifying encounters")
    try:
        deid_file_path, error_file_path = DeidEncounter.do_deidentify(
            file_path)
        logger.info(
            "Check error logs of encounter de-identification if any : {}", error_file_path)
        return deid_file_path
    except Exception as e:
        logger.error("Failed to deidentify the encounters : {}", e)
        raise

def create_encounter_mapping(file_list):
    """Load encounter mapping from the given encounetr or fact file to the i2b2 instance.

    Args:
        file_list (:obj:`str`, mandatory): Path to the files which needs to be imported
    """
    try:
        for csv_file in file_list:
            extractFileName = csv_file.split("/")
            extractFileName = extractFileName[-1]
            filename="/usr/src/app/tmp/"+"log_"+extractFileName
            f=open(filename, "a")
            start = time.time()
            bcp_file_path = EncounterMapping.create_encounter_mapping(
                csv_file)
            end = time.time()
            f.write("create_encounter_mapping  || encounter mapping "+  "  : "+str(end-start)[:4]+"\n")
            # Upload patient mapping using bcp
            if os.path.exists(bcp_file_path):
                start = time.time()
                bcp_upload_encounter_mapping(bcp_file_path)
                end = time.time()
                f.write("bcp_upload_encounter_mapping  || encounter mapping "+  "  : "+str(end-start)[:4]+"\n")
            f.close()
    except Exception as e:
        logger.error("Failed to create encounter mappings : {}", e)
        raise


def bcp_upload_encounter_mapping(bcp_file_path):
    """Upload the encounters data from bcp file to the i2b2 instance

    Args:
        bcp_file_path (:obj:`str`, mandatory): Path to the bcp file having encounters data

    """
    logger.info("Uploading encounter mappings using BCP")
    base_dir = str(Path(bcp_file_path).parents[2])
    error_file = base_dir + "/logs/error_bcp_patient_mappings.log"
    mkParentDir(error_file)
    try:
        _bcp = PyBCP(
            table_name="encounter_mapping",
            import_file=bcp_file_path,
            delimiter=str(Config.config.bcp_delimiter),
            batch_size=10000,
            error_file=base_dir + "/logs/error_bcp_encounter_mappings.log")
        if(Config.config.crc_db_type=='mssql'):
            _bcp.upload_facts_sql()
        elif(Config.config.crc_db_type=='pg'):
            _bcp.upload_facts_pg()
    except Exception as e:
        logger.error("Failed to upload encounter mappings using BCP : {}", e)
        raise


def convert_csv_to_bcp(file_path):
    """Transform the deidentified encounters csv file to the bcp file
    Args:
        file_path (:obj:`str`, mandatory): Path to the file which needs to be converted to bcp file
    Returns:
        str: path to the bcp file
    """
    logger.info("Converting CSV file to BCP format")
    try:
        bcp_file_path, error_file_path = TransformFile.do_transform(file_path)
        logger.info(
            "Check error logs of csv to bcp conversion if any : {}", error_file_path)
        return bcp_file_path
    except Exception as e:
        logger.error("Failed to convert CSV to BCP : {}", e)
        raise


def bcp_upload_encounters(bcp_file_path):
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
            delimiter=str(Config.config.bcp_delimiter),
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
        

        if(str(Config.config.crc_db_type)=='pg'):
            _bcp.execute_sql_pg(create_table_path)
            _bcp.upload_facts_pg()
            _bcp.execute_sql_pg(add_column_path)
            _bcp.execute_sql_pg(load_encounter_path)
        elif(str(Config.config.crc_db_type)=='mssql'):
            _bcp.execute_sql(create_table_path)
            _bcp.upload_facts_sql()
            _bcp.execute_sql(add_column_path)
            _bcp.execute_sql(load_encounter_path)


    except Exception as e:
        logger.error("Failed to upload encounters using BCP : {}", e)
        raise


if __name__ == "__main__":
    args = get_argument_parser()

    if args.delete_encounters:
        delete_encounters()
    elif args.delete_encounter_mappings:
        delete_encounter_mappings()
    elif args.encounter_file:
        # Check database connection before load
        demodata_connection = I2b2crcDataSource()
        demodata_connection.check_database_connection()
        load_encounters(args.encounter_file.name)
        args.encounter_file.close()
