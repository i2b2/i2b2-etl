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
from threading import Thread
from loguru import logger
from i2b2_cdi.config.config import Config
from tabulate import tabulate

from datetime import datetime as datetime
from flask import jsonify, make_response
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('max_colwidth', 800)
etl_logger=None
LOG_FILE_NAME = 'etl-runtime.log'

class AsyncLoadDataTask(Thread):
    """Class provides the interface to run the data loading task in a thread"""
    def __init__(self, user_dir, log_dir,login_project,etl_logger,handler_id):
        Thread.__init__(self)
        self.etl_logger=etl_logger
        self.dir_path = user_dir
        self.log_path = log_dir
        self.login_project = login_project
        self.handler_id=handler_id

    def run(self):
        try:
            etl_logger=logger.bind(etl=self.login_project)
            crc_db_name = os.environ['CRC_DB_NAME']
            ont_db_name = os.environ['ONT_DB_NAME']            
            if self.login_project and self.login_project != 'Demo':
                crc_db_name = self.login_project
                ont_db_name = self.login_project
            
            # etl_logger.info("Connecting to crc db : {}", crc_db_name)
            # etl_logger.debug("Connecting to ont db : {}", ont_db_name)
            # etl_logger.info("running aynsc in dir {}",self.dir_path)

            logger.debug('Delete log files before import')
            upload_id=datetime.now().strftime('%Y%m%d%H%M%S%f')[:19]
            
            excel_files = [f for f in os.listdir(self.dir_path) if f[-4:] == 'xlsx']# this is done just to take only the xlsx files
            for f in excel_files:
                #convert excel to concepts and facts
                config=Config().new_config(argv=['excel-extract', 
                '--input-file', self.dir_path+'/'+f,
                '--output-dir', self.dir_path,
                '--patient-id-field','MRN','--date-time-field', 'start_date','--category-threshold','3'])
                import Shells.excel_extract.runner as excel_extract_runner
                excel_extract_runner.mod_run(config)

            files = os.listdir(self.dir_path)
            csvFiles = list(filter(lambda f: f.endswith('.csv'), files))
            
            #concept load
            config=Config().new_config(argv=['concept','load','--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name, '--upload-id', upload_id, '--crc-db-type', os.environ['CRC_DB_TYPE'],'--input-dir', self.dir_path ])
            
            logger.info('..started')

            import i2b2_cdi.concept.runner as concept_runner        
            errDf =concept_runner.mod_run(config)
    
            #determine concept type if concept type column is missing 
            if errDf is not None and len(errDf):
                errDf = generate_new_concept_file(self.dir_path,errDf)
                summarize_erroDf(errDf, self.login_project)

            #Fact load call
            import i2b2_cdi.fact.runner as fact_runner
            config=Config().new_config(argv=['fact','load', '--crc-db-type', os.environ['CRC_DB_TYPE'],'--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name, '--upload-id', upload_id,  '--input-dir', self.dir_path])
            errDf = fact_runner.mod_run(config)
            if len(errDf):
                summarize_erroDf(errDf, self.login_project)


            # etl_logger.debug("Deleting input files after import")
            msg="\nLoad data : operation completed !!\n"
            etl_logger.success(msg)
            
        except Exception as e:
            etl_logger.error(str(e))
        finally:
            #shutil.rmtree(self.dir_path, ignore_errors=True, onerror=None)
            #etl_logger=logger.bind(etl=True)
            etl_logger.info('removing dir:{}',self.dir_path)
            msg="\nLoad data : All operation completed !!\n"
            etl_logger.success(msg)
            logger.remove(self.handler_id)

def generate_new_concept_file(input_dir,errDf):
    # TBD: refactoring required here, remove the hardcoded string validations.
    try:
        if "type does not exists in csv file" in str(errDf):
            logger.debug("Concept Type column is not available")
            import glob
            # checking if fact file is present or not
            if  glob.glob(input_dir+'/*facts.csv'):
                logger.debug("Fact File is present")

                #generate concept_type file and merge with concept file on code
                import i2b2_cdi.fact.runner as fact_runner
                config=Config().new_config(argv=['fact','determine-concept-type','--fact-file-dir',input_dir])
                fact_runner.mod_run(config)               
                concept_type_df=pd.read_csv((glob.glob(input_dir+"/concepts_type.csv"))[0])

                #reading all concepts csv files as DF 
                from i2b2_cdi.common import getConcatCsvAsDf
                cdf=getConcatCsvAsDf(dirPath=input_dir,fileSuffix='concepts.csv')
                
                #if concept type is int then dataframe merge is failing 
                cdf['code']=cdf['code'].astype(str)
                concept_type_df['code']=concept_type_df['code'].astype(str)

                cdf_new=cdf.merge(concept_type_df, on='code',how='left')

                #dropping unnecessary columns in DF
                cdf_new=cdf_new.drop(['input_file','line_num'],axis = 1)
                
                #removing original concepts file missing type column
                for f in glob.glob(input_dir+"/*concepts.csv"):
                    os.remove(f)
                cdf_new.to_csv(input_dir+"/concepts.csv", index = False)

                #loading new concept file having mandatory type column
                import i2b2_cdi.concept.runner as concept_runner    
                config=Config().new_config(argv=['concept','load', '--input-dir', input_dir])
                errDf_new = concept_runner.mod_run(config)
                return errDf_new
                
            else:
                logger.debug("Mandatory column type is missing and fact file is not provided")
                errDf.loc[ errDf['error'] == 'Mandatory column, type does not exists in csv file','error']="Mandatory column type is missing and fact file is not provided"
                return errDf
        else:
            return errDf
    except Exception as e:
        logger.exception(e)


def _exception_response(error,status_code=500):
    logger.exception(error)
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

# this is for the No content success response
def _sucess_response_with_validation_soft_error(message):
    response = make_response(jsonify(status='Success', message= message))
    response.status_code = 204
    return response

def summarize_erroDf(errDf, login_project):
    # if (errDf is None):
    #     return True
    etl_logger=logger.bind(etl=login_project)
    if errDf is not None and len(errDf) > 0:
        # etl_logger.info('Number of errors:{} ',len(errDf))
        arr=[]
        for file in errDf['input_file'].unique():
            tmpErrDF = errDf[errDf['input_file']==file]
            unique_err =tmpErrDF['error'].unique()
            for err in unique_err:
                subDf=tmpErrDF[tmpErrDF['error']==err]
                sDf=subDf.head(3)
                _indexes=[int(x) for x in sDf.line_num]
                arr.append([err,len(subDf),_indexes,file.split('/')[-1]])
            finalDf=pd.DataFrame(arr,columns = ['Error','#Rows','Row-Number','Input-file'])
           
            etl_logger.info(tabulate(finalDf,headers='keys',tablefmt='psql', showindex='never'))
            etl_logger.info("\n")
