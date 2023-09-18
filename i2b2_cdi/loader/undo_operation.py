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

import os 
from flask import Flask, request, jsonify, make_response
from i2b2_cdi.loader import _exception_response,_error_response,_sucess_response
from loguru import logger
from i2b2_cdi.database import  DataSource
from i2b2_cdi.config.config import Config

def undo_operation(login_project):    
    """
        This function undo the last data load operation done by ETL (includes creation of derived concept)
    """
    upload_id_concept=0
    upload_id_fact=0
    try:
        crc_db_name = os.environ['CRC_DB_NAME']
        ont_db_name = os.environ['ONT_DB_NAME']
        if login_project != 'Demo':
            crc_db_name = login_project
            ont_db_name = login_project
        logger.debug("Connecting to crc db : {}", crc_db_name)
        logger.debug("Connecting to ont db : {}", ont_db_name)

        # get the latest upload_id
        proj_ds=DataSource( ip=os.environ['CRC_DB_HOST'],
        port=os.environ['CRC_DB_PORT'],
        database=crc_db_name,
        username=os.environ['CRC_DB_USER'],
        password=os.environ['CRC_DB_PASS'],
        dbType=os.environ['CRC_DB_TYPE'])

        upload_id_concept,upload_id_fact,data_flag,volume_flag=get_upload_id_vol_flags(proj_ds,login_project)   
        etl_logger=logger.bind(etl=login_project)

        etl_logger.info("Deleting data..")
        # check which is last operation

        # last operation is concept load 
        if(upload_id_concept>upload_id_fact):
            import i2b2_cdi.concept.runner as concept_runner
            config=Config().new_config(argv=['concept','undo',
            '--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name, '--upload-id', str(upload_id_concept)])
            concept_runner.mod_run(config)

        # last operation is fact load #upload_id_fact = 5 is for volume loaded data 
        elif(upload_id_concept<upload_id_fact and upload_id_fact!=5):
            import i2b2_cdi.fact.runner as fact_runner
            config=Config().new_config(argv=['fact','undo',
                '--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name,
                '--upload-id', str(upload_id_fact)])
            fact_runner.mod_run(config)

        # last operation is concept and fact load
        elif(upload_id_concept==upload_id_fact and upload_id_fact!=0):
            import i2b2_cdi.concept.runner as concept_runner
            config=Config().new_config(argv=['concept','undo',
            '--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name, '--upload-id', str(upload_id_concept)])
            concept_runner.mod_run(config)

            import i2b2_cdi.fact.runner as fact_runner
            config=Config().new_config(argv=['fact','undo',
                '--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name,
                '--upload-id', str(upload_id_fact)])
            fact_runner.mod_run(config)

        return _sucess_response()
    except Exception as e:
        return _error_response(e)
        

def get_upload_id_vol_flags(proj_ds,login_project): 
    '''
    This function fetches the upload id and generate the data & volume flag
    used in Undo operation and check_database(enabling undo and delete buttons)
    '''
    data_flag=False
    volume_flag_concept=False
    volume_flag_fact=False
    volume_flag=False
    upload_id_concept=0
    upload_id_fact=0
    etl_logger=logger.bind(etl=login_project)

    try:
        with proj_ds as cursor:
            try:
                cursor.execute("select upload_id from concept_dimension order by upload_id desc")
                if cursor.fetchone():
                    upload_id_concept = cursor.fetchone()[0]
                    data_flag=True
                    #data is present without upload_id
                    if(upload_id_concept==None):
                        volume_flag_concept=True
                        logger.debug("Volume data Concept")
                else:
                    data_flag=False
            except Exception as e:
                etl_logger.info(e)
            try:
                cursor.execute("select upload_id from observation_fact order by upload_id desc")
                if cursor.fetchone():
                    upload_id_fact = cursor.fetchone()[0]
                    data_flag=True
                    # data is present without upload_id
                    if(upload_id_fact==None or upload_id_fact==5):
                        volume_flag_fact=True
                        logger.debug("Volume data fact")
                
            except Exception as e:
                etl_logger.info(e)                
            if(volume_flag_concept==True and volume_flag_fact==True):
                volume_flag=True
            return upload_id_concept,upload_id_fact,data_flag,volume_flag
    except Exception as e:
        logger.error(e)

def check_db_status():
    '''
    This function gets volume and data flag from get_upload_id_vol_flags function and builds the response  
    '''
    login_project = request.args.get('loginProject')
    if not login_project:
        login_project = 'Demo'
   
    try:
        crc_db_name = os.environ['CRC_DB_NAME']
        if login_project != 'Demo':
            crc_db_name = login_project

        # get the latest upload_id
        proj_ds=DataSource( ip=os.environ['CRC_DB_HOST'],
        port=os.environ['CRC_DB_PORT'],
        database=crc_db_name,
        username=os.environ['CRC_DB_USER'],
        password=os.environ['CRC_DB_PASS'],
        dbType=os.environ['CRC_DB_TYPE'])
        upload_id_concept,upload_id_fact,data_flag,volume_flag=get_upload_id_vol_flags(proj_ds,login_project)   
        response = make_response(jsonify({
        "data":data_flag,
        "volume_data":volume_flag}))
        response.status_code = 200
        return response
    except Exception as err:
        return _exception_response(err)