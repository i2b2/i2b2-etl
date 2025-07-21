from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.config.config import Config
from  i2b2_cdi.common.utils import clean_json_string
from loguru import logger
import json

class BaseEngine(ABC):
    def __init__(self):
        self.job_id=None
        self.concept_code=None
        self.output=None
       

    @abstractmethod
    def run(self, jobId, projectName, input, conceptCode, conceptPath, host, jobType):
        pass
    

    def get_job_inputs(self,jobId):
        crc_ds = I2b2crcDataSource(Config().new_config(argv=['project','add']))
        with crc_ds as cursor:
            query = "SELECT input FROM job WHERE id = %(jobId)s"
            cursor.execute(query, {'jobId': jobId})
            logger.trace(f"Executing query to fetch job inputs for job ID {jobId}: {query}")

            result = cursor.fetchone()
            logger.trace(f"Fetched job inputs for job ID {jobId}: {result}")

            if result:
                input_json_str = result[0]

                # Fix invalid backslashes
                input_json_str_fixed = input_json_str.replace("\\", "\\\\")
                
                # Now parse
                input_data = json.loads(input_json_str_fixed)
                return(input_data)
            else:
                logger.error(f"No inputs found for job ID {jobId}")
                return None
            
    def get_concept_blob(self,concept_cd):
        crc_ds = I2b2crcDataSource(Config().new_config(argv=['project','add']))
        with crc_ds as cursor: 
            query = "SELECT concept_blob from concept_dimension where concept_cd = %(concept_cd)s"
            cursor.execute(query, {'concept_cd': concept_cd})       
            result = cursor.fetchall()    

        blob = result[0][0]
        blob = blob.replace("'",'"')
        logger.trace("Concept Blob: {}", blob)
        blob = json.loads(blob,  strict=False)
        return blob 

    def send_facts(self,df):
        class_name = self.__class__.__name__
        outDir='/usr/src/app/tmp/{}/output'.format(class_name)
        Path(outDir).mkdir(parents=True, exist_ok=True)
        fpath=outDir+'/llm_{}_facts.csv'.format(class_name)
        factLoad = ['fact','load','-i',outDir]

            
        df.to_csv(fpath,index=False)

        import i2b2_cdi.fact.runner as fact_runner
        logger.debug(factLoad)

        config = Config().new_config(argv=factLoad)
        fact_runner.mod_run(config)
        Path(fpath).unlink()
        return 


    def save_output(self):
        logger.info('saving job output:'+str(self.output))
        config=Config().new_config(argv=['project','add'])  
        try:
            with I2b2crcDataSource(config) as cursor:
                res = json.dumps((self.output)).replace("'",'"')
                sql ="update job set output = %s where id = %s"
                cursor.execute(sql,(str(res),self.job_id,))
        except Exception as e:
            logger.exception("error in :{}",e)
            raise Exception(e)  
        
    