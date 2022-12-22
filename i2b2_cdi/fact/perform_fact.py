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

# from glob import glob
import glob
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
import pandas as pd
import numpy as np
from i2b2_cdi.fact.TimeAnalysiswithDecorator import total_time
import os

def load_facts(file_list,config):
    """Load the facts from the given file to the i2b2 instance using bcp tool.

    Args:
        file_list (:obj:`str`, mandatory): List of files from which facts to be imported

    """
    
    try:
        # Get concept_cd map for fact validation and to decide column
        concept_map = {}
        factsErrorsList = []
        if not config.disable_fact_validation:
            concept_map = ConceptCdMap.get_concept_code_mapping(config)
        for _file in file_list:
            extractFileName = _file.split("/")
            extractFileName = extractFileName[-1]
            filename="/usr/src/app/tmp/"+"log_"+extractFileName  
        
            deid_file_path, error_file_path = DeidFact.do_deidentify(_file, concept_map,config)
            logger.debug("Check error logs of fact de-identification if any : " + error_file_path)
            factsErrorsList.append(error_file_path)
            bcp_file_path = TransformFile.csv_to_bcp(deid_file_path, concept_map, config)

            for f in glob.glob(bcp_file_path+'/observation_*.bcp'):
                bcp_upload(f, config)
                os.remove(f)
            
            if(str(config.crc_db_type)=='pg'):
                create_indexes = Path('i2b2_cdi/resources/sql') / \
                'create_indexes_observation_fact_pg.sql'
                pyBcp = PyBCP(
                table_name='observation_fact',
                import_file=bcp_file_path,
                delimiter=str(config.bcp_delimiter),
                batch_size=10000,
                error_file="/usr/src/app/tmp/benchmark/logs/error_bcp_facts.log")
                
                pyBcp.execute_sql_pg(create_indexes, config)
        logger.success(SUCCESS)
        return factsErrorsList
    except Exception as e:
        logger.error("Failed to load facts : {}", e)
        raise

@total_time
def bcp_upload(bcp_file_path,config):
    """Upload the fact data from bcp file to the i2b2 instance

    Args:
        bcp_file_path (:obj:`str`, mandatory): Path to the bcp file having fact data

    """
    logger.debug('entering bcp_upload')
    logger.debug("Uploading facts using BCP")
    base_dir = str(Path(bcp_file_path).parents[2])
    try:
        if(str(config.crc_db_type)=='pg'):
            fact_table_name='observation_fact'
        elif(str(config.crc_db_type)=='mssql'):
            fact_table_name='observation_fact_numbered'
        
        _bcp = PyBCP(
            table_name=fact_table_name,
            import_file=bcp_file_path,
            delimiter=str(config.bcp_delimiter),
            batch_size=10000,
            error_file=base_dir + "/logs/error_bcp_facts.log")

        if(str(config.crc_db_type)=='pg'):
            drop_indexes = Path('i2b2_cdi/resources/sql') / \
            'drop_indexes_observation_fact_pg.sql'
            create_indexes = Path('i2b2_cdi/resources/sql') / \
            'create_indexes_observation_fact_pg.sql'
            _bcp.execute_sql_pg(drop_indexes,config)
            logger.info("Dropped indexes from observation_fact")
            _bcp.upload_facts_pg(config)        
        elif(str(config.crc_db_type)=='mssql'):
            create_table_path = Path('i2b2_cdi/resources/sql') / \
            'create_observation_fact_numbered.sql'
            load_fact_path = Path('i2b2_cdi/resources/sql') / \
            'load_observation_fact_from_numbered.sql'
            _bcp.execute_sql(create_table_path,config )
            _bcp.upload_facts_sql(config)
            _bcp.execute_sql(load_fact_path,config)
            
        logger.debug('exiting bcp_upload')
        logger.debug('Completed bcp_upload for file:-')
        logger.debug(bcp_file_path)
            
    except Exception as e:
        logger.error("Failed to uplaod facts using BCP : {}", e)
        raise







            



# if __name__ == "__main__":
#     args = get_argument_parser()

#     if args.delete_facts:
#         delete_facts()
#     elif args.fact_file:
#         # Check database connection before load
#         demodata_connection = I2b2crcDataSource()
#         demodata_connection.check_database_connection()
#         load_facts(args.fact_file.name)
#         args.fact_file.close()
