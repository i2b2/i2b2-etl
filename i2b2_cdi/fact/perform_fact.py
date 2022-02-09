#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`perform_fact` -- process facts
====================================

.. module:: perform_fact
    :platform: Linux/Windows
    :synopsis: module contains methods for importing, deleting facts



"""

from pathlib import Path
from i2b2_cdi.fact import deid_fact as DeidFact
from i2b2_cdi.fact import transform_file as TransformFile
from i2b2_cdi.log import logger
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.common.py_bcp import PyBCP
from i2b2_cdi.common.constants import *
from i2b2_cdi.fact import delete_fact
from i2b2_cdi.config.config import Config
from i2b2_cdi.fact import concept_cd_map as ConceptCdMap
import time

def delete_facts():
    """Delete the facts from i2b2 instance"""
    logger.debug("Deleting facts")
    try:
        delete_fact.delete_facts_i2b2_demodata()
        logger.success(SUCCESS)
    except Exception as e:
        logger.error("Failed to delete facts : {}", e)
        raise

def undo_facts():
    logger.debug("Deleting facts (undo operation)")
    try:
        delete_fact.facts_delete_by_id()
        logger.success(SUCCESS)
        
    except Exception as e:
        logger.error("Failed to delete facts : {}", e)
        raise



def load_facts(file_list):
    """Load the facts from the given file to the i2b2 instance using bcp tool.

    Args:
        file_list (:obj:`str`, mandatory): List of files from which facts to be imported

    """
    try:
        # Get concept_cd map for fact validation and to decide column
        concept_map = {}
        if not Config.config.disable_fact_validation:
            concept_map = ConceptCdMap.get_concept_code_mapping()
        for _file in file_list:
            extractFileName = _file.split("/")
            extractFileName = extractFileName[-1]
            filename="/usr/src/app/tmp/"+"log_"+extractFileName  
            f = open(filename, "a")
            start = time.time()
            deid_file_path = de_identify_facts(_file, concept_map)
            end = time.time()  
            f.write("de_identify_facts || facts"+ ","+str(end-start)[:4]+"\n")

            start = time.time()
            bcp_file_path = convert_csv_to_bcp(deid_file_path, concept_map)
            end = time.time()  
            f.write("convert_csv_to_bcp || facts"+  ","+str(end-start)[:4]+"\n")

            start = time.time()
            bcp_upload(bcp_file_path)
            end = time.time()  
            f.write("bcp_upload || facts "+  ","+str(end-start)[:4]+"\n")
            f.close()
        logger.success(SUCCESS)
    except Exception as e:
        logger.error("Failed to load facts : {}", e)
        raise


def de_identify_facts(obs_file_path, concept_map):
    """DeIdentify the fact data

    Args:
        file_path (:obj:`str`, mandatory): Path to the file which needs to be deidentified

    Returns:
        str: path to the deidentified file

    """
    logger.debug("De-identifying facts")
    try:
        deid_file_path, error_file_path = DeidFact.do_deidentify(obs_file_path, concept_map)

        logger.debug(
            "Check error logs of fact de-identification if any : " + error_file_path)
        return deid_file_path
    except Exception as e:
        logger.error("Failed to deidentify the facts : {}", e)
        raise


def convert_csv_to_bcp(deid_file_path, concept_map):
    """Transform the cdi fact file to the bcp fact file

    Args:
        deid_file_path (:obj:`str`, mandatory): Path to the deidentified file which needs to be converted to bcp file

    Returns:
        str: path to the bcp file

    """
    logger.debug("Converting CSV file to BCP format")
    try:
        #print("============>>> deid_file_path======>>>>>>",deid_file_path)
        bcp_file_path = TransformFile.csv_to_bcp(deid_file_path, concept_map)
        return bcp_file_path
    except Exception as e:
        logger.error("Failed to convert CSV to BCP : {}", e)
        raise


def bcp_upload(bcp_file_path):
    """Upload the fact data from bcp file to the i2b2 instance

    Args:
        bcp_file_path (:obj:`str`, mandatory): Path to the bcp file having fact data

    """
    logger.debug("Uploading facts using BCP")
    base_dir = str(Path(bcp_file_path).parents[2])
    try:
        _bcp = PyBCP(
            table_name="observation_fact_numbered",
            import_file=bcp_file_path,
            delimiter=str(Config.config.bcp_delimiter),
            batch_size=10000,
            error_file=base_dir + "/logs/error_bcp_facts.log")

        if(str(Config.config.crc_db_type)=='pg'):
            create_table_path = Path('i2b2_cdi/resources/sql') / \
            'create_observation_fact_numbered_pg.sql'
            load_fact_path = Path('i2b2_cdi/resources/sql') / \
            'load_observation_fact_from_numbered_pg.sql'
            _bcp.execute_sql_pg(create_table_path)
            _bcp.upload_facts_pg()        
            _bcp.execute_sql_pg(load_fact_path)
        elif(str(Config.config.crc_db_type)=='mssql'):
            create_table_path = Path('i2b2_cdi/resources/sql') / \
            'create_observation_fact_numbered.sql'
            load_fact_path = Path('i2b2_cdi/resources/sql') / \
            'load_observation_fact_from_numbered.sql'
            _bcp.execute_sql(create_table_path)
            _bcp.upload_facts_sql()
            _bcp.execute_sql(load_fact_path)
            
    except Exception as e:
        logger.error("Failed to uplaod facts using BCP : {}", e)
        raise


if __name__ == "__main__":
    args = get_argument_parser()

    if args.delete_facts:
        delete_facts()
    elif args.fact_file:
        # Check database connection before load
        demodata_connection = I2b2crcDataSource()
        demodata_connection.check_database_connection()
        load_facts(args.fact_file.name)
        args.fact_file.close()
