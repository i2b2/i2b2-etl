#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
 
import os

from threading import Thread
from loguru import logger
from i2b2_cdi.config.config import Config
import pathlib

from datetime import datetime as datetime
from flask import jsonify, make_response
import shutil

etl_logger=None
class AsyncLoadDataTask(Thread):
    """Class provides the interface to run the data loading task in a thread"""
    def __init__(self, dir_path,log_path, login_project):
        Thread.__init__(self)
        self.dir_path = dir_path
        self.log_path = log_path
        self.login_project = login_project
        

    def run(self):
        etl_logger=logger.bind(etl=True)
        if etl_logger is None:
                logger.add(self.log_path + '/etl-runtime.log',filter=lambda record: record["extra"].get("etl") == True)
        etl_logger=logger.bind(etl=True)
           
         
        try:
            crc_db_name = os.environ['CRC_DB_NAME']
            ont_db_name = os.environ['ONT_DB_NAME']
            if self.login_project and self.login_project != 'Demo':
                crc_db_name = self.login_project
                ont_db_name = self.login_project
                
            etl_logger.info("Connecting to crc db : {}", crc_db_name)
            etl_logger.debug("Connecting to ont db : {}", ont_db_name)
            etl_logger.info("running aynsc in dir {}",self.dir_path)
            
            logger.debug('Delete log files before import')
            upload_id=datetime.now().strftime('%m%d%H%M%S')
            
            excel_files = [f for f in os.listdir(self.dir_path) if f[-4:] == 'xlsx']# this is done just to take only the xlsx files
            for f in excel_files:
                #convert excel to concepts and facts
                config=Config().new_config(argv=['excel-extract', 
                '--input-file', self.dir_path+'/'+f,
                '--output-dir', self.dir_path,
                '--patient-id-field','MRN','--date-time-field', 'start_date','--category-threshold','3'])
                import i2b2_cdi.excel_extract.runner as excel_extract_runner
                excel_extract_runner.mod_run(config)

            config=Config().new_config(argv=['concept','load','-c', str(pathlib.Path(__file__).parent.absolute())+'/resources/etl.env', 
                '--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name, '--upload-id', upload_id, '--input-dir', self.dir_path])
            chk_dupconcept=[]
            import i2b2_cdi.concept.runner as concept_runner
            chk_dupconcept=concept_runner.mod_run(config)

            import i2b2_cdi.fact.runner as fact_runner
            config=Config().new_config(argv=['fact','load','-c', str(pathlib.Path(__file__).parent.absolute())+'/resources/etl.env',
                '--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name, '--upload-id', upload_id,  '--input-dir', self.dir_path])
            fact_runner.mod_run(config)
            #On the postback the logger instance is breaking up so on adding again the log file works
            
            if chk_dupconcept is not None and len(chk_dupconcept)>0 :
                raise Exception(chk_dupconcept)
        except Exception as e:
            logger.add(self.log_path + '/etl-runtime.log',filter=lambda record: record["extra"].get("etl") == True)
            #etl logger is used to print the log file.
            if chk_dupconcept is not None and len(chk_dupconcept)>0 :
                etl_logger.error("Failed to run async task! Duplicate Row : {}", e)
            else:
                etl_logger.error("Failed to run async task : {}", e)
            
        else:
            logger.add(self.log_path + '/etl-runtime.log',filter=lambda record: record["extra"].get("etl") == True)
            etl_logger.debug("Deleting input files after import")
            msg="\nLoad data : operation completed !!\n"
            etl_logger.success(msg)
        finally:
            shutil.rmtree(self.dir_path, ignore_errors=True, onerror=None)
            if etl_logger is None:
                logger.add(self.log_path + '/etl-runtime.log',filter=lambda record: record["extra"].get("etl") == True)
                etl_logger=logger.bind(etl=True)
            etl_logger.info('removing dir:{}',self.dir_path)
            

    

def _exception_response(error,status_code=500):
    logger.error(error)
    response = make_response(jsonify(status='failed', error=str(error)))
    response.status_code = status_code
    return response

def _error_response(error_msg,status_code=400):
    response = make_response(jsonify(status='failed', error=error_msg))
    response.status_code = status_code
    return response

def _sucess_response():
    response = make_response(jsonify(status='Success'))
    response.status_code = 200
    return response
