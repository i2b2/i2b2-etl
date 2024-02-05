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
:mod:`perform_encounter` -- process and inserts encounters using bcp utility
============================================================================

.. module:: perform_encounter
    :platform: Linux/Windows
    :synopsis: module contains methods for transforming and importing encounters


"""

from pathlib import Path
from loguru import logger
from i2b2_cdi.common.bulk_uploader import BulkUploader
from i2b2_cdi.encounter import encounter_mapping as EncounterMapping
from i2b2_cdi.common.utils import *
from i2b2_cdi.common.constants import *
from i2b2_cdi.common.utils import total_time
from i2b2_cdi.common.file_util import get_package_path


def load_encounters(config,encounter_files):
    from Mozilla.mozilla_perform_encounter import load_encounters as mozilla_load_encounters
    mozilla_load_encounters(config,encounter_files)

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
        bulkUploader = BulkUploader(
            table_name="encounter_mapping",
            import_file=bcp_file_path,
            delimiter=str(config.bcp_delimiter),
            batch_size=10000,
            error_file=base_dir + "/logs/error_bcp_encounter_mappings.log")
        # if(config.crc_db_type=='mssql'):
        #     _bcp.upload_facts_sql(config)
        if(config.crc_db_type=='pg'):
            bulkUploader.upload_facts_pg(config)
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
        bulkUploader = BulkUploader(
            table_name="visit_dimension_temp",
            import_file=bcp_file_path,
            delimiter=str(config.bcp_delimiter),
            batch_size=10000,
            error_file=base_dir + "/logs/error_bcp_encounters.log")
        # Create visit dimension temp table
        create_table_path = get_package_path('i2b2_cdi/resources/sql/create_visit_dimension_temp.sql') 
        # Add new columns in visit dimension
        add_column_path = get_package_path('i2b2_cdi/resources/sql/add_columns_visit_dimension.sql')
        # Load encounters from temp to visit dimension
        load_encounter_path = get_package_path('i2b2_cdi/resources/sql/load_visit_dimension_from_temp.sql')        

        if(str(config.crc_db_type)=='pg'):
            bulkUploader.execute_sql_pg(create_table_path,config)
            bulkUploader.upload_facts_pg(config)
            bulkUploader.execute_sql_pg(add_column_path,config)
            bulkUploader.execute_sql_pg(load_encounter_path,config)
        # elif(str(config.crc_db_type)=='mssql'):
        #     _bcp.execute_sql(create_table_path,config)
        #     _bcp.upload_facts_sql(config)
        #     _bcp.execute_sql(add_column_path,config)
        #     _bcp.execute_sql(load_encounter_path,config )


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
